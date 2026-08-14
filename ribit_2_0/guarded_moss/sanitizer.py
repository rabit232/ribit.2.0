"""Classify action-shaped text without treating it as executable instruction."""

from __future__ import annotations

import re


_ACTION_PATTERNS = (
    r"\bsubprocess\b", r"\bos\.system\b", r"\bexec\s*\(", r"\beval\s*\(",
    r"\brun_command\b", r"\bclick\b", r"\btype_text\b", r"\bpress_key\b",
    r"\bimportlib\b", r"\brequests\b", r"\baiohttp\b", r"\bwebbrowser\b",
)


def flagged_terms(value: str) -> tuple[str, ...]:
    """Return normalized indicators found in text; no action is taken."""
    hits: list[str] = []
    for pattern in _ACTION_PATTERNS:
        if re.search(pattern, value, flags=re.IGNORECASE):
            hits.append(pattern.replace("\\b", "").replace("\\s*", " ").replace("\\", ""))
    return tuple(hits)


def safety_label(value: str) -> str:
    return "review_required" if flagged_terms(value) else "text_only"
