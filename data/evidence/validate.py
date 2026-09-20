#!/usr/bin/env python3
"""Validate data/evidence/evidence.csv against docs/methodology.md section 8.

Every row has a row_type: "claim" (default), "structural", "sensitivity", or
"withdrawn". Only "claim" rows are held to the full sourcing rule. The other
three each get a narrower rule of their own.

Fails (non-zero exit) if any row breaks its type's rule:

  Every row, regardless of type:
    1. Has a claim_id that duplicates another row's.
    4. Has status "live" with no approved_by value.
    5. Has a last_verified date more than 12 months (365 days) old, missing,
       or unparseable.

  row_type "claim" only:
    2. Lacks at least one source (source_1 or source_2) with a tier, a quote,
       and an accessed date all filled in.
    3. Is supported only by Tier C source(s), with no approved-exception
       marker ("EXCEPTION APPROVED", any case, in claim_text, a source name,
       or calculation_ref).
    6. A used source's quote contains a phrase indicating no real quote was
       ever found ("no verbatim", "no quotable", "not captured", "no single
       verbatim", "no source found", "no current source" — case-insensitive).
       A "claim" row asserting a fact needs a real quote, not a description
       of why one couldn't be found — reclassify or withdraw instead.
    7. A used source's URL doesn't start with "http" (case-insensitive).
       A source with no real URL isn't a source a reader can go check.

  row_type "structural" (a fact with no source, e.g. "home storage costs
  nothing"): no sourcing rule at all — value/unit and claim_text still apply
  as normal, but source_1_*/source_2_* and their quote/URL rules are skipped.

  row_type "sensitivity" (published as a labelled range/bound under
  methodology section 3's unsourced-cost sensitivity rule):
    8. value and unit must both be filled in (the row must actually state
       its bound).
    9. No source attribution at all — every source_1_*/source_2_* field must
       be blank. A sensitivity row is an assumption, not an evidenced fact;
       giving it a source manufactures a paper trail for something that
       isn't actually sourced.

  row_type "withdrawn" (a figure known to be wrong or superseded):
    10. If calculation_ref or claim_text names a replacement via the pattern
        "replaced by <CLAIM-ID>", that claim_id must actually exist in the
        file. Naming a replacement is optional ("where one exists") — this
        only checks a named one isn't dangling.

Usage: python3 data/evidence/validate.py [path/to/evidence.csv]
"""

import csv
import re
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

DEFAULT_CSV_PATH = Path(__file__).resolve().parent / "evidence.csv"

REQUIRED_COLUMNS = [
    "claim_id",
    "row_type",
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

VALID_ROW_TYPES = {"claim", "structural", "sensitivity", "withdrawn"}

MAX_VERIFIED_AGE_DAYS = 365

EXCEPTION_RE = re.compile(r"EXCEPTION APPROVED", re.IGNORECASE)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REPLACED_BY_RE = re.compile(r"replaced by\s+([A-Z]+-\d{4})", re.IGNORECASE)

NO_REAL_QUOTE_PHRASES = [
    "no verbatim",
    "no quotable",
    "not captured",
    "no single verbatim",
    "no source found",
    "no current source",
]


def _clean(value):
    return (value or "").strip()


def _row_type(row):
    rt = _clean(row.get("row_type")).lower() or "claim"
    return rt


def _source_complete(row, n):
    """A source is 'complete' for rule 2 if tier, quote and accessed date are all filled."""
    tier = _clean(row.get(f"source_{n}_tier"))
    quote = _clean(row.get(f"source_{n}_quote"))
    accessed = _clean(row.get(f"source_{n}_accessed"))
    return bool(tier and quote and accessed)


def _source_any_field(row, n):
    return any(
        _clean(row.get(f"source_{n}_{field}"))
        for field in ("name", "tier", "quote", "url", "accessed")
    )


def _used_sources(row):
    """Indices (1, 2) of sources that are actually populated (have a tier)."""
    return [n for n in (1, 2) if _clean(row.get(f"source_{n}_tier"))]


def _source_tiers_present(row):
    tiers = []
    for n in (1, 2):
        tier = _clean(row.get(f"source_{n}_tier")).upper()
        if tier:
            tiers.append(tier)
    return tiers


def _has_exception_marker(row):
    haystack = " ".join(
        _clean(row.get(field))
        for field in ("claim_text", "source_1_name", "source_2_name", "calculation_ref")
    )
    return bool(EXCEPTION_RE.search(haystack))


def _quote_lacks_real_content(quote):
    lowered = quote.lower()
    return any(phrase in lowered for phrase in NO_REAL_QUOTE_PHRASES)


def _parse_date(raw):
    raw = _clean(raw)
    if not raw or not DATE_RE.match(raw):
        return None
    try:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError:
        return None


def _validate_claim_row(row):
    errors = []

    if not (_source_complete(row, 1) or _source_complete(row, 2)):
        errors.append(
            "no source has a tier, a quote and an accessed date all filled in "
            "(source_1_* or source_2_*)"
        )
        return errors  # rules 3/6/7 need a complete source to check against

    tiers = _source_tiers_present(row)
    if tiers and all(t == "C" for t in tiers):
        if not _has_exception_marker(row):
            errors.append(
                "supported only by Tier C source(s) with no EXCEPTION APPROVED marker"
            )

    for n in _used_sources(row):
        quote = _clean(row.get(f"source_{n}_quote"))
        if quote and _quote_lacks_real_content(quote):
            errors.append(
                f"source_{n}_quote describes an absent quote rather than containing "
                f"a real one: {quote!r}"
            )
        url = _clean(row.get(f"source_{n}_url"))
        if url and not url.lower().startswith("http"):
            errors.append(f"source_{n}_url does not start with 'http': {url!r}")
        elif not url:
            errors.append(f"source_{n}_url is blank (needs a URL starting with 'http')")

    return errors


def _validate_structural_row(row):
    # No sourcing rule at all. Nothing to check here beyond the universal rules.
    return []


def _validate_sensitivity_row(row):
    errors = []
    if not (_clean(row.get("value")) and _clean(row.get("unit"))):
        errors.append("sensitivity row must state its bound in both value and unit")
    for n in (1, 2):
        if _source_any_field(row, n):
            errors.append(
                f"sensitivity row must carry no source attribution, but source_{n}_* is populated"
            )
    return errors


def _validate_withdrawn_row(row, known_ids):
    errors = []
    haystack = " ".join(_clean(row.get(field)) for field in ("claim_text", "calculation_ref"))
    m = REPLACED_BY_RE.search(haystack)
    if m:
        replacement_id = m.group(1).upper()
        if replacement_id not in known_ids:
            errors.append(
                f"names a replacing claim_id, {replacement_id!r}, that does not exist in this file"
            )
    return errors


def validate_row(row, today=None, known_ids=None):
    """Return a list of error strings for a single row. Does not check duplicates."""
    today = today or date.today()
    known_ids = known_ids or set()
    errors = []

    row_type = _row_type(row)
    if row_type not in VALID_ROW_TYPES:
        errors.append(
            f"row_type {row_type!r} is not one of {sorted(VALID_ROW_TYPES)}"
        )
        row_type = "claim"  # fall back to the strictest rule for the rest of the checks

    if row_type == "claim":
        errors.extend(_validate_claim_row(row))
    elif row_type == "structural":
        errors.extend(_validate_structural_row(row))
    elif row_type == "sensitivity":
        errors.extend(_validate_sensitivity_row(row))
    elif row_type == "withdrawn":
        errors.extend(_validate_withdrawn_row(row, known_ids))

    # Universal rule: status "live" needs approved_by.
    status = _clean(row.get("status")).lower()
    if status == "live" and not _clean(row.get("approved_by")):
        errors.append("status is 'live' but approved_by is blank")

    # Universal rule: last_verified within the last 12 months.
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

    ids_seen = defaultdict(list)
    for i, row in enumerate(rows, start=1):
        ids_seen[_clean(row.get("claim_id"))].append(i)
    known_ids = set(ids_seen.keys())

    failures = []
    for i, row in enumerate(rows, start=1):
        claim_id = _clean(row.get("claim_id")) or f"<row {i}, no claim_id>"
        errors = []

        occurrences = ids_seen.get(_clean(row.get("claim_id")), [])
        if len(occurrences) > 1:
            errors.append(
                f"claim_id is duplicated across rows {occurrences} (not unique)"
            )

        errors.extend(validate_row(row, today=today, known_ids=known_ids))

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
