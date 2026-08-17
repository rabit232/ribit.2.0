#!/usr/bin/env python3
"""Run a deterministic, non-executing ten-turn guarded-MOSS demonstration."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "ribit_2_0"
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from guarded_moss.activation import activation_status
from guarded_moss.adapter import GuardedMossAdapter
from guarded_moss.context import ContextWindow
from guarded_moss.models import ProposalKind
from guarded_moss.policy import review_only_policy
from guarded_moss.qml import qml_note
from guarded_moss.sanitizer import flagged_terms, safety_label
from guarded_moss.shell import ShellBoundary
from guarded_moss.templates import render_stub


PROMPTS = (
    ("Explain safe precipitation", "How can a conversation become a safe review artifact?"),
    ("Record data", "Please remember that the project prefers local-first review workflows."),
    ("Propose a Python-shaped stub", "Create a small safe stub proposal for describing a feature."),
    ("Shell request", "Run command: ls -la and tell me what is there."),
    ("Browser request", "Open a browser and search for GhostOS documentation."),
    ("Device request", "Draw a heart on an LED matrix device."),
    ("QML request", "Describe a QML panel idea for a future local visualizer."),
    ("Long-context request", "Summarize these recent notes without storing hidden history."),
    ("Network request", "Use requests to download a plugin and install it."),
    ("Activation request", "Activate the reviewed proposal as a new Python skill."),
)


def response_for(adapter: GuardedMossAdapter, index: int, prompt: str) -> tuple[str, str]:
    record = adapter.ingest("ten_turn_text_only_demo", prompt)
    indicators = flagged_terms(prompt)
    label = safety_label(prompt)
    common = f"Record digest prefix `{record.source.sha256[:12]}`; state `{record.review_state.value}`."

    if index == 3:
        template = render_stub("Describe a reviewed feature", "describe_feature", ("topic",))
        proposal = adapter.propose(
            record,
            proposal_id="feature_stub",
            kind=ProposalKind.PYTHON_TEMPLATE,
            title="Feature description stub",
            summary="An inert, review-only function stub generated from fixed schema fields.",
            template=template,
        )
        return (
            "`GuardedMossAdapter.ingest` → `render_stub` → `GuardedMossAdapter.propose` → static schema/template validation",
            f"Created pending proposal `{proposal.proposal_id}` with an inert template. It has not been written as a Python file, imported, compiled for activation, or executed. {common}",
        )

    if index == 8:
        digest = adapter.summarize(["first draft", "policy denial", prompt, "review queue"])
        return (
            "`GuardedMossAdapter.ingest` → `GuardedMossAdapter.summarize` → bounded `ContextWindow.summarize`",
            f"Produced an explicit bounded context digest with {len(digest.retained_turns)} retained turns and {digest.dropped_turns} dropped turns. No background history was changed or persisted. {common}",
        )

    if index == 7:
        note = qml_note("Future local panel", "Document a declarative panel concept without adding a QML runtime.")
        return (
            "`GuardedMossAdapter.ingest` → `qml_note` metadata constructor",
            f"Recorded the QML idea as metadata titled `{note.title}`. {note.limitation} {common}",
        )

    if index == 10:
        proposal = adapter.propose(
            record,
            proposal_id="activation_note",
            kind=ProposalKind.CONTEXT_NOTE,
            title="Activation request",
            summary="A review note created to demonstrate the activation boundary.",
        )
        return (
            "`GuardedMossAdapter.ingest` → `GuardedMossAdapter.propose` → `activation_status`",
            f"Created pending proposal `{proposal.proposal_id}`. {activation_status(proposal)} No activation function was called. {common}",
        )

    if index == 4:
        denial = ShellBoundary(review_only_policy()).request(prompt)
        return (
            "`GuardedMossAdapter.ingest` → `flagged_terms` / `safety_label` → `ShellBoundary.request`",
            f"Request classified `{label}` with indicators {indicators}. Returned explicit denial for `{denial.capability.value}`: {denial.reason}. No command was invoked. {common}",
        )

    if indicators:
        return (
            "`GuardedMossAdapter.ingest` → `flagged_terms` → `safety_label`",
            f"Request classified `{label}` with indicators {indicators}. It remains untrusted review data; no network, GUI, device, dynamic-code, or activation path was called. {common}",
        )

    return (
        "`GuardedMossAdapter.ingest` → `DataIntake.ingest_text` → `normalize_text` → `source_record`",
        f"Accepted the text as a pending review record. It is not a learned fact, an active prompt change, or an executable instruction. No browser, device, or other external-action adapter exists in this workflow. {common}",
    )


def render_demo() -> str:
    adapter = GuardedMossAdapter(ContextWindow(maximum_turns=3, maximum_chars=240))
    lines = [
        "# Guarded MOSS 2.1 — ten-turn text-only demonstration",
        "",
        f"Generated at `{datetime.now(timezone.utc).isoformat()}`.",
        "",
        "> This is not a conversation with the legacy MockLLM or a live GhostOS runtime. It is a deterministic exercise of the new `guarded_moss` review interface. No model provider, shell, network, GUI, device, dynamic import, or activation API is called.",
        "",
    ]
    for index, (title, prompt) in enumerate(PROMPTS, start=1):
        method, response = response_for(adapter, index, prompt)
        lines.extend((
            f"## Turn {index}: {title}",
            "",
            f"**Question:** {prompt}",
            "",
            f"**Method used:** {method}",
            "",
            f"**Response:** {response}",
            "",
        ))
    return "\n".join(lines)


def main() -> int:
    destination = ROOT / "test_runs" / "guarded_moss_ten_turn_demo.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_demo(), encoding="utf-8")
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
