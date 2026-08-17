---
name: video-frame-extraction-artifact
description: Experimental and incomplete video-frame extraction tools retained as artifacts for later repair. Use only when exploring automatic scene-candidate sampling, reviewing known issues, or improving unfinished video-analysis heuristics; use video-frame-extraction-stable for reliable evidence extraction.
---

# Video Frame Extraction — Experimental Artifact

This package intentionally preserves experimental work. It is **not** the default frame-extraction workflow. Its scripts are retained so future work can reproduce, test, and repair their behavior rather than losing incomplete implementation details.

> Use `video-frame-extraction-stable` for reliable extraction. Use this package only when automatic scene-candidate sampling or heuristic experimentation is explicitly requested.

## Current Artifact

`scripts/scene_candidate_sampler.py` samples a video at a fixed time interval, downsizes frames, computes a grayscale frame-to-frame change score, and writes frames whose score exceeds a threshold as scene candidates.

The approach can be useful for exploratory triage of ordinary constant-frame-rate footage. It is not suitable as the sole evidence source for forensic analysis, archival extraction, or decisions where missed frames matter.

## Known Issues

Read `KNOWN_ISSUES.md` before running or editing the script. Preserve this file and append test results or newly discovered defects rather than deleting failed behavior.

| Area | Current status |
|---|---|
| Fixed-interval sampling | Implemented, but approximate on variable-frame-rate media |
| Hard-cut detection | Exploratory only; threshold is content-dependent |
| Fade/transition handling | Known false-positive and false-negative behavior |
| Timestamp precision | Approximate; candidate filename timestamps are derived from sample order |
| Audio/subtitles/rotation/HDR | Not analyzed or normalized |
| Test corpus | Insufficient; needs varied real-world video tests |

## Workflow

1. Run the stable extractor first and retain its manifest as the trustworthy baseline.
2. Run the artifact sampler on a copy or separate output directory.
3. Compare every candidate against stable frames or the source video before making a claim.
4. Record defects, test media characteristics, command arguments, and expected/actual behavior in `KNOWN_ISSUES.md` or a dated issue note. Do not overwrite prior evidence.
5. When repairing, retain the prior script under `legacy/` and document the replacement's compatibility changes.

## Example

```bash
python scripts/scene_candidate_sampler.py input.mp4 artifact-output \
  --interval 1.0 --threshold 18
```

## Artifact Outputs

| File | Description |
|---|---|
| `samples/` | Interval-sampled PNG frames retained for debugging |
| `candidates/` | Frames whose change score exceeded the selected threshold |
| `candidate_scores.json` | Approximate timestamps, score values, threshold, and limitations |
| `run_log.json` | Invocation context and tool status |

Do not interpret a missing candidate as evidence that nothing changed in the source video.
