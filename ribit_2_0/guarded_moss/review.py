"""Explicit review decisions for pending proposal records."""

from __future__ import annotations

from .models import Proposal, ReviewDecision, ReviewState


def decide(proposal: Proposal, *, accepted: bool, reviewer: str, reason: str) -> ReviewDecision:
    if proposal.review_state is not ReviewState.PENDING:
        raise ValueError("Only pending proposals may receive a review decision.")
    if not reviewer.strip() or not reason.strip():
        raise ValueError("Reviewer and reason are required for an auditable decision.")
    state = ReviewState.ACCEPTED if accepted else ReviewState.REJECTED
    return ReviewDecision(proposal.proposal_id, state, reviewer.strip(), reason.strip())
