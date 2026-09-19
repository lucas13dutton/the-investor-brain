#!/usr/bin/env python3
"""Validate data/evidence/evidence.csv against docs/methodology.md section 8.

Fails (non-zero exit) if any row:
  1. Has a claim_id that duplicates another row's.
  2. Lacks at least one source (source_1 or source_2) with a tier, a quote,
     and an accessed date all filled in.
  3. Is supported only by Tier C source(s), with no labelled-sensitivity
     marker and no approved-exception marker.
  4. Has status "live" with no approved_by value.
  5. Has a last_verified date more than 12 months (365 days) old, missing,
     or unparseable.

Convention for rule 3, since there is no dedicated column for it: write the
word SENSITIVITY (any case) somewhere in claim_text to mark a row as a
labelled sensitivity (per methodology section 3's unsourced-cost sensitivity
rule), or the phrase "EXCEPTION APPROVED" (any case) somewhere in claim_text,
a source name, or calculation_ref to mark an approved Tier-C-only exception.

Usage: python3 data/evidence/validate.py [path/to/evidence.csv]
"""

import csv
import re
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

DEFAULT_CSV_PATH = Path(__file__).resolve().parent / "evidence.csv"

REQUIRED_COLUMNS = [
    "claim_id",
    "claim_text",
    "asset",
    "window",
    "cost_scenario",
    "tax_scenario",
    "value",
    "unit",
    "source_1_name",
    "source_1_tier",
    "source_1_quote",
    "source_1_url",
    "source_1_accessed",
    "source_2_name",
    "source_2_tier",
    "source_2_quote",
    "source_2_url",
    "source_2_accessed",
    "calculation_ref",
    "checked_by",
    "approved_by",
    "status",
    "created",
    "last_verified",
]

MAX_VERIFIED_AGE_DAYS = 365

SENSITIVITY_RE = re.compile(r"SENSITIVITY", re.IGNORECASE)
EXCEPTION_RE = re.compile(r"EXCEPTION APPROVED", re.IGNORECASE)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _clean(value):
    return (value or "").strip()


def _source_complete(row, n):
    """A source is 'complete' for rule 2 if tier, quote and accessed date are all filled."""
    tier = _clean(row.get(f"source_{n}_tier"))
    quote = _clean(row.get(f"source_{n}_quote"))
    accessed = _clean(row.get(f"source_{n}_accessed"))
    return bool(tier and quote and accessed)


def _source_tiers_present(row):
    """Tiers of sources that have at least a tier filled in, for rule 3."""
    tiers = []
    for n in (1, 2):
        tier = _clean(row.get(f"source_{n}_tier")).upper()
        if tier:
            tiers.append(tier)
    return tiers


def _has_sensitivity_or_exception_marker(row):
    haystack = " ".join(
        _clean(row.get(field))
        for field in ("claim_text", "source_1_name", "source_2_name", "calculation_ref")
    )
    return bool(SENSITIVITY_RE.search(haystack) or EXCEPTION_RE.search(haystack))


def _parse_date(raw):
    raw = _clean(raw)
    if not raw or not DATE_RE.match(raw):
        return None
    try:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError:
        return None


def validate_row(row, today=None):
    """Return a list of error strings for a single row. Does not check duplicates."""
    today = today or date.today()
    errors = []

    # Rule 2: at least one complete source.
    if not (_source_complete(row, 1) or _source_complete(row, 2)):
        errors.append(
            "no source has a tier, a quote and an accessed date all filled in "
            "(source_1_* or source_2_*)"
        )

    # Rule 3: Tier C-only without a sensitivity or exception marker.
    tiers = _source_tiers_present(row)
    if tiers and all(t == "C" for t in tiers):
        if not _has_sensitivity_or_exception_marker(row):
            errors.append(
                "supported only by Tier C source(s) with no SENSITIVITY label "
                "and no EXCEPTION APPROVED marker"
            )

    # Rule 4: status "live" needs approved_by.
    status = _clean(row.get("status")).lower()
    if status == "live" and not _clean(row.get("approved_by")):
        errors.append("status is 'live' but approved_by is blank")

    # Rule 5: last_verified within the last 12 months.
    last_verified = _parse_date(row.get("last_verified"))
    if last_verified is None:
        errors.append(
            f"last_verified is missing or not a valid YYYY-MM-DD date: "
            f"{row.get('last_verified')!r}"
        )
    else:
        age_days = (today - last_verified).days
        if age_days > MAX_VERIFIED_AGE_DAYS:
            errors.append(
                f"last_verified is {age_days} days old, more than "
                f"{MAX_VERIFIED_AGE_DAYS} days (12 months)"
            )

    return errors


def validate_rows(rows, today=None):
    """Validate a list of row dicts. Returns a list of (claim_id, [errors]) for failing rows."""
    today = today or date.today()

    # Rule 1: duplicate claim_id, checked across the whole set first.
    ids_seen = defaultdict(list)
    for i, row in enumerate(rows, start=1):
        ids_seen[_clean(row.get("claim_id"))].append(i)

    failures = []
    for i, row in enumerate(rows, start=1):
        claim_id = _clean(row.get("claim_id")) or f"<row {i}, no claim_id>"
        errors = []

        occurrences = ids_seen.get(_clean(row.get("claim_id")), [])
        if len(occurrences) > 1:
            errors.append(
                f"claim_id is duplicated across rows {occurrences} (not unique)"
            )

        errors.extend(validate_row(row, today=today))

        if errors:
            failures.append((claim_id, errors))

    return failures


def load_rows(csv_path):
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing_columns = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing_columns:
            raise ValueError(
                f"evidence.csv is missing required column(s): {', '.join(missing_columns)}"
            )
        return list(reader)


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    csv_path = Path(argv[0]) if argv else DEFAULT_CSV_PATH

    if not csv_path.exists():
        print(f"ERROR: {csv_path} does not exist", file=sys.stderr)
        return 1

    try:
        rows = load_rows(csv_path)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    failures = validate_rows(rows)

    if failures:
        print(f"FAILED: {len(failures)} of {len(rows)} row(s) in {csv_path.name}:\n", file=sys.stderr)
        for claim_id, errors in failures:
            print(f"  {claim_id}:", file=sys.stderr)
            for error in errors:
                print(f"    - {error}", file=sys.stderr)
        return 1

    print(f"OK: {len(rows)} row(s) in {csv_path.name} all pass validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
