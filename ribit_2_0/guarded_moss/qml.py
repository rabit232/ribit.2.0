"""Documentation-only QML research notes; no Qt or QML runtime integration."""

from __future__ import annotations

from dataclasses import dataclass

from .limits import MAX_QML_NOTE_CHARS


@dataclass(frozen=True, slots=True)
class QmlResearchNote:
    title: str
    purpose: str
    limitation: str = "Research metadata only; no QML runtime, JavaScript execution, or device integration is provided."


def qml_note(title: str, purpose: str) -> QmlResearchNote:
    if not title.strip() or not purpose.strip() or len(purpose) > MAX_QML_NOTE_CHARS:
        raise ValueError("QML research-note fields are missing or exceed the local bound.")
    return QmlResearchNote(title.strip(), purpose.strip())
