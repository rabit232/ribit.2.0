"""Approved-root path validation for local review artifacts."""

from __future__ import annotations

from pathlib import Path


class ScopeError(ValueError):
    """Raised when a path escapes the explicitly approved workspace root."""


class WorkspaceScope:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root).expanduser().resolve()

    def resolve(self, candidate: str | Path) -> Path:
        path = Path(candidate)
        resolved = (self.root / path).resolve() if not path.is_absolute() else path.resolve()
        try:
            resolved.relative_to(self.root)
        except ValueError as exc:
            raise ScopeError("Path is outside the approved workspace root.") from exc
        return resolved
