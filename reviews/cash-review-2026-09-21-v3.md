# Skeptic review: Cash dossier (round 3, final)

**Reviewed:** `dossiers/cash.md` against the two Critical/Major findings from round 2 (`reviews/cash-review-2026-09-21-v2.md`), which the orchestrating session reported fixing.
**Reviewer:** skeptic agent · **Date:** 2026-09-21

---

## Verdict: **Pass**

This was a narrow, final check of the two round-2 blockers plus one carried-over cosmetic item. All three are confirmed fixed; no new issues found on a final scan.

## Findings

### 1. [Resolved] Stale "Tier B" reference in section 5

Line 148 (NS&I product pages row) now reads: `C (see corrected tier reasoning, section 1; each claim carries an EXCEPTION APPROVED marker)`. Grepped the whole file for "Tier B": the only two remaining hits are in section 1 (correctly describing the superseded old reasoning as historical context) and the Confidence section (correctly stating "not Tier B, as first drafted"). No unqualified "B" tier assertion remains anywhere.

### 2. [Resolved] CASH-0032 and CASH-0033 quotes now verbatim

Independently re-fetched both pages myself this round:
- `nsandi.com/products/guaranteed-growth-bonds` states: "If you change your mind after you invest, you can cancel within 30 days of receiving confirmation of your Bond." The evidence.csv row for CASH-0032 now has `source_1_quote` = "you can cancel within 30 days of receiving confirmation of your Bond" — an exact substring match. Confirmed.
- `nsandi.com/products/premium-bonds` states: "Prizes range from £25 to £1 million and are all tax-free." The evidence.csv row for CASH-0033 now has `source_1_quote` = "Prizes range from £25 to £1 million and are all tax-free" — exact match, fabricated "up" removed. Confirmed.

### 3. [Resolved] CASH-0026 double-bracket

Section 2 now reads "in £25 [CASH-0025] units up to a £50,000 [CASH-0026] per-person maximum." — single bracket. Grepped the file for repeated adjacent same-ID brackets and duplicate-ID patterns; found none. (The adjacent `[CASH-0014][CASH-0015]` and `[CASH-0017][CASH-0018]` pairs in section 5 are two distinct claim IDs cited together, not duplicates — not an issue.)

### 4. Final scan

Read the full dossier top to bottom. No other stray brackets, no other unverified-looking quotes introduced by this round's edits, no new unbracketed numbers spotted. The one still-open minor item from round 2 (CASH-0034's 1.45pp rounding to "1.4" rather than "1.5") was left as-is per instruction — it remains non-blocking and is not re-raised here.

---

## What I couldn't check

- Did not re-verify rows untouched by this round's fixes (all previously confirmed across rounds 1–2); re-checking them again would be outside this round's narrow scope.
- No `validate.py` run (no Bash access this session) — relied on direct grep/read against `data/evidence/evidence.csv` and `data/evidence/README.md` rules for the three specific rows in question, as in prior rounds.

## Recommendation

Ready to publish as draft. No further round needed.
