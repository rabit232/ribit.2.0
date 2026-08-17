#!/usr/bin/env python3
"""Extract verified video frames with explicit timestamps and an audit manifest."""

from __future__ import annotations

import argparse
import json
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def invoke(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, check=True, capture_output=True, text=True)


def probe(source: Path) -> dict:
    command = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=index,codec_name,codec_type,width,height,avg_frame_rate,r_frame_rate,nb_frames,duration",
        "-of", "json", str(source),
    ]
    payload = json.loads(invoke(command).stdout)
    video_streams = [stream for stream in payload.get("streams", []) if stream.get("codec_type") == "video"]
    if not video_streams:
        raise ValueError("No video stream was found")
    stream = video_streams[0]
    duration = float(payload.get("format", {}).get("duration") or stream.get("duration") or 0)
    if duration <= 0:
        raise ValueError("The video duration is unavailable or invalid")
    frame_rate = stream.get("avg_frame_rate") or stream.get("r_frame_rate") or "0/1"
    numerator, denominator = frame_rate.split("/")
    fps = float(numerator) / float(denominator) if float(denominator) else 0.0
    return {
        "source": str(source.resolve()),
        "duration_seconds": duration,
        "video_stream": stream,
        "nominal_fps": fps,
    }


def parse_timestamps(value: str, duration: float) -> list[float]:
    timestamps = []
    for token in value.split(","):
        try:
            timestamp = float(token.strip())
        except ValueError as exc:
            raise ValueError(f"Invalid timestamp: {token!r}") from exc
        if timestamp < 0 or timestamp >= duration:
            raise ValueError(f"Timestamp {timestamp} is outside [0, {duration})")
        timestamps.append(timestamp)
    if not timestamps:
        raise ValueError("At least one timestamp is required")
    return timestamps


def uniform_timestamps(sample_count: int, duration: float, fps: float) -> list[float]:
    if sample_count < 1:
        raise ValueError("--samples must be at least 1")
    # Container duration can exceed the final presentation timestamp. Reserve at least 0.25 s
    # or eight nominal frames for uniform sampling; explicit timestamps are never silently shifted.
    margin = max(0.25, 8.0 / fps) if fps > 0 else 0.25
    final_time = max(0.0, duration - margin)
    if sample_count == 1:
        return [0.0]
    return [final_time * index / (sample_count - 1) for index in range(sample_count)]


def frame_name(index: int, timestamp: float) -> str:
    return f"frame_{index:03d}_t{timestamp:012.6f}s.png"


def extract_frame(source: Path, timestamp: float, target: Path, overwrite: bool) -> None:
    # Place -ss after -i for accurate seeking. This is slower than keyframe-fast seeking by design.
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y" if overwrite else "-n", "-i", str(source),
               "-ss", f"{timestamp:.6f}", "-frames:v", "1", "-map", "0:v:0", "-pix_fmt", "rgb24", str(target)]
    invoke(command)
    if not target.is_file() or target.stat().st_size == 0:
        raise RuntimeError(f"No frame was produced at {timestamp:.6f}s")


def make_contact_sheet(frames: list[tuple[float, Path]], destination: Path, thumbnail_width: int) -> None:
    if thumbnail_width < 32:
        raise ValueError("--thumbnail-width must be at least 32")
    font = ImageFont.load_default()
    opened = [(timestamp, Image.open(frame).convert("RGB")) for timestamp, frame in frames]
    thumb_height = max(1, round(opened[0][1].height * thumbnail_width / opened[0][1].width))
    columns = min(4, len(opened))
    rows = math.ceil(len(opened) / columns)
    label_height = 20
    sheet = Image.new("RGB", (columns * thumbnail_width, rows * (thumb_height + label_height)), "white")
    draw = ImageDraw.Draw(sheet)
    for index, (timestamp, image) in enumerate(opened):
        thumbnail = image.copy()
        thumbnail.thumbnail((thumbnail_width, thumb_height))
        x = (index % columns) * thumbnail_width
        y = (index // columns) * (thumb_height + label_height)
        sheet.paste(thumbnail, (x, y))
        draw.text((x + 3, y + thumb_height + 3), f"t={timestamp:.3f}s", fill="black", font=font)
    sheet.save(destination)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Input local video file")
    parser.add_argument("output_dir", type=Path, help="Directory for frames, contact sheet, and manifest")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--samples", type=int, default=12, help="Uniformly sampled frame count (default: 12)")
    selection.add_argument("--timestamps", help="Comma-separated timestamps in seconds")
    parser.add_argument("--thumbnail-width", type=int, default=320, help="Contact-sheet thumbnail width (default: 320)")
    parser.add_argument("--overwrite", action="store_true", help="Allow replacement of an existing output PNG")
    args = parser.parse_args()

    if not args.source.is_file():
        parser.error(f"Source file does not exist: {args.source}")
    metadata = probe(args.source)
    timestamps = parse_timestamps(args.timestamps, metadata["duration_seconds"]) if args.timestamps else uniform_timestamps(
        args.samples, metadata["duration_seconds"], metadata["nominal_fps"]
    )

    frames_dir = args.output_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    extracted: list[tuple[float, Path]] = []
    for index, timestamp in enumerate(timestamps, start=1):
        target = frames_dir / frame_name(index, timestamp)
        extract_frame(args.source, timestamp, target, args.overwrite)
        extracted.append((timestamp, target))

    contact_sheet = args.output_dir / "contact_sheet.png"
    make_contact_sheet(extracted, contact_sheet, args.thumbnail_width)
    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "tool": "extract_frames_stable.py",
        "source_metadata": metadata,
        "selection": {"mode": "timestamps" if args.timestamps else "uniform", "requested_timestamps_seconds": timestamps},
        "frames": [{"timestamp_seconds": timestamp, "path": str(path.resolve())} for timestamp, path in extracted],
        "contact_sheet": str(contact_sheet.resolve()),
        "accurate_seek": True,
    }
    (args.output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
