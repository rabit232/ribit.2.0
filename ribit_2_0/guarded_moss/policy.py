"""Deny-by-default capability policy for local review workflows."""

from __future__ import annotations

from dataclasses import dataclass

from .models import Capability, Denial


@dataclass(frozen=True, slots=True)
class CapabilityPolicy:
    allowed: frozenset[Capability] = frozenset()

    def permits(self, capability: Capability) -> bool:
        return capability in self.allowed

    def require(self, capability: Capability) -> None:
        if not self.permits(capability):
            raise PermissionError(f"Capability denied: {capability.value}")

    def denial(self, capability: Capability) -> Denial:
        return Denial(capability, f"{capability.value} is denied by the local review policy")


def review_only_policy() -> CapabilityPolicy:
    """Allow only narrow local review-file interaction, never activation."""
    return CapabilityPolicy(frozenset({Capability.WORKSPACE_READ, Capability.REVIEW_ARTIFACT_WRITE}))
