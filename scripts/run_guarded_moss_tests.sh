#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPORT_DIR="$ROOT/test_runs"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
REPORT="$REPORT_DIR/guarded_moss_${STAMP}.md"
mkdir -p "$REPORT_DIR"

{
  echo "# Guarded MOSS 2.1 validation"
  echo
  echo "| Field | Value |"
  echo "| --- | --- |"
  printf '| UTC timestamp | `%s` |\n' "$(date -u +%FT%TZ)"
  printf '| Python | `%s` |\n' "$(python3 --version)"
  echo '| Test command | `PYTHONPATH=ribit_2_0 python3 -m unittest tests/test_guarded_moss_2_1.py -v` |'
  echo
  echo "## Package syntax"
  echo
  echo '```text'
  (cd "$ROOT" && python3 -m py_compile ribit_2_0/guarded_moss/*.py)
  echo 'Guarded package compilation passed.'
  echo '```'
  echo
  echo "## Focused unit tests"
  echo
  echo '```text'
  (cd "$ROOT" && PYTHONPATH="$ROOT/ribit_2_0" python3 -m unittest tests/test_guarded_moss_2_1.py -v) 2>&1
  echo '```'
  echo
  echo "## Result"
  echo
  echo 'Guarded MOSS 2.1 local tests passed.'
} > "$REPORT"

cp "$REPORT" "$REPORT_DIR/guarded_moss_latest.md"
printf 'Saved validation report: %s\n' "$REPORT"
