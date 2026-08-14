"""Bounded JSON audit ledger for review-only events."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from .limits import MAX_LEDGER_EVENTS


@dataclass(frozen=True, slots=True)
class LedgerEvent:
    event_type: str
    subject_id: str
    timestamp_utc: str
    detail: str


def append_event(path: str | Path, *, event_type: str, subject_id: str, detail: str) -> LedgerEvent:
    destination = Path(path).expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    event = LedgerEvent(event_type[:80], subject_id[:80], datetime.now(timezone.utc).isoformat(), detail[:500])
    try:
        existing = json.loads(destination.read_text(encoding="utf-8")) if destination.exists() else []
    except json.JSONDecodeError:
        existing = []
    if not isinstance(existing, list):
        existing = []
    existing.append(asdict(event))
    destination.write_text(json.dumps(existing[-MAX_LEDGER_EVENTS:], indent=2) + "\n", encoding="utf-8")
    return event
