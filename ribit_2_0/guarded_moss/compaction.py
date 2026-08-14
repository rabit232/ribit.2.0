"""Render bounded context summaries as reviewable, non-authoritative metadata."""

from __future__ import annotations

from .models import ContextDigest


def compact_markdown(digest: ContextDigest) -> str:
    lines = [
        "# Context digest",
        "",
        f"- Source turns: {digest.turn_count}",
        f"- Retained turns: {len(digest.retained_turns)}",
        f"- Dropped turns: {digest.dropped_turns}",
        f"- Retained characters: {digest.character_count}",
        "",
        "## Retained text",
        "",
    ]
    lines.extend(f"{index}. {value}" for index, value in enumerate(digest.retained_turns, start=1))
    return "\n".join(lines) + "\n"
