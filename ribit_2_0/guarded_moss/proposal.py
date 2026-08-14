"""Build constrained, review-pending proposals from already-normalized records."""

from __future__ import annotations

from .models import DataRecord, Proposal, ProposalKind
from .schema import validate_fields
from .validator import validate_python_template


def create_proposal(
    record: DataRecord,
    *,
    proposal_id: str,
    kind: ProposalKind,
    title: str,
    summary: str,
    template: str = "",
) -> Proposal:
    validate_fields(proposal_id, kind, title, summary, template)
    if kind is ProposalKind.PYTHON_TEMPLATE:
        validate_python_template(template)
    elif template and kind is ProposalKind.CONTEXT_NOTE:
        raise ValueError("Context notes do not carry source templates.")
    return Proposal(proposal_id, kind, title.strip(), summary.strip(), record.source.sha256, template)
