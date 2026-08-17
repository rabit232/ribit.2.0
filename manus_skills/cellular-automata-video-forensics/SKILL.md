---
name: cellular-automata-video-forensics
description: Extract and analyze cellular-automata patterns from screen recordings, videos, or screenshots. Use when a user wants to identify visible CA parameters, measure reflection symmetry, preserve evidence, or distinguish rule-generated structure from unsupported claims of hidden messages.
---

# Cellular Automata Video Forensics

Use this skill to turn a cellular-automata screen recording into a reproducible evidence package. Work from the source media, retain the raw frames, and separate **observations** from **inferences**.

## Workflow

1. Create an isolated output directory. Run `scripts/extract_video_frames.py` to record media metadata, extract evenly sampled PNG frames, and create a labeled contact sheet.
2. View the contact sheet and two or more full-resolution frames. Identify the simulation canvas and record only values that are actually readable: state count, neighborhood size, isotropy setting, lambda/rule-control value, seed or rule identifier, initial-condition mode, cell size, and generation/time position.
3. Crop only the simulation canvas for quantitative analysis. Do not treat browser chrome, labels, scrollbars, or compression artifacts as cells.
4. Measure horizontal reflection symmetry with `scripts/measure_reflection_symmetry.py`. Give the script the canvas crop and, when necessary, a manual vertical-axis coordinate. Report the score as an image-derived estimate, not proof of the original automaton state.
5. Check parameter consistency. For an odd neighborhood of width `n`, `s` states, and reflection-isotropic rules, calculate the number of unique neighborhood classes as `(s^n + s^((n + 1) / 2)) / 2`. State whether the visible rule-count label agrees with this calculation.
6. If recreation is requested, hand off the extracted parameters, crop, and uncertainty notes to the `isotropic-cellular-automata-recreation` skill. Do not claim exact replication unless the complete rule table and exact initial world, or an export/seed that deterministically regenerates both, are available.

## Evidence Standard

| Claim | Minimum evidence | Wording to use |
|---|---|---|
| Symmetry is visible | Canvas crop plus measured reflection score | “The displayed image is approximately mirror-symmetric.” |
| Isotropic CA is likely | A visible isotropic control or documented rule behavior | “The interface indicates isotropic rules.” |
| Exact parameters | Readable UI fields, source code, or exported configuration | “The recording shows …” |
| Exact replication | Full rule table plus initial world, or deterministic export/seed | “This is an exact reproduction.” |
| Hidden message | A reversible, documented encoding that decodes consistently | “A verifiable encoding is present.” |

Treat visual resemblance to scripts, glyphs, faces, or ancient art as an **interpretive observation**, not encoded content. A complex deterministic system can create ordered, repeated, or symbol-like forms without semantic information. If a user suggests an external scientific claim, research and cite credible primary sources before presenting it as fact.

## Output Package

Create a short `findings.md` containing a table of visible parameters, a table of uncertainty, the symmetry score, the formula check, and links to generated frames/crops. Retain `metadata.json`, `frames/`, `contact_sheet.png`, and all source-crop coordinates so another analysis can be audited.

## Scripts

| Resource | Use |
|---|---|
| `scripts/extract_video_frames.py` | Extract uniformly sampled frames and a contact sheet from an MP4/WebM/MOV recording. |
| `scripts/measure_reflection_symmetry.py` | Measure color-distance reflection symmetry in a cropped canvas. |

## References

[1]: https://math.hws.edu/eck/js/edge-of-chaos/CA-info.html "1D Cellular Automata and the Edge of Chaos — Documentation"
[2]: https://math.hws.edu/eck/js/edge-of-chaos/CA.html "Cellular Automata — Edge of Chaos"

Use the terminology and parameter model documented by the referenced simulator when analyzing that specific application.[1]
