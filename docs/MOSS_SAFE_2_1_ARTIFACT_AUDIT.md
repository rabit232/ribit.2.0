# moss-safe-2.1 Artifact Audit and Source Assessment

## Audit purpose

This document responds to a reproducibility concern: a document or script must not depend on a local file that is absent from the branch, and a generated artifact must be recreated safely if a user removes it. The audit also records a static, non-executing review of the supplied materials for possible **future** use in `MockRibit20LLM` or the Termux bot `0.2` branch.

> No uploaded Python source was imported or executed. The inspection used Python AST parsing and text reads only. No source from the uploads was copied into a runtime package in this audit.

## Artifact audit result

The `moss-safe-2.1` remote branch contains the transcript and its generator. The following required paths were checked locally and in the remote Git tree.

| Path | Remote branch status | Runtime role | Missing-file behavior |
| --- | --- | --- | --- |
| `test_runs/guarded_moss_ten_turn_demo.md` | Present and committed | Saved deterministic ten-turn transcript. | If deleted locally, the generator recreates it. |
| `scripts/run_guarded_moss_demo.py` | Present and committed | Writes the transcript. | Resolves its own repository root and creates `test_runs/` before writing. |
| `test_runs/guarded_moss_latest.md` | Present and committed | Latest focused validation summary. | `run_guarded_moss_tests.sh` recreates it. |
| `scripts/run_guarded_moss_tests.sh` | Present and committed | Runs compilation and the focused test suite. | Creates `test_runs/` before producing a timestamped report and latest copy. |
| `docs/MOSS_SAFE_2_1_DESIGN.md` | Present and committed | Original design and provenance report. | Static documentation only. |
| `docs/MOSS_SAFE_2_1_VALIDATION_AND_DEMO.md` | Present and committed | Validation and demonstration documentation. | Links resolve to committed artifacts; instructions now use the standalone generator command. |
| `scripts/check_guarded_moss_artifacts.py` | Added by this audit | Verifies required paths and local Markdown link targets. | Exits nonzero rather than allowing a silent broken reference. |

### Repair made

The transcript file was already committed, so the remote branch did not contain a dangling reference. However, the first form of `run_guarded_moss_demo.py` relied on a caller-set `PYTHONPATH`. That could make a direct command fail with an import error even though the transcript path itself was valid. The script now derives the repository root from its own file location, adds only the local `ribit_2_0` source directory to its import path, creates `test_runs/`, and writes the Markdown artifact.

This was tested by deleting `test_runs/guarded_moss_ten_turn_demo.md`, changing the working directory to `/tmp`, and running:

```bash
python3 /path/to/ribit.2.0/scripts/run_guarded_moss_demo.py
```

The script recreated a non-empty transcript containing all ten turns. The focused validation runner then passed again and wrote `test_runs/guarded_moss_20260817T151454Z.md` and `test_runs/guarded_moss_latest.md`.

### Ongoing check

Run the following from the branch root before relying on the reports:

```bash
python3 scripts/check_guarded_moss_artifacts.py
scripts/run_guarded_moss_tests.sh
python3 scripts/run_guarded_moss_demo.py
```

The artifact checker verifies seven required files and all local Markdown links in `README.md`, `MOSS_SAFE_2_1_DESIGN.md`, and `MOSS_SAFE_2_1_VALIDATION_AND_DEMO.md`. It does not run model, shell, web, GUI, device, or activation code.

## Supplied-material classification

| Submitted item | Inspection result | Potential value | Decision |
| --- | --- | --- | --- |
| `message(1).txt` | Conversation transcript from “KarlsonAI,” with emotional labels and a saved `karlson_memory.pkl` notice. | Inspiration for user-facing empathy test cases and transparent tone labels. | **Reference-only.** Do not copy private transcript content or unscoped pickle persistence. |
| `message(2).txt` | Parsed 157,734-character monolithic Python emotional-engine script. It contains structured emotion data, phrase analysis, dataset scoring, a background thread, Rich UI, GGUF loading, and automatic installer calls. | Reimplement a very small bounded emotion-analysis record and negation-aware phrase handling. | **Selective adaptation only.** Never import the monolith. |
| `message(3).txt` | Parsed 31,107-character local reasoning module with optional `llama_cpp`, bounded dialogue slicing, and heuristic fallback. | Provider-parameter validation, bounded history, explicit backend status, and safe fallback structure. | **Selective adaptation only.** Do not copy consciousness, autonomous-continuity, threatening, or hidden-state prompts. |
| `messages.gz` | 2,024,504-byte decompressed Discord/Mindustry conversation archive. Sampled only as text. | No identified Ribit, Termux, MockLLM, or safety-module source value. | **Exclude.** Treat as unrelated unreviewed conversational data. |
| `message.txt` | PGP public-key block. | Potential key material only if a separate signing/verification task is explicitly requested. | **Exclude from runtime and commits.** |

## Static authority findings

The supplied sources were processed with an AST-only inventory; no imports, installers, threads, models, or command loops were run.

| Source | Static design observations | High-impact indicators | Consequence |
| --- | --- | --- | --- |
| `message(2).txt` | 16 classes, including `EmotionDef`, `EventAppraisal`, `HumanBrain`, and `GGUFModelConnector`; token and phrase emotion detection; dataset-scoring helpers. | `os.system` installer calls at lines 135 and 1880; background thread creation at line 918; auto-loads a nearby CSV dataset; Rich UI. | Process/installer and persistent-thread behavior are blocked. Dataset ingestion needs explicit scope, size limit, provenance, and review. |
| `message(3).txt` | `ReasoningEngine` supports local GGUF parameters, a bounded `dialogue_history[-max_history:]`, `max_tokens`, stop tokens, status reporting, and heuristic fallback. | No matching process, web, GUI, device, dynamic-code, or thread indicator in the static scan. Its `llama_cpp` import and model load remain optional local-model integration concerns. | Use only as a design reference for bounds and fallback. The large context packet and autonomy language must not enter a provider prompt unchanged. |

## Safe candidate patterns

The following are **design patterns to reimplement in a separate, tested package**, rather than code to merge wholesale.

| Candidate pattern | Source | Target | Required constraint |
| --- | --- | --- | --- |
| Structured `EmotionSignal` with label, score, trigger excerpt, and explanation. | `EmotionDef` and appraisal structures in `message(2).txt`. | `MockRibit20LLM` display context and Termux `ContextPackage`. | Bound labels and excerpts; do not claim genuine feelings or diagnoses. |
| Negation-aware phrase scoring. | `_count_trigger_hits` and `_detect_phrase_emotions` in `message(2).txt`. | A pure `analyze_text(text) -> EmotionAnalysis` helper. | No thread, persistence, contagion model, “trauma” state, or action route. Include tests for negation and hostile language. |
| Fixed-size recent-message context. | `dialogue_history[-max_history:]` in `message(3).txt`. | Termux `CognitiveRuntime.prepare` and any MockLLM context assembler. | Preserve the existing Termux bounds and exclude room data outside the current scope. |
| Optional local-provider status and heuristic fallback. | `backend_summary` and `respond` in `message(3).txt`. | Existing provider router, not Matrix command handling. | Never auto-install packages or auto-load models from user messages. Use explicit configuration and user-approved paths. |
| Explainable tone selection. | `get_emotional_tone` and state summaries in `message(2).txt`. | Persona metadata for ordinary text replies. | Treat it as a response-style hint only; truthfulness, authorization, and capability policy remain dominant. |

## Blocked or unsuitable patterns

| Pattern | Why it is not adopted |
| --- | --- |
| `os.system(... pip install ...)` and automatic dependency installation | A chat or model response must never obtain installer or process authority. |
| Background ticking, daemon threads, dream cycles, and continuous inner life | The Termux runtime is deliberately message-scoped and has no scheduler or autonomous loop surface. |
| Automatic dataset discovery and full conversation accumulation | Raw data needs provenance, scope, retention limit, and review. It must not become implicit bot memory. |
| Writing/importing generated Python skills | Model and conversation output must remain text or review data, never imported executable code. |
| “Alive,” autonomous, possessive, threatening, or predatory system prompts | The agent should not falsely claim consciousness, ongoing private life, hidden autonomy, or coercive intent. |
| Hardware, LED, ROS, browser, GUI, or device connections | Those capabilities are not part of the safe text-only Matrix/Termux message path. |

## Recommended integration path

The best compatible route is a future **`emotion_context`** module that is pure, synchronous, and text-only. It should accept one message, return a small serializable analysis, and be consumed as untrusted metadata by existing context builders.

| Target | Insertion point | Safe behavior |
| --- | --- | --- |
| `rabit232/termux-bot` branch `0.2` | `ribit_termux/cognition/context.py` inside the already bounded `ContextBuilder.build` workflow. | Add a compact `emotion_analysis` field to the provider context, with capped scores and a “style hint only” instruction. Do not alter the conversation guard or provider authorization path. |
| `rabit232/ribit.2.0` `MockRibit20LLM` | A separate adapter called before display-text selection, not inside controller or command routing. | Produce an explainable tone hint and include it only in ordinary response text or diagnostics. Never interpret model output as an action. |

Any future implementation should include syntax checks, tests for neutral/negative/negated phrases, scope and retention tests, explicit denial tests for process/network/GUI/device authority, and a saved reproducible report.
