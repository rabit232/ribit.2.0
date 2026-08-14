"""Explicit non-activation behavior for all reviewed proposals."""

from __future__ import annotations

from .models import Proposal, ReviewDecision


class ActivationBlockedError(PermissionError):
    """Raised whenever an integration attempts to activate a proposal."""


def activation_status(proposal: Proposal, decision: ReviewDecision | None = None) -> str:
    state = decision.state.value if decision else proposal.review_state.value
    return f"Proposal {proposal.proposal_id} is {state}; runtime activation is intentionally unavailable."


def activate(proposal: Proposal) -> None:
    del proposal
    raise ActivationBlockedError("Review artifacts cannot be imported, executed, scheduled, or dispatched.")
