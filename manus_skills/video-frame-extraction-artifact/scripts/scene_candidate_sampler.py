#!/usr/bin/env python3
"""EXPERIMENTAL: Sample fixed-interval frames and flag abrupt visual-change candidates.

See KNOWN_ISSUES.md before relying on the results. This script is retained as an
artifact for repair and must not replace stable frame extraction.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image


def command_output(command: list[str]) -> str:
    return subprocess.run(command, check=True, capture_output=True, text=True).stdout


def duration_seconds(source: Path) -> float:
    output = command_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(source)
    ]).strip()
    duration = float(output)
    if duration <= 0:
        raise ValueError("Video duration must be positive")
    return duration


def create_interval_samples(source: Path, sample_dir: Path, interval: float) -> list[Path]:
    sample_dir.mkdir(parents=True, exist_ok=True)
    # Known limitation: the fps filter creates evenly timed output, but its filename index does not preserve
    # exact input presentation timestamps, especially for variable-frame-rate inputs.
    filter_expression = f"fps=1/{interval:.12g},format=rgb24"
    target_pattern = sample_dir / "sample_%06d.png"
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-n", "-i", str(source), "-vf", filter_expression,
        str(target_pattern),
    ], check=True)
    samples = sorted(sample_dir.glob("sample_*.png"))
    if not samples:
        raise RuntimeError("ffmpeg produced no interval samples")
    return samples


def change_score(previous: Path, current: Path, side: int = 96) -> float:
    with Image.open(previous) as before, Image.open(current) as after:
        before_gray = np.asarray(before.convert("L").resize((side, side)), dtype=np.int16)
        after_gray = np.asarray(after.convert("L").resize((side, side)), dtype=np.int16)
    return float(np.mean(np.abs(after_gray - before_gray)))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--interval", type=float, default=1.0, help="Approximate sampling interval in seconds")
    parser.add_argument("--threshold", type=float, default=18.0, help="Mean grayscale difference threshold")
    args = parser.parse_args()

    if not args.source.is_file():
        parser.error(f"Source file does not exist: {args.source}")
    if args.interval <= 0:
        parser.error("--interval must be positive")
    if args.threshold < 0:
        parser.error("--threshold must be non-negative")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    samples = create_interval_samples(args.source, args.output_dir / "samples", args.interval)
    candidates_dir = args.output_dir / "candidates"
    candidates_dir.mkdir(exist_ok=True)

    candidates: list[dict] = []
    for index in range(1, len(samples)):
        score = change_score(samples[index - 1], samples[index])
        approximate_timestamp = index * args.interval
        result = {
            "sample_index": index + 1,
            "approximate_timestamp_seconds": approximate_timestamp,
            "score": score,
            "sample_path": str(samples[index].resolve()),
            "is_candidate": score >= args.threshold,
        }
        if result["is_candidate"]:
            candidate_path = candidates_dir / samples[index].name
            shutil.copy2(samples[index], candidate_path)
            result["candidate_path"] = str(candidate_path.resolve())
        candidates.append(result)

    report = {
        "artifact_status": "experimental",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": str(args.source.resolve()),
        "reported_duration_seconds": duration_seconds(args.source),
        "interval_seconds": args.interval,
        "threshold": args.threshold,
        "sample_count": len(samples),
        "candidate_count": sum(item["is_candidate"] for item in candidates),
        "known_limitations": [
            "Candidate timestamps are inferred from sample order, not decoded presentation timestamps.",
            "Threshold behavior varies substantially with fades, camera motion, animated interfaces, and exposure changes.",
            "The sampling interval can miss short scenes or transitions entirely.",
            "A non-candidate does not prove that no meaningful video change occurred.",
        ],
        "candidates": candidates,
    }
    (args.output_dir / "candidate_scores.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "run_log.json").write_text(json.dumps({
        "status": "completed_with_known_limitations",
        "source": str(args.source.resolve()),
        "output_dir": str(args.output_dir.resolve()),
    }, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("artifact_status", "sample_count", "candidate_count", "threshold")}, indent=2))


if __name__ == "__main__":
    main()
