#!/usr/bin/env python3
"""Verify guarded-MOSS committed artifacts and local Markdown link targets."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    Path("ribit_2_0/guarded_moss/__init__.py"),
    Path("scripts/run_guarded_moss_tests.sh"),
    Path("scripts/run_guarded_moss_demo.py"),
    Path("test_runs/guarded_moss_latest.md"),
    Path("test_runs/guarded_moss_ten_turn_demo.md"),
    Path("docs/MOSS_SAFE_2_1_DESIGN.md"),
    Path("docs/MOSS_SAFE_2_1_VALIDATION_AND_DEMO.md"),
    Path("docs/MOSS_SAFE_2_1_ARTIFACT_AUDIT.md"),
)
DOCUMENTS = (
    Path("README.md"),
    Path("docs/MOSS_SAFE_2_1_DESIGN.md"),
    Path("docs/MOSS_SAFE_2_1_VALIDATION_AND_DEMO.md"),
    Path("docs/MOSS_SAFE_2_1_ARTIFACT_AUDIT.md"),
)
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def local_link_targets(document: Path) -> list[Path]:
    targets: list[Path] = []
    for raw_target in MARKDOWN_LINK.findall(document.read_text(encoding="utf-8")):
        target = raw_target.split("#", 1)[0].strip()
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        targets.append((document.parent / target).resolve())
    return targets


def main() -> int:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    broken_links: list[str] = []
    for document in DOCUMENTS:
        source = ROOT / document
        if not source.is_file():
            missing.append(document)
            continue
        for target in local_link_targets(source):
            if not target.exists():
                broken_links.append(f"{document}: {target}")

    if missing or broken_links:
        for path in missing:
            print(f"MISSING: {path}")
        for link in broken_links:
            print(f"BROKEN LINK: {link}")
        return 1

    print(f"OK: {len(REQUIRED)} required artifacts present.")
    print(f"OK: checked local Markdown links in {len(DOCUMENTS)} documents.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
