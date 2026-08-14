"""Regression tests for the isolated 2.1 guarded MOSS-inspired package."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from guarded_moss.activation import ActivationBlockedError, activate, activation_status
from guarded_moss.adapter import GuardedMossAdapter
from guarded_moss.compaction import compact_markdown
from guarded_moss.context import ContextWindow
from guarded_moss.intake import DataIntake
from guarded_moss.ledger import append_event
from guarded_moss.models import Capability, ProposalKind, ReviewState
from guarded_moss.normalizer import NormalizationError, normalize_text
from guarded_moss.policy import CapabilityPolicy, review_only_policy
from guarded_moss.proposal import create_proposal
from guarded_moss.qml import qml_note
from guarded_moss.report import proposal_report
from guarded_moss.review import decide
from guarded_moss.sanitizer import flagged_terms, safety_label
from guarded_moss.schema import SchemaError
from guarded_moss.scope import ScopeError, WorkspaceScope
from guarded_moss.shell import ShellBoundary
from guarded_moss.store import ScopedStore
from guarded_moss.templates import render_stub
from guarded_moss.validator import TemplateValidationError, validate_python_template


class PolicyAndBoundaryTests(unittest.TestCase):
    def test_policy_denies_high_authority_capabilities_by_default(self) -> None:
        policy = CapabilityPolicy()
        for capability in Capability:
            self.assertFalse(policy.permits(capability))
        for capability in (Capability.PROCESS_EXECUTION, Capability.NETWORK_ACCESS, Capability.GUI_CONTROL, Capability.DEVICE_CONTROL, Capability.DYNAMIC_CODE, Capability.AUTONOMOUS_LOOP):
            with self.subTest(capability=capability):
                with self.assertRaises(PermissionError):
                    policy.require(capability)

    def test_shell_boundary_returns_a_denial_without_executing_text(self) -> None:
        denial = ShellBoundary(review_only_policy()).request("rm -rf /; echo unsafe")
        self.assertEqual(denial.capability, Capability.PROCESS_EXECUTION)
        self.assertIn("denied", denial.reason)

    def test_activation_is_unavailable_after_review(self) -> None:
        record = DataIntake().ingest_text("chat", "Provide a safe stub")
        proposal = create_proposal(record, proposal_id="demo_stub", kind=ProposalKind.PYTHON_TEMPLATE, title="Safe stub", summary="Review only", template=render_stub("A safe demo", "demo"))
        decision = decide(proposal, accepted=True, reviewer="tester", reason="Safe inert interface")
        self.assertIn("intentionally unavailable", activation_status(proposal, decision))
        with self.assertRaises(ActivationBlockedError):
            activate(proposal)


class IntakeAndTemplateTests(unittest.TestCase):
    def test_intake_normalizes_and_records_provenance(self) -> None:
        record = DataIntake().ingest_text(" upload-note ", "  line one\r\nline two  ")
        self.assertEqual(record.normalized_text, "line one\nline two")
        self.assertEqual(record.source.source_label, "upload-note")
        self.assertEqual(len(record.source.sha256), 64)
        self.assertEqual(record.review_state, ReviewState.PENDING)

    def test_normalizer_rejects_blank_and_non_text_input(self) -> None:
        for value in ("  ", None):
            with self.subTest(value=value):
                with self.assertRaises(NormalizationError):
                    normalize_text(value)  # type: ignore[arg-type]

    def test_action_shaped_text_is_flagged_as_untrusted_evidence(self) -> None:
        text = "Please run_command then use subprocess and click the window"
        self.assertEqual(safety_label(text), "review_required")
        self.assertTrue(flagged_terms(text))
        self.assertEqual(safety_label("Summarize a concept."), "text_only")

    def test_inert_template_validator_allows_only_narrow_stubs(self) -> None:
        valid = render_stub("Example purpose", "explain", ("topic",))
        validate_python_template(valid)
        for invalid in ("import os\n", "def f():\n    open('x')\n", "x = 1\n", "def f():\n    return value\n"):
            with self.subTest(invalid=invalid):
                with self.assertRaises(TemplateValidationError):
                    validate_python_template(invalid)

    def test_proposals_require_schema_and_keep_pending_state(self) -> None:
        record = DataIntake().ingest_text("chat", "Draft a safe explanation")
        proposal = create_proposal(record, proposal_id="context_note", kind=ProposalKind.CONTEXT_NOTE, title="Context note", summary="A text-only summary")
        self.assertEqual(proposal.review_state, ReviewState.PENDING)
        with self.assertRaises(SchemaError):
            create_proposal(record, proposal_id="BAD ID", kind=ProposalKind.CONTEXT_NOTE, title="x", summary="y")
        decision = decide(proposal, accepted=False, reviewer="reviewer", reason="Needs more provenance")
        self.assertEqual(decision.state, ReviewState.REJECTED)
        self.assertIn("review-only", proposal_report(proposal, decision))


class ScopeContextAndArtifactTests(unittest.TestCase):
    def test_scoped_store_rejects_traversal_and_source_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            store = ScopedStore(WorkspaceScope(root), review_only_policy())
            destination = store.write_text("reviews/proposal.md", "# reviewed")
            self.assertEqual(destination.read_text(encoding="utf-8"), "# reviewed")
            self.assertEqual(store.read_text("reviews/proposal.md"), "# reviewed")
            with self.assertRaises(ScopeError):
                store.write_text("../escape.md", "no")
            with self.assertRaises(ValueError):
                store.write_text("reviews/plugin.py", "print('no')")

    def test_bounded_context_compaction_is_deterministic(self) -> None:
        digest = ContextWindow(maximum_turns=2, maximum_chars=30).summarize(["first", "second", "third"])
        self.assertEqual(digest.turn_count, 3)
        self.assertEqual(digest.retained_turns, ("second", "third"))
        self.assertEqual(digest.dropped_turns, 1)
        rendered = compact_markdown(digest)
        self.assertIn("Dropped turns: 1", rendered)
        self.assertIn("second", rendered)

    def test_ledger_and_qml_note_are_local_metadata_only(self) -> None:
        note = qml_note("Panel concept", "Document declarative UI options without a runtime.")
        self.assertIn("no QML runtime", note.limitation)
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "ledger.json"
            event = append_event(target, event_type="review", subject_id="proposal-1", detail="metadata only")
            payload = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(payload[0]["subject_id"], event.subject_id)

    def test_composed_adapter_produces_review_pending_data(self) -> None:
        adapter = GuardedMossAdapter(ContextWindow(maximum_turns=1, maximum_chars=100))
        record = adapter.ingest("conversation", "Design a constrained note")
        proposal = adapter.propose(record, proposal_id="safe_note", kind=ProposalKind.CONTEXT_NOTE, title="Safe note", summary="No activation")
        self.assertEqual(proposal.review_state, ReviewState.PENDING)
        self.assertEqual(adapter.summarize(["old", "new"]).retained_turns, ("new",))


if __name__ == "__main__":
    unittest.main(verbosity=2)
