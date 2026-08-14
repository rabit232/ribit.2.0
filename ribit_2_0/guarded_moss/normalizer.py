"""Deterministic normalization for untrusted text records."""

from __future__ import annotations

from .limits import MAX_RECORD_CHARS


class NormalizationError(ValueError):
    """Raised when untrusted input cannot fit the local review limits."""


def normalize_text(value: str, *, maximum: int = MAX_RECORD_CHARS) -> str:
    if not isinstance(value, str):
        raise NormalizationError("Input must be text.")
    normalized = value.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        raise NormalizationError("Input must not be blank.")
    if len(normalized) > maximum:
        raise NormalizationError("Input exceeds the review size limit.")
    return normalized
