"""Policy-gated persistence for review artifacts, not executable code."""

from __future__ import annotations

from pathlib import Path

from .models import Capability
from .policy import CapabilityPolicy
from .scope import WorkspaceScope

_ALLOWED_SUFFIXES = {".json", ".md"}


class ScopedStore:
    def __init__(self, scope: WorkspaceScope, policy: CapabilityPolicy) -> None:
        self.scope = scope
        self.policy = policy

    def write_text(self, relative_path: str | Path, content: str) -> Path:
        self.policy.require(Capability.REVIEW_ARTIFACT_WRITE)
        destination = self.scope.resolve(relative_path)
        if destination.suffix not in _ALLOWED_SUFFIXES:
            raise ValueError("Only review Markdown and JSON artifacts may be written.")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
        return destination

    def read_text(self, relative_path: str | Path) -> str:
        self.policy.require(Capability.WORKSPACE_READ)
        return self.scope.resolve(relative_path).read_text(encoding="utf-8")
