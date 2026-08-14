"""Constrained schema validation for review-only proposals."""

from __future__ import annotations

import re

from .limits import MAX_PROPOSAL_SUMMARY, MAX_PROPOSAL_TITLE, MAX_TEMPLATE_CHARS
from .models import ProposalKind

_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]{2,63}$")


class SchemaError(ValueError):
    """Raised when a review proposal is structurally invalid."""


def validate_fields(proposal_id: str, kind: ProposalKind, title: str, summary: str, template: str) -> None:
    if not _ID_PATTERN.fullmatch(proposal_id):
        raise SchemaError("Proposal id must use lowercase letters, digits, hyphens, or underscores.")
    if not isinstance(kind, ProposalKind):
        raise SchemaError("Proposal kind is not recognized.")
    if not title.strip() or len(title) > MAX_PROPOSAL_TITLE:
        raise SchemaError("Proposal title is missing or too long.")
    if not summary.strip() or len(summary) > MAX_PROPOSAL_SUMMARY:
        raise SchemaError("Proposal summary is missing or too long.")
    if len(template) > MAX_TEMPLATE_CHARS:
        raise SchemaError("Proposal template is too long.")
