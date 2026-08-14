"""Non-autonomous Ghost-profile metadata for reviewed local workflows."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GhostProfile:
    name: str
    purpose: str
    safe_scopes: tuple[str, ...] = ("text_review", "local_metadata")

    def describe(self) -> str:
        scopes = ", ".join(self.safe_scopes)
        return f"{self.name}: {self.purpose} Safe scopes: {scopes}."
