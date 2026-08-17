# Known Issues and Repair Backlog

## Status

This package is deliberately retained as an **experimental artifact**. It may be useful for exploratory scene-candidate sampling, but it is not a reliable evidence-extraction tool. Do not delete this record when bugs are found. Add reproducible evidence below and preserve prior entries.

## Confirmed Limitations

| ID | Severity | Area | Current behavior | Repair direction |
|---|---|---|---|---|
| ART-001 | High | Variable-frame-rate video | Candidate timestamps are inferred as `sample_index × interval`; they can drift from decoded presentation times. | Capture frame PTS with `ffprobe -show_frames` or use a library that exposes decoded timestamps. |
| ART-002 | High | Short scenes | Fixed interval sampling can skip a scene or transition entirely. | Add adaptive sampling and seek around candidate boundaries. |
| ART-003 | Medium | Fade transitions | A fade can generate multiple candidates or none, depending on threshold and sample interval. | Add transition aggregation and separate hard-cut/fade scoring. |
| ART-004 | Medium | Motion/UI animation | Camera movement, scrolling, flashing, and animated interfaces can generate false positives. | Combine perceptual differences with local feature tracking or content-aware masking. |
| ART-005 | Medium | Threshold calibration | The default threshold is not normalized across resolution, contrast, or content. | Build a test corpus, expose calibration reports, and select/document a more robust metric. |
| ART-006 | Medium | Existing outputs | The script uses non-overwriting ffmpeg output and fails if sample names already exist. | Add an explicit run ID or a safe resumable manifest mode. |
| ART-007 | Low | Metadata | The report does not capture rotation, HDR/color-space details, audio tracks, or subtitle tracks. | Expand ffprobe metadata and normalize/display metadata deliberately. |
| ART-008 | High | End-of-stream seeking | The pre-repair stable extractor failed on a 22.984195-second uniformly selected timestamp in the supplied 23.04-second MP4, even though it reserved a one-frame end margin. | The preserved implementation remains in `legacy/`. The stable package now reserves the larger of 0.25 seconds or eight nominal frames for uniform sampling; test this policy on a varied codec/VFR corpus. |

## Preserved Failure Artifact

The precise pre-repair implementation is retained at `legacy/extract_frames_stable_pre_end_boundary_repair.py`; its SHA-256 checksum is in the accompanying `.sha256` file. The failure was observed while extracting four uniform samples from `VID_20251115_015659.mp4`. The final requested sample at 22.984195 seconds produced no PNG, despite the input reporting a 23.04-second duration.

## Testing Record

Append a dated entry in this format:

```markdown
### YYYY-MM-DD — Test name

| Field | Value |
|---|---|
| Source characteristics | Codec, duration, frame rate, resolution, VFR/CFR status |
| Command | Exact command line |
| Expected behavior | What should happen |
| Actual behavior | What happened |
| Evidence | Paths, hashes, screenshots, or output manifest |
| Related issue | ART-### or new issue ID |
| Proposed repair | Specific next step |
```

## Repair Policy

Retain the script that produced an issue. For a material repair, copy the prior implementation to `legacy/` using a dated filename, add a test case or reproducible command, update this backlog, and describe any output-format change in `SKILL.md`. Do not relabel an experimental artifact as stable merely because it completes on one input.
