"""A non-executing Shell boundary for transparent capability denial."""

from __future__ import annotations

from .models import Capability, Denial
from .policy import CapabilityPolicy


class ShellBoundary:
    """Represents a shell concept without any subprocess or code authority."""

    def __init__(self, policy: CapabilityPolicy) -> None:
        self.policy = policy

    def request(self, command_text: str) -> Denial:
        del command_text
        if self.policy.permits(Capability.PROCESS_EXECUTION):
            return Denial(Capability.PROCESS_EXECUTION, "Execution is not implemented by this review-only boundary.")
        return self.policy.denial(Capability.PROCESS_EXECUTION)
