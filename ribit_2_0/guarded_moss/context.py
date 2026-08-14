"""Bounded local context helpers; no autonomous history retention."""

from __future__ import annotations

from .limits import MAX_CONTEXT_CHARS, MAX_CONTEXT_TURNS
from .models import ContextDigest


class ContextWindow:
    def __init__(self, *, maximum_turns: int = MAX_CONTEXT_TURNS, maximum_chars: int = MAX_CONTEXT_CHARS) -> None:
        if maximum_turns < 1 or maximum_chars < 1:
            raise ValueError("Context bounds must be positive.")
        self.maximum_turns = maximum_turns
        self.maximum_chars = maximum_chars

    def summarize(self, turns: list[str] | tuple[str, ...]) -> ContextDigest:
        normalized = tuple(item.strip() for item in turns if isinstance(item, str) and item.strip())
        retained = normalized[-self.maximum_turns:]
        while retained and len("\n".join(retained)) > self.maximum_chars:
            retained = retained[1:]
        return ContextDigest(len(normalized), retained, len(normalized) - len(retained), len("\n".join(retained)))
