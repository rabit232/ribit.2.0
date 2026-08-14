"""Immutable data contracts for the guarded MOSS-inspired extension."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Capability(str, Enum):
    """Authorities that are denied unless an explicit policy grants them."""

    WORKSPACE_READ = "workspace_read"
    REVIEW_ARTIFACT_WRITE = "review_artifact_write"
    PROCESS_EXECUTION = "process_execution"
    NETWORK_ACCESS = "network_access"
    GUI_CONTROL = "gui_control"
    DEVICE_CONTROL = "device_control"
    DYNAMIC_CODE = "dynamic_code"
    AUTONOMOUS_LOOP = "autonomous_loop"


class ReviewState(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class ProposalKind(str, Enum):
    CONTEXT_NOTE = "context_note"
    PYTHON_TEMPLATE = "python_template"
    QML_RESEARCH_NOTE = "qml_research_note"


@dataclass(frozen=True, slots=True)
class SourceRecord:
    source_label: str
    sha256: str
    char_count: int
    excerpt: str


@dataclass(frozen=True, slots=True)
class DataRecord:
    source: SourceRecord
    normalized_text: str
    review_state: ReviewState = ReviewState.PENDING


@dataclass(frozen=True, slots=True)
class Proposal:
    proposal_id: str
    kind: ProposalKind
    title: str
    summary: str
    source_digest: str
    template: str
    review_state: ReviewState = ReviewState.PENDING


@dataclass(frozen=True, slots=True)
class ReviewDecision:
    proposal_id: str
    state: ReviewState
    reviewer: str
    reason: str


@dataclass(frozen=True, slots=True)
class Denial:
    capability: Capability
    reason: str


@dataclass(frozen=True, slots=True)
class ContextDigest:
    turn_count: int
    retained_turns: tuple[str, ...]
    dropped_turns: int
    character_count: int
