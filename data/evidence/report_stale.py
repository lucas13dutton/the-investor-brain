#!/usr/bin/env python3
"""Report evidence-log entries whose last_verified date is stale.

Stale means missing, unparseable, or more than 12 months (365 days) old —
the same threshold validate.py enforces as a hard failure. This script is
for the weekly scheduled report: it always lists every stale entry, and
exits non-zero if any are found so the workflow run itself flags it.

Usage: python3 data/evidence/report_stale.py [path/to/evidence.csv]
"""

import os
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate  # noqa: E402

DEFAULT_CSV_PATH = Path(__file__).resolve().parent / "evidence.csv"


def find_stale(rows, today=None):
    today = today or date.today()
    stale = []
    for row in rows:
        claim_id = validate._clean(row.get("claim_id")) or "<no claim_id>"
        last_verified = validate._parse_date(row.get("last_verified"))
        if last_verified is None:
            stale.append((claim_id, row.get("last_verified"), None))
        else:
            age_days = (today - last_verified).days
            if age_days > validate.MAX_VERIFIED_AGE_DAYS:
                stale.append((claim_id, row.get("last_verified"), age_days))
    return stale


def format_report(stale, total_rows, today):
    lines = []
    if not stale:
        lines.append(f"OK: all {total_rows} row(s) have a last_verified date within the last 12 months, as of {today.isoformat()}.")
        return "\n".join(lines)

    lines.append(f"STALE: {len(stale)} of {total_rows} row(s) have a last_verified date more than 12 months old or missing, as of {today.isoformat()}:\n")
    for claim_id, raw_date, age_days in stale:
        if age_days is None:
            lines.append(f"  - {claim_id}: last_verified is missing or invalid ({raw_date!r})")
        else:
            lines.append(f"  - {claim_id}: last_verified {raw_date} is {age_days} days old")
    return "\n".join(lines)


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    csv_path = Path(argv[0]) if argv else DEFAULT_CSV_PATH
    today = date.today()

    if not csv_path.exists():
        print(f"ERROR: {csv_path} does not exist", file=sys.stderr)
        return 1

    try:
        rows = validate.load_rows(csv_path)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    stale = find_stale(rows, today=today)
    report = format_report(stale, len(rows), today)
    print(report)

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write("## Evidence log staleness report\n\n")
            f.write(f"```\n{report}\n```\n")

    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
