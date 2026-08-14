"""Provenance helpers for review-only input records."""

from __future__ import annotations

import hashlib

from .limits import MAX_EXCERPT_CHARS, MAX_SOURCE_LABEL
from .models import SourceRecord


def digest_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def source_record(source_label: str, normalized_text: str) -> SourceRecord:
    label = source_label.strip()
    if not label or len(label) > MAX_SOURCE_LABEL:
        raise ValueError("Source label is missing or exceeds the allowed length.")
    return SourceRecord(label, digest_text(normalized_text), len(normalized_text), normalized_text[:MAX_EXCERPT_CHARS])
