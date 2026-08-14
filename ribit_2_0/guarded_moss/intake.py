"""Safe data intake for untrusted conversation or file content."""

from __future__ import annotations

from .models import DataRecord
from .normalizer import normalize_text
from .provenance import source_record


class DataIntake:
    """Create review-pending records; this class never activates input."""

    def ingest_text(self, source_label: str, value: str) -> DataRecord:
        normalized = normalize_text(value)
        return DataRecord(source_record(source_label, normalized), normalized)
