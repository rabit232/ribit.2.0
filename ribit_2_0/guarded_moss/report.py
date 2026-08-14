"""Render review-only proposal reports."""

from __future__ import annotations

from .models import Proposal, ReviewDecision


def proposal_report(proposal: Proposal, decision: ReviewDecision | None = None) -> str:
    state = decision.state.value if decision else proposal.review_state.value
    reviewer = decision.reviewer if decision else "unreviewed"
    reason = decision.reason if decision else "No review decision recorded."
    return (
        f"# Proposal: {proposal.title}\n\n"
        f"| Field | Value |\n| --- | --- |\n"
        f"| Identifier | `{proposal.proposal_id}` |\n"
        f"| Kind | `{proposal.kind.value}` |\n"
        f"| Source digest | `{proposal.source_digest}` |\n"
        f"| Review state | `{state}` |\n"
        f"| Reviewer | {reviewer} |\n\n"
        f"## Summary\n\n{proposal.summary}\n\n"
        f"## Review rationale\n\n{reason}\n\n"
        "## Runtime status\n\nThis artifact is review-only and cannot be imported, executed, scheduled, or dispatched.\n"
    )
