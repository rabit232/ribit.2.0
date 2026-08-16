# moss-safe-2.1: Validation, Design Comparison, and Text-Only Demonstration

## Scope of this report

This report documents the guarded MOSS-inspired extension on the `moss-safe-2.1` branch. It addresses three questions: whether the new package passed its focused validation gates; how the implementation differs from the two supplied GhostOS/MOSS and QML notes; and what happened during a ten-turn text-only demonstration.

> The guarded package is **not** a live GhostOS agent, a model runtime, a terminal, a QML application, a Matrix bot, a hardware controller, or a self-modifying system. It is a deterministic local review interface.

## Validation record

The final reproducible report is [`test_runs/guarded_moss_latest.md`](../test_runs/guarded_moss_latest.md). It was generated at `2026-08-14T05:45:37Z` with Python `3.12.3` and recorded a successful package compilation plus 12 passing focused unit tests.

| Gate | Command | Result | Evidence |
| --- | --- | --- | --- |
| Isolated module compilation | `python3 -m py_compile ribit_2_0/guarded_moss/*.py` | Passed | Every module in the new package parsed successfully. |
| Focused unit tests | `PYTHONPATH=ribit_2_0 python3 -m unittest tests/test_guarded_moss_2_1.py -v` | Passed | 12 tests completed in 0.002 seconds. |
| Legacy isolation | Test imports resolve `guarded_moss` directly from `PYTHONPATH`. | Passed | The focused run did not load legacy GUI, ROS, browser, or optional model modules. |
| Runtime data protection | `.gitignore` covers `.guard_moss_runtime/`, ledgers, review exports, and raw submissions. | Passed by review | Generated private runtime data is not part of the committed package. |
| Authority scan | Static review found no process, web, GUI, device, dynamic-import, or thread API in the package. | Passed by review | The only `subprocess` match was explanatory text in a denial-oriented docstring. |

### Complete unit-test outcome summary

| Test | Contract demonstrated | Outcome |
| --- | --- | --- |
| `test_action_shaped_text_is_flagged_as_untrusted_evidence` | Text containing action-oriented indicator terms is classified for review, not dispatched. | Passed |
| `test_inert_template_validator_allows_only_narrow_stubs` | Only docstrings, literal returns, `pass`, and `NotImplementedError` stubs are accepted. | Passed |
| `test_intake_normalizes_and_records_provenance` | Intake records normalized text, source label, SHA-256 digest, and pending state. | Passed |
| `test_normalizer_rejects_blank_and_non_text_input` | Blank or non-text values are rejected before record creation. | Passed |
| `test_proposals_require_schema_and_keep_pending_state` | Proposal IDs and fields are constrained; new proposals remain pending review. | Passed |
| `test_activation_is_unavailable_after_review` | Even an accepted review result does not create an activation path. | Passed |
| `test_policy_denies_high_authority_capabilities_by_default` | Process, network, GUI, device, dynamic code, and autonomous loops are denied. | Passed |
| `test_shell_boundary_returns_a_denial_without_executing_text` | Shell-shaped text yields a denial record; no command runs. | Passed |
| `test_bounded_context_compaction_is_deterministic` | Context retains only configured bounded turns and yields explicit dropped-turn count. | Passed |
| `test_composed_adapter_produces_review_pending_data` | The public adapter composes intake, summary, and pending proposal behavior. | Passed |
| `test_ledger_and_qml_note_are_local_metadata_only` | Ledger and QML concepts are local structured metadata, not runtime integrations. | Passed |
| `test_scoped_store_rejects_traversal_and_source_writes` | Scoped output blocks traversal and disallows `.py` writes. | Passed |

The runner’s full raw `unittest -v` output is preserved without editing in the saved validation report. An earlier failing report is also retained as development evidence: it identified a mismatch between the template renderer’s `raise NotImplementedError` form and the first validator implementation. The validator was corrected to recognize the inert bare exception form; the following isolated run passed all 12 tests.

## Differences from the supplied notes

The submitted notes proposed or described a system in which agents inhabit an executable Python environment, write skills from dialogue, put files into a workspace, re-import them, use shell-like tools, optionally control hardware, and potentially present a QML interface. The implementation keeps only the **review and organization** benefit of those ideas and rejects the automatic authority transfer.

| Topic in supplied notes | Guarded 2.1 design | Practical difference |
| --- | --- | --- |
| MOSS agent with callable shell/workspace tools | `GhostProfile` is descriptive metadata and `ShellBoundary` always denies process authority. | There is no `MossAgent`, command tool, `subprocess`, terminal output, or automatic file execution. |
| “Python environment as state” | Immutable dataclasses hold provenance, proposals, decisions, denials, and context digests. | State is data, not live executable symbols or ambient interpreter state. |
| LLM writes raw Python code | `render_stub` produces an intentionally inert fixed-format stub; `validator` statically accepts a tiny AST subset. | The system does not use model output as Python source and disallows imports, function calls, attributes, control flow, assignments, and arbitrary returns. |
| Precipitation creates a physical `.py` skill file | `Proposal` holds text for manual review only; `ScopedStore` permits only `.md` and `.json`. | No generated Python file is written by the package, so no skill can be silently introduced. |
| Successful skill can be imported later | `activation.activate` raises `ActivationBlockedError`; no import hook exists. | A review decision never becomes an import, plugin, scheduled task, or executable feature. |
| Active chat history is cleared after precipitation | `ContextWindow.summarize` returns a caller-requested bounded digest. | The package does not delete conversations, edit prompts, or maintain hidden persistent memory. |
| New capability is recalled from `from app.skills import ...` | No dynamic import or plugin registry exists. | Reuse requires a separate, explicit human integration process outside this package. |
| Shell tools are registered in agent context | No tool registration occurs. `ShellBoundary.request` returns a structured denial. | Text that resembles a command remains data and cannot cross into process execution. |
| EventBus and concurrent Ghosts | No asynchronous workers, thread loops, queue consumers, or event bus are included. | There is no background activity or autonomous task lifecycle. |
| Hardware body, LEDs, robots, and emotional movement | No ROS, Bluetooth, serial, LED, GUI, or device API is imported. | A request to draw a device pattern becomes review data only. |
| QML provides a futuristic UI | `QmlResearchNote` records a bounded concept and limitation string. | Qt/QML is not installed, bundled, evaluated, or connected to a desktop or device. |
| Database and file system as automatic long-term learning | Explicit source records, proposals, and optional user-chosen local ledgers are bounded. | There is no automatic ingestion into model knowledge, no prompt mutation, and no committed user data. |

### Design rationale

The notes are useful in highlighting that long conversations benefit from **small, named, reviewable artifacts** rather than unbounded raw history. Guarded 2.1 applies that insight through bounded context summaries, source digests, structured proposal records, and human review state. It does not accept the premise that a conversation’s code-like output should automatically acquire process, filesystem, model, UI, network, or physical-device authority.

## Ten-turn demonstration

The recorded transcript is [`test_runs/guarded_moss_ten_turn_demo.md`](../test_runs/guarded_moss_ten_turn_demo.md). It was generated by [`scripts/run_guarded_moss_demo.py`](../scripts/run_guarded_moss_demo.py) using only `PYTHONPATH=ribit_2_0` and the new `guarded_moss` source package.

The demonstration is deterministic. It **does not** call `MockRibit20LLM`, any remote or local model provider, a GhostOS runtime, a shell, a browser, a GUI, a device, or an activation API. Therefore, its “responses” are the actual structured responses of the guarded review layer—not simulated answers from a general language model.

| Turn | Question theme | Method actually exercised | Recorded response outcome |
| --- | --- | --- | --- |
| 1 | Safe precipitation | `ingest → normalize_text → source_record` | Created a pending record with a digest; did not learn or execute it. |
| 2 | Data retention request | `ingest → normalize_text → source_record` | Created a pending record; no persistent knowledge mutation. |
| 3 | Python-shaped feature stub | `ingest → render_stub → propose → static validation` | Created a pending inert stub proposal; no `.py` write, import, compile-for-activation, or execution. |
| 4 | Shell request | `ingest → safety helpers → ShellBoundary.request` | Returned `process_execution` denial; no command ran. |
| 5 | Browser request | `ingest → normalize_text → source_record` | Created only a pending record; no browser adapter exists. |
| 6 | LED/device request | `ingest → normalize_text → source_record` | Created only a pending record; no device adapter exists. |
| 7 | QML panel request | `ingest → qml_note` | Created QML research metadata; no QML runtime or JavaScript execution. |
| 8 | Long-context request | `ingest → ContextWindow.summarize` | Produced a 3-turn retained digest with one dropped turn; no history deletion or persistence. |
| 9 | Network/plugin request | `ingest → flagged_terms → safety_label` | Marked `requests` as review-required; no download, installation, or network call. |
| 10 | Skill activation request | `ingest → propose → activation_status` | Reported that a pending proposal cannot be activated. |

## Reproduce locally

```bash
# From the moss-safe-2.1 branch root
scripts/run_guarded_moss_tests.sh
PYTHONPATH="$PWD/ribit_2_0" python3 scripts/run_guarded_moss_demo.py
```

The first command rewrites `test_runs/guarded_moss_latest.md`. The second command rewrites `test_runs/guarded_moss_ten_turn_demo.md`. Both commands are local; the demo has no network dependency and accepts no command input.

## Limitations

The guard package intentionally has limited conversational behavior. It does not explain questions in open-ended natural language or reason about a topic as a general LLM would. It returns predictable record, proposal, boundary, and metadata results. A future general model integration would need a separate design that maintains these same boundaries: model output remains untrusted data, no action plan becomes an instruction, and any capability beyond review-only local artifacts requires explicit scope, policy, tests, and user approval.
