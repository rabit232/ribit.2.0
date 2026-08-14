"""Composition facade for data-only, review-pending Ghost/MOSS-inspired workflows."""

from __future__ import annotations

from .context import ContextWindow
from .intake import DataIntake
from .models import DataRecord, Proposal, ProposalKind
from .proposal import create_proposal


class GuardedMossAdapter:
    def __init__(self, context_window: ContextWindow | None = None) -> None:
        self.intake = DataIntake()
        self.context_window = context_window or ContextWindow()

    def ingest(self, source_label: str, text: str) -> DataRecord:
        return self.intake.ingest_text(source_label, text)

    def summarize(self, turns: list[str] | tuple[str, ...]):
        return self.context_window.summarize(turns)

    def propose(self, record: DataRecord, *, proposal_id: str, kind: ProposalKind, title: str, summary: str, template: str = "") -> Proposal:
        return create_proposal(record, proposal_id=proposal_id, kind=kind, title=title, summary=summary, template=template)
