#!/usr/bin/env python3
"""Report evidence-log entries whose last_verified date is stale, and refresh
the open research queue.

Stale means missing, unparseable, or more than 12 months (365 days) old —
the same threshold validate.py enforces as a hard failure. This script is
for the weekly scheduled report: it always lists every stale entry, and
exits non-zero if any are found so the workflow run itself flags it.

It also regenerates the auto-generated block in docs/open-research-queue.md
(everything between the BEGIN/END AUTO-GENERATED markers) with the current
list of rows flagged NEEDS RE-VERIFICATION, grouped by publisher, and flags
any withdrawn-with-no-replacement row that isn't already mentioned somewhere
on that page, so a new gap never falls through silently even though the
hand-authored "what's needed"/"owner" detail for each item stays untouched.

Usage: python3 data/evidence/report_stale.py [path/to/evidence.csv]
"""

import os
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate  # noqa: E402

DEFAULT_CSV_PATH = Path(__file__).resolve().parent / "evidence.csv"
DEFAULT_QUEUE_PATH = Path(__file__).resolve().parents[2] / "docs" / "open-research-queue.md"

AUTO_BEGIN = "<!-- BEGIN AUTO-GENERATED -->"
AUTO_END = "<!-- END AUTO-GENERATED -->"


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


def _publisher_key(name):
    m = re.match(r"^([A-Za-z0-9&' .]+)", name or "")
    return (m.group(1).strip() if m else (name or "unknown"))[:40] or "unknown"


def build_flagged_table(rows):
    flagged = [r for r in rows if validate.needs_reverification(r)]
    groups = defaultdict(list)
    for r in flagged:
        groups[(r.get("asset", ""), _publisher_key(r.get("source_1_name", "")))].append(
            r["claim_id"]
        )

    lines = [f"_Last regenerated {date.today().isoformat()}. {len(flagged)} row(s) flagged._", ""]
    if not flagged:
        lines.append("None currently flagged.")
        return "\n".join(lines)

    lines.append("| Asset | Publisher | Rows |")
    lines.append("|---|---|---|")
    for (asset, publisher), ids in sorted(groups.items()):
        lines.append(f"| {asset} | {publisher} | {', '.join(sorted(ids))} |")
    return "\n".join(lines)


def find_unlisted_withdrawn(rows, queue_text):
    """Withdrawn-with-no-replacement claim_ids not mentioned anywhere in the queue file."""
    unlisted = []
    for r in rows:
        if r.get("row_type") != "withdrawn":
            continue
        if validate.replacement_id(r):
            continue
        if r["claim_id"] not in queue_text:
            unlisted.append(r["claim_id"])
    return unlisted


def update_open_research_queue(rows, queue_path):
    """Regenerate the auto-generated block in the queue file. Returns True if the file changed."""
    if not queue_path.exists():
        return False

    original_text = queue_path.read_text(encoding="utf-8")

    if original_text.count(AUTO_BEGIN) != 1 or original_text.count(AUTO_END) != 1:
        print(
            f"ERROR: {queue_path} must contain exactly one {AUTO_BEGIN!r} and one "
            f"{AUTO_END!r} marker (found {original_text.count(AUTO_BEGIN)} and "
            f"{original_text.count(AUTO_END)}) — refusing to touch it rather than guess "
            f"which pair delimits the real block. Check for an incidental mention of the "
            f"marker text elsewhere on the page.",
            file=sys.stderr,
        )
        return False

    unlisted = find_unlisted_withdrawn(rows, original_text)
    flagged_table = build_flagged_table(rows)

    new_block_lines = [AUTO_BEGIN, flagged_table]
    if unlisted:
        new_block_lines.append("")
        new_block_lines.append(
            f"⚠️ **{len(unlisted)} withdrawn row(s) with no replacement are not yet listed "
            f"above and need a manual entry:** {', '.join(sorted(unlisted))}"
        )
    new_block_lines.append(AUTO_END)
    new_block = "\n".join(new_block_lines)

    pattern = re.compile(re.escape(AUTO_BEGIN) + r".*?" + re.escape(AUTO_END), re.DOTALL)
    new_text = pattern.sub(lambda _match: new_block, original_text, count=1)

    if new_text != original_text:
        queue_path.write_text(new_text, encoding="utf-8")
        return True
    return False


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

    queue_path = DEFAULT_QUEUE_PATH
    queue_updated = update_open_research_queue(rows, queue_path)
    if queue_updated:
        print(f"\nUpdated {queue_path} with the current flagged-row list.")
    elif queue_path.exists():
        print(f"\n{queue_path} already up to date.")
    else:
        print(f"\nNOTE: {queue_path} does not exist — nothing to update.", file=sys.stderr)

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write("## Evidence log staleness report\n\n")
            f.write(f"```\n{report}\n```\n")
            f.write(f"\nOpen research queue {'updated' if queue_updated else 'unchanged'}: `{queue_path}`\n")

    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
