---
name: isotropic-cellular-automata-recreation
description: Recreate, compare, and preserve 1D multi-state reflection-isotropic cellular automata. Use when a user provides CA parameters, a rule table, a seed, an exported configuration, or a desired mirror-symmetric CA visualization and wants a reproducible simulation.
---

# Isotropic Cellular Automata Recreation

Use this skill to run reproducible one-dimensional, multi-state cellular automata whose rules are invariant under left-right reflection. Preserve the full configuration so results can be independently regenerated.

## Reproduction Standard

| Available input | Appropriate result claim |
|---|---|
| State count, neighborhood width, and visual reference only | **Parameter-matched approximation** |
| Rule table plus initial world | **Exact reproduction** |
| Seed, deterministic rule-generation algorithm, and initial-world generator | **Seeded reproduction** |
| Partial/uncertain values from a video | **Exploratory simulation** |

Do not describe a new random rule set as the same automaton as the reference. A matching state count, lambda value, or apparent symmetry is insufficient for exact replication.

## Workflow

1. Record the known parameters: `states`, odd `neighborhood`, periodic versus fixed boundaries, rule table/seed, active-rule policy, initial world, number of generations, and color palette.
2. For reflection-isotropic rules, canonicalize each neighborhood as the lexicographically smaller of the neighborhood and its reversal. Apply rules to this canonical key.
3. For a mirror-symmetric result, initialize the world so `world[i] == world[width - 1 - i]`. With reflection-isotropic rules and the same boundary handling on both sides, this symmetry must persist at every generation.
4. Run `scripts/run_isotropic_ca.py` with an explicit `--seed`. Save `config.json`, `rules.json`, `initial_world.json`, `history.npy`, and `render.png` in the same output directory.
5. Measure the generated history's reflection symmetry from its discrete state values. If it is not exactly 1.0, inspect initialization, boundary handling, asymmetric palette/rendering, or a non-isotropic rule table.
6. Compare a recreation to a reference only after aligning the canvas width, generation range, cropping, palette, and time orientation. State deviations plainly.

## Rules and Lambda

For `s` states and an odd neighborhood width `n`, the number of raw neighborhoods is `s^n`. Under reflection isotropy, the number of unique neighborhood classes is:

`(s^n + s^((n + 1) / 2)) / 2`

If using the edge-of-chaos convention, reserve state `0` as dead and force the all-zero neighborhood to produce `0`. Interpret lambda as the proportion of non-all-zero canonical neighborhoods that produce a living state. Keep the random generator and seed because lambda describes only a rule-set statistic, not the rule table itself.[1]

## Long-Running Browser Visualizers

Keep the live CA state and the displayed stream separate. For a finite viewport, retain only the newest `viewportRows` rows in a fixed typed-array **ring buffer** and rasterize that bounded buffer when rendering. Do not repeatedly shift an offscreen canvas by drawing it onto itself; that pattern can fail or degrade after long runs.

1. Retain `width × viewportRows` state cells in a circular buffer and advance an `oldestRow` index on wrap-around.
2. Reuse one or two work rows for live rule evaluation rather than allocating a new row for each generation.
3. Preserve any finite reference history and raw rule table separately from the viewport buffer; use them only to seed the continuation.
4. Expose a small debug API reporting generation, retained-row count, wrap index, and renderer type. Stress-test it past any reported failure threshold, including the transition from saved replay to live calculation.
5. Compare consecutive live rows during testing. If they become identical, report a **fixed point** rather than labeling a static visual result as a renderer failure. Check for longer cycles separately when needed.

For the Edge of Chaos source simulator, first click **Create New Rule Set** after selecting the state count, neighborhood size, and isotropy. This initializes the correct canonical rule-path length. Then set the exact active-rule count through the native slider/change path; changing its text field alone can be overwritten by internal state. In the current page implementation, `completeEnterRulesUsed()` performs this native completion after the field has been assigned. Save the result as a browser-local example only after the active-rule field visibly remains at the requested value.

## Runner Examples

Create a parameter-matched, mirror-symmetric exploration:

```bash
python scripts/run_isotropic_ca.py output --states 9 --neighborhood 5 \
  --width 800 --generations 1200 --lambda-value 0.33 \
  --initial symmetric-random --fill 0.50 --seed 20260817
```

Regenerate an exact saved simulation:

```bash
python scripts/run_isotropic_ca.py output-copy --config existing-output/config.json
```

## Outputs

| File | Purpose |
|---|---|
| `config.json` | Complete runtime parameters and reproducibility metadata |
| `rules.json` | Canonical isotropic rule table |
| `initial_world.json` | Exact initial-state row |
| `history.npy` | Full discrete state history |
| `render.png` | Palette-rendered CA image |
| `summary.json` | Rule counts, activity, and state-level symmetry score |

## Script

Use `scripts/run_isotropic_ca.py`. It accepts either explicit arguments for a new seeded simulation or `--config` to regenerate a saved configuration. It requires Python with `numpy` and `Pillow`.

## References

[1]: https://math.hws.edu/eck/js/edge-of-chaos/CA-info.html "1D Cellular Automata and the Edge of Chaos — Documentation"
[2]: https://math.hws.edu/eck/js/edge-of-chaos/CA.html "Cellular Automata — Edge of Chaos"

The definitions of isotropy, living/dead states, and the lambda control in this skill follow the terminology of the referenced simulator.[1]
