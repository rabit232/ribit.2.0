#!/usr/bin/env python3
"""Extract evenly sampled video frames and generate an audit-friendly contact sheet."""

from __future__ import annotations

import argparse
import json
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def run(command: list[str]) -> str:
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    return completed.stdout


def video_metadata(source: Path) -> dict:
    raw = run([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,duration,nb_frames",
        "-of", "json", str(source),
    ])
    stream = json.loads(raw)["streams"][0]
    numerator, denominator = stream["r_frame_rate"].split("/")
    fps = float(numerator) / float(denominator)
    duration = float(stream.get("duration") or 0)
    return {
        "source": str(source.resolve()),
        "width": int(stream["width"]),
        "height": int(stream["height"]),
        "fps": fps,
        "duration_seconds": duration,
        "frame_count_reported": stream.get("nb_frames"),
    }


def extract_frames(source: Path, output_dir: Path, sample_count: int, duration: float) -> list[Path]:
    frames_dir = output_dir / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    # Sampling exactly at a container's reported duration can fall beyond its final decodable frame.
    safe_end = max(0.0, duration - 0.05)
    timestamps = [0.0] if sample_count == 1 else [safe_end * i / (sample_count - 1) for i in range(sample_count)]
    output_frames: list[Path] = []
    for index, timestamp in enumerate(timestamps, start=1):
        frame = frames_dir / f"frame_{index:03d}_t{timestamp:08.3f}s.png"
        subprocess.run([
            "ffmpeg", "-y", "-ss", f"{timestamp:.6f}", "-i", str(source),
            "-frames:v", "1", "-vf", "format=rgb24", str(frame),
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if not frame.is_file() or frame.stat().st_size == 0:
            raise RuntimeError(f"ffmpeg did not produce a frame at {timestamp:.3f}s")
        output_frames.append(frame)
    return output_frames


def make_contact_sheet(frames: list[Path], output_file: Path, columns: int = 4, thumb_width: int = 320) -> None:
    font = ImageFont.load_default()
    opened = [Image.open(frame).convert("RGB") for frame in frames]
    thumb_height = max(1, round(opened[0].height * thumb_width / opened[0].width))
    label_height = 24
    rows = math.ceil(len(opened) / columns)
    sheet = Image.new("RGB", (columns * thumb_width, rows * (thumb_height + label_height)), "white")

    for index, (image, frame) in enumerate(zip(opened, frames)):
        thumbnail = image.copy()
        thumbnail.thumbnail((thumb_width, thumb_height))
        x = (index % columns) * thumb_width
        y = (index // columns) * (thumb_height + label_height)
        sheet.paste(thumbnail, (x, y))
        ImageDraw.Draw(sheet).text((x + 4, y + thumb_height + 4), frame.name, fill="black", font=font)

    sheet.save(output_file)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Input MP4, MOV, WebM, or other ffmpeg-supported video")
    parser.add_argument("output_dir", type=Path, help="New or existing evidence-package directory")
    parser.add_argument("--samples", type=int, default=12, help="Number of uniformly sampled frames (default: 12)")
    args = parser.parse_args()

    if args.samples < 1:
        parser.error("--samples must be at least 1")
    if not args.source.is_file():
        parser.error(f"Source file does not exist: {args.source}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    metadata = video_metadata(args.source)
    frames = extract_frames(args.source, args.output_dir, args.samples, metadata["duration_seconds"])
    contact_sheet = args.output_dir / "contact_sheet.png"
    make_contact_sheet(frames, contact_sheet)

    metadata["samples_requested"] = args.samples
    metadata["frames"] = [str(frame.resolve()) for frame in frames]
    metadata["contact_sheet"] = str(contact_sheet.resolve())
    (args.output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
