# Guarded MOSS 2.1 validation

| Field | Value |
| --- | --- |
| UTC timestamp | `2026-08-14T05:45:37Z` |
| Python | `Python 3.12.3` |
| Test command | `PYTHONPATH=ribit_2_0 python3 -m unittest tests/test_guarded_moss_2_1.py -v` |

## Package syntax

```text
Guarded package compilation passed.
```

## Focused unit tests

```text
test_action_shaped_text_is_flagged_as_untrusted_evidence (tests.test_guarded_moss_2_1.IntakeAndTemplateTests.test_action_shaped_text_is_flagged_as_untrusted_evidence) ... ok
test_inert_template_validator_allows_only_narrow_stubs (tests.test_guarded_moss_2_1.IntakeAndTemplateTests.test_inert_template_validator_allows_only_narrow_stubs) ... ok
test_intake_normalizes_and_records_provenance (tests.test_guarded_moss_2_1.IntakeAndTemplateTests.test_intake_normalizes_and_records_provenance) ... ok
test_normalizer_rejects_blank_and_non_text_input (tests.test_guarded_moss_2_1.IntakeAndTemplateTests.test_normalizer_rejects_blank_and_non_text_input) ... ok
test_proposals_require_schema_and_keep_pending_state (tests.test_guarded_moss_2_1.IntakeAndTemplateTests.test_proposals_require_schema_and_keep_pending_state) ... ok
test_activation_is_unavailable_after_review (tests.test_guarded_moss_2_1.PolicyAndBoundaryTests.test_activation_is_unavailable_after_review) ... ok
test_policy_denies_high_authority_capabilities_by_default (tests.test_guarded_moss_2_1.PolicyAndBoundaryTests.test_policy_denies_high_authority_capabilities_by_default) ... ok
test_shell_boundary_returns_a_denial_without_executing_text (tests.test_guarded_moss_2_1.PolicyAndBoundaryTests.test_shell_boundary_returns_a_denial_without_executing_text) ... ok
test_bounded_context_compaction_is_deterministic (tests.test_guarded_moss_2_1.ScopeContextAndArtifactTests.test_bounded_context_compaction_is_deterministic) ... ok
test_composed_adapter_produces_review_pending_data (tests.test_guarded_moss_2_1.ScopeContextAndArtifactTests.test_composed_adapter_produces_review_pending_data) ... ok
test_ledger_and_qml_note_are_local_metadata_only (tests.test_guarded_moss_2_1.ScopeContextAndArtifactTests.test_ledger_and_qml_note_are_local_metadata_only) ... ok
test_scoped_store_rejects_traversal_and_source_writes (tests.test_guarded_moss_2_1.ScopeContextAndArtifactTests.test_scoped_store_rejects_traversal_and_source_writes) ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.002s

OK
```

## Result

Guarded MOSS 2.1 local tests passed.
