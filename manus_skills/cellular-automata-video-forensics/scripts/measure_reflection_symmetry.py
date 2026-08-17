#!/usr/bin/env python3
"""Measure left-right reflection symmetry in a cropped cellular-automata canvas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def crop_image(image: Image.Image, crop: str | None) -> Image.Image:
    if crop is None:
        return image
    try:
        left, top, right, bottom = (int(value) for value in crop.split(","))
    except ValueError as exc:
        raise ValueError("--crop must be left,top,right,bottom") from exc
    if not (0 <= left < right <= image.width and 0 <= top < bottom <= image.height):
        raise ValueError("Crop bounds must fall inside the image")
    return image.crop((left, top, right, bottom))


def compare_about_axis(array: np.ndarray, axis: float) -> tuple[float, float, int]:
    height, width, _ = array.shape
    left = int(math_floor(axis))
    right = int(math_ceil(axis))
    pairs = min(left + 1, width - right)
    if pairs < 1:
        return float("nan"), float("nan"), 0

    left_pixels = array[:, left - pairs + 1:left + 1][:, ::-1].astype(np.float32)
    right_pixels = array[:, right:right + pairs].astype(np.float32)
    color_error = np.abs(left_pixels - right_pixels).mean(axis=2)
    normalized_error = float(color_error.mean() / 255.0)
    score = max(0.0, 1.0 - normalized_error)
    exact_fraction = float((color_error == 0).mean())
    return score, exact_fraction, pairs * height


def math_floor(value: float) -> int:
    return int(np.floor(value))


def math_ceil(value: float) -> int:
    return int(np.ceil(value))


def find_best_axis(array: np.ndarray, requested_axis: float | None) -> tuple[float, float, float, int]:
    _, width, _ = array.shape
    if requested_axis is not None:
        score, exact, comparisons = compare_about_axis(array, requested_axis)
        return requested_axis, score, exact, comparisons

    midpoint = (width - 1) / 2
    candidates = np.arange(max(0.0, midpoint - 4.0), min(width - 1.0, midpoint + 4.0) + 0.001, 0.5)
    results = [(axis, *compare_about_axis(array, float(axis))) for axis in candidates]
    axis, score, exact, comparisons = max(results, key=lambda result: result[1])
    return float(axis), float(score), float(exact), int(comparisons)


def annotate(image: Image.Image, axis: float) -> Image.Image:
    annotated = image.copy().convert("RGB")
    draw = ImageDraw.Draw(annotated)
    draw.line((axis, 0, axis, image.height), fill=(255, 0, 0), width=max(1, image.width // 400))
    return annotated


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path, help="PNG/JPEG canvas image or a full screenshot")
    parser.add_argument("--crop", help="Canvas crop as left,top,right,bottom")
    parser.add_argument("--axis", type=float, help="Reflection axis in cropped-image pixel coordinates")
    parser.add_argument("--output-dir", type=Path, default=Path("symmetry_analysis"))
    args = parser.parse_args()

    if not args.image.is_file():
        parser.error(f"Image does not exist: {args.image}")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    with Image.open(args.image) as source:
        canvas = crop_image(source.convert("RGB"), args.crop)
    array = np.asarray(canvas)
    axis, score, exact_fraction, comparisons = find_best_axis(array, args.axis)

    canvas_path = args.output_dir / "canvas_crop.png"
    canvas.save(canvas_path)
    annotated_path = args.output_dir / "reflection_axis.png"
    annotate(canvas, axis).save(annotated_path)

    result = {
        "source": str(args.image.resolve()),
        "crop": args.crop,
        "canvas_width": canvas.width,
        "canvas_height": canvas.height,
        "axis_x_in_crop": axis,
        "normalized_color_similarity": score,
        "exact_pixel_match_fraction": exact_fraction,
        "mirrored_pixel_comparisons": comparisons,
        "interpretation": "Image-level color similarity. Compression, overlays, and an inaccurate crop can reduce the score.",
        "canvas_crop": str(canvas_path.resolve()),
        "axis_visualization": str(annotated_path.resolve()),
    }
    (args.output_dir / "symmetry_result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
