#!/usr/bin/env python3
"""Validate data/evidence/evidence.csv against docs/methodology.md section 8.

Fails (non-zero exit) if any row:
  1. Lacks a source with a tier (A/B/C) and an access date.
  2. Is supported only by Tier C source(s) with no approved exception flag.
  3. Has a published status ("live" or "corrected") but no approved_by.

Usage: python3 data/evidence/validate.py
"""

import csv
import re
import sys
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent / "evidence.csv"

REQUIRED_COLUMNS = [
    "claim_id",
    "claim",
    "asset",
    "window",
    "cost_scenario",
    "tax_scenario",
    "sources",
    "calculation_ref",
    "checked_by",
    "approved_by",
    "published_in",
    "status",
]

PUBLISHED_STATUSES = {"live", "corrected"}

SOURCE_SPLIT_RE = re.compile(r"\s;\s")
TIER_RE = re.compile(r"Tier\s*([ABC])", re.IGNORECASE)
DATE_RE = re.compile(r"accessed\s*(\d{4}-\d{2}-\d{2})", re.IGNORECASE)
EXCEPTION_RE = re.compile(r"EXCEPTION APPROVED", re.IGNORECASE)


def parse_sources(raw):
    """Split a sources cell into individual source entries."""
    raw = (raw or "").strip()
    if not raw:
        return []
    return [s.strip() for s in SOURCE_SPLIT_RE.split(raw) if s.strip()]


def validate_row(row, line_no):
    errors = []
    claim_id = row.get("claim_id", "").strip() or f"<row {line_no}, no claim_id>"

    sources = parse_sources(row.get("sources", ""))
    if not sources:
        errors.append("no sources given")
    else:
        tiers = []
        for entry in sources:
            tier_match = TIER_RE.search(entry)
            date_match = DATE_RE.search(entry)
            if not tier_match:
                errors.append(f"source missing a tier (A/B/C): {entry!r}")
            else:
                tiers.append(tier_match.group(1).upper())
            if not date_match:
                errors.append(f"source missing an access date: {entry!r}")

        if tiers and all(t == "C" for t in tiers):
            if not EXCEPTION_RE.search(row.get("sources", "")):
                errors.append(
                    "supported only by Tier C source(s) with no 'EXCEPTION APPROVED' flag"
                )

    status = (row.get("status", "") or "").strip().lower()
    if status in PUBLISHED_STATUSES and not (row.get("approved_by", "") or "").strip():
        errors.append(f"status is '{status}' but approved_by is blank")

    return claim_id, errors


def main():
    if not CSV_PATH.exists():
        print(f"ERROR: {CSV_PATH} does not exist", file=sys.stderr)
        return 1

    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        missing_columns = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing_columns:
            print(
                f"ERROR: evidence.csv is missing required column(s): {', '.join(missing_columns)}",
                file=sys.stderr,
            )
            return 1

        failures = []
        row_count = 0
        for line_no, row in enumerate(reader, start=2):  # header is line 1
            row_count += 1
            claim_id, errors = validate_row(row, line_no)
            if errors:
                failures.append((claim_id, errors))

    if failures:
        print(f"FAILED: {len(failures)} of {row_count} row(s) in evidence.csv:\n", file=sys.stderr)
        for claim_id, errors in failures:
            print(f"  {claim_id}:", file=sys.stderr)
            for error in errors:
                print(f"    - {error}", file=sys.stderr)
        return 1

    print(f"OK: {row_count} row(s) in evidence.csv all pass validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
