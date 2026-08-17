---
name: video-frame-extraction-stable
description: Reliably extract uniformly sampled or explicitly timestamped frames from video files, preserve source metadata, and create contact sheets. Use for MP4, MOV, WebM, and other ffmpeg-supported local videos when audit-friendly still-frame evidence is needed.
---

# Stable Video Frame Extraction

Use this stable package for ordinary frame extraction. It prioritizes reproducibility, explicit timestamps, precise seeking, file-existence checks, and an inspectable output manifest.

## Workflow

1. Run `scripts/extract_frames_stable.py` against a local video file. Use either `--samples` for evenly distributed frames or `--timestamps` for explicitly selected times in seconds; do not use both.
2. Inspect `contact_sheet.png` and `manifest.json` before interpreting the frames. For detailed visual analysis, retain `frames/` rather than relying on thumbnails.
3. Cite the requested frame timestamp and its output filename in subsequent analysis. If the video is a screen recording, crop browser/interface areas only after retaining the original extracted frame.
4. If an output frame cannot be decoded, the script fails with the timestamp and preserves all earlier frames. Do not silently infer content from missing frames.

## Guarantees

| Capability | Stable behavior |
|---|---|
| Uniform sampling | Avoids the reported end-of-stream boundary by a codec-aware safety margin. |
| Timestamp seeking | Uses accurate, post-input seeking rather than keyframe-fast seeking. |
| Provenance | Writes source metadata, requested timestamps, output paths, and extraction mode to `manifest.json`. |
| Verification | Checks that every PNG exists and is non-empty before producing the contact sheet. |
| Reuse | Keeps original frames, a contact sheet, and manifest in one directory. |

## Examples

Extract 12 evenly spaced frames:

```bash
python scripts/extract_frames_stable.py input.mp4 output --samples 12
```

Extract exact requested times:

```bash
python scripts/extract_frames_stable.py input.webm output \
  --timestamps 0,3.5,12.0,27.25
```

Set a lower thumbnail width for a compact contact sheet:

```bash
python scripts/extract_frames_stable.py input.mov output --samples 20 --thumbnail-width 240
```

## Dependencies

Require `ffmpeg`, `ffprobe`, Python 3, and Pillow. This skill invokes only local files and does not upload, alter, or delete the source video.

## Output Files

| File | Description |
|---|---|
| `frames/frame_XXX_tXXXXXXXXs.png` | Full-resolution source-derived PNG frame |
| `contact_sheet.png` | Labeled thumbnail overview |
| `manifest.json` | Source metadata, requested time, decoded output paths, and script settings |

## Artifact Version

Use `video-frame-extraction-artifact` only for experimental scene-change heuristics or incomplete/under-repair code. Keep its results separate from stable evidence outputs.
