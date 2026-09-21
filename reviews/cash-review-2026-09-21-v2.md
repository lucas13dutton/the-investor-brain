# Skeptic review: Cash dossier (round 2)

**Reviewed:** `dossiers/cash.md` (draft v1, 2026-09-21) against `docs/methodology.md` (v0.9), `docs/house-rules.md` (v0.1), `data/evidence/evidence.csv` (CASH-0001–CASH-0035), and `data/evidence/README.md`, following the fixes applied after round 1 (`reviews/cash-review-2026-09-21-v1.md`) and Lucas's ruling downgrading NS&I to Tier C.
**Reviewer:** skeptic agent · **Date:** 2026-09-21

---

## Verdict: **Fix**

Round 1's two Critical findings are mostly closed cleanly: the six previously-unbracketed numbers are now logged and bracketed, CASH-0022's gap is now a proper `withdrawn` row, the 8.75pp compounded figure is correct and shown alongside the 9.7pp simple-subtraction figure, and the NS&I Tier C downgrade was applied to all 8 originally-affected rows plus the new rows this round, each carrying the required `EXCEPTION APPROVED` marker where needed and none where not needed.

But this round introduces two new problems that block Pass:

1. **A stray, uncorrected "Tier B" reference to NS&I survives in the dossier text** (section 5), directly contradicting the settled ruling stated one paragraph away in section 1 and in the Confidence section.
2. **Two of the five newly-added evidence rows (CASH-0032, CASH-0033) contain quotes that are not verbatim from the source they cite** — a genuine methodology §7.3 violation, and ironically introduced in the very fix meant to close the "unlogged number" finding. I independently re-fetched both NS&I pages just now and confirmed the real wording differs from what's recorded in the evidence log.

Neither is a research-quality problem (the underlying facts are all still correct) — both are drafting/QA slips in the fix itself. Both are quick to fix, but per the house rule "a single unverifiable [or, here, inaccurately-quoted] number is enough to block," and given methodology §7.3's explicit requirement that a citation quote the exact wording, this can't be waved through as Pass.

---

## Findings

### 1. [Major] Stale "Tier B" reference to NS&I survives in section 5's Price data sources table

Line 148 (the "NS&I product pages" row of the section 5 table):

> `| **NS&I product pages** (Premium Bonds, Guaranteed Growth Bonds) | NS&I | B (see tier reasoning, section 1) | Publicly viewable; ...`

This directly contradicts:
- Section 1's tier-reasoning paragraph: "**NS&I is therefore treated as Tier C throughout this dossier**..."
- The Confidence section: "...rests on Tier C (not Tier B, as first drafted)..."
- Section 9's Sources list: "**NS&I** — ... Tier C, see corrected reasoning in section 1..."

I grepped the whole dossier for "Tier B" / NS&I-adjacent "B" references and found exactly three hits: section 1 (correctly describing the *old*, now-superseded reasoning as context), the Confidence section (correctly stating the *corrected* position), and this one — the only place where "B" is asserted as the dossier's *current* tier for NS&I, unqualified, in a table a reader could reasonably treat as the authoritative summary of source tiers.

**Fix:** change "B (see tier reasoning, section 1)" to "C (see tier reasoning, section 1)" in the section 5 table.

### 2. [Critical] Two new evidence rows added this round contain quotes that are not verbatim from the cited source

Methodology §7.3: "Every citation must quote the exact sentence or clause being relied on, taken from the page." The README repeats this for `claim` rows: "a real quote, not a description of why one couldn't be found."

I independently re-fetched both pages just now (2026-09-21) to check:

**CASH-0032** (`source_1_quote`): `"You have a 30 day cooling off period"`

NS&I's Guaranteed Growth Bonds page actually states: **"If you change your mind after you invest, you can cancel within 30 days of receiving confirmation of your Bond."** This is not a truncation or a clause taken from that sentence — it is a different sentence structure entirely, not present anywhere on the page in that form. Notably, the round-1 review (`reviews/cash-review-2026-09-21-v1.md`, finding 1 item 4) had already independently fetched and quoted the *correct* wording ("you can cancel within 30 days of receiving confirmation of your Bond") — whoever added this row in the fix did not carry that already-verified quote over, and wrote a fresh, inaccurate paraphrase instead.

**CASH-0033** (`source_1_quote`): `"prizes range from £25 up to £1 million"`

NS&I's Premium Bonds page actually states: **"Prizes range from £25 to £1 million and are all tax-free."** The evidence-log quote inserts the word "up" (making it "up to £1 million") which does not appear on the page — a small but real fabrication of wording. Here too, round 1's own finding (item 6) had already independently confirmed the correct quote ("Prizes range from £25 to £1 million and are all tax-free") — the row added this round doesn't match even that.

By contrast, **CASH-0031** (Personal Allowance) checks out: its quote, "The standard Personal Allowance is £12,570," is a genuine truncation (at a comma) of the real sentence I confirmed by direct fetch just now ("The standard Personal Allowance is £12,570, which is the amount of income you do not have to pay tax on.") — a legitimate partial clause, not an alteration, consistent with how other rows in this log truncate at natural breaks (e.g. "Basic rate: £1,000"). CASH-0031 is fine as-is.

**Fix:** correct `source_1_quote` for CASH-0032 to the real wording ("you can cancel within 30 days of receiving confirmation of your Bond" or the full sentence it sits in), and for CASH-0033 to the real wording ("Prizes range from £25 to £1 million and are all tax-free," or a clean clause of it, e.g. "Prizes range from £25 to £1 million"). Since the underlying facts (30-day window, £1m top prize) are correct and already independently confirmed twice now (round 1 and this round), this is a pure text fix to the evidence row, not a re-research task.

### 3. [Minor, carried over from round 1, not required to fix, still present] Redundant double-bracketing

Section 2: "in £25 [CASH-0025] units up to a £50,000 [CASH-0026] per-person maximum [CASH-0026]" — CASH-0026 is bracketed twice in the same clause. Round 1 flagged this as cosmetic and non-blocking; it remains unfixed. Still not blocking, but worth a copyedit pass whenever this dossier is next touched.

### 4. [Minor] "1.4 percentage points" (CASH-0034) rounds a genuine midpoint (1.45) down, without flagging that it's a midpoint

3.1% (CASH-0016) − 1.65% (CASH-0014) = 1.45 percentage points exactly. Standard "round half up" gives 1.5, not 1.4 (round-half-to-even gives 1.4). The evidence row states "1.4 percentage points (rounded)" without noting this is a midpoint value where the rounding convention matters. Round 1 flagged the same arithmetic as "trivial, not worth blocking," and I agree it isn't blocking — but since a new evidence row (CASH-0034) was created this round that restates this exact rounding as settled ("= 1.4 percentage points (rounded)"), it would have been a good opportunity to either round to 1.5 or note the midpoint explicitly. Not required before publication, but flagged since it's now baked into a citable row rather than just dossier prose.

### 5. What I verified this round and it checked out cleanly

- **All 8 originally-flagged NS&I rows** (CASH-0001, 0002, 0003, 0020, 0021, 0025, 0026, 0027) now show `source_1_tier` (and `source_2_tier` for CASH-0021) as `C`, each with the `EXCEPTION APPROVED by Lucas, 2026-09-21` marker present in `calculation_ref`, exactly as Lucas ruled.
- **CASH-0022** is now a proper `withdrawn` row, correctly naming its replacement ("replaced by CASH-0021, which carries this same fact as a second source") — CASH-0021 is a real, existing row, satisfying the README's rule that a named replacement must be real.
- **All six previously-unbracketed numbers from round 1's finding 1** are now logged and bracketed in the dossier text: the two "Gap" percentage-point figures (§3.2, now CASH-0034/CASH-0035), the £12,570 Personal Allowance (§4.1, CASH-0031), the 30-day cooling-off window (§3.3, CASH-0032 — see Finding 2 above on its quote accuracy), the £1m top prize (§1, CASH-0033 — see Finding 2), and the unsourced easy-access withdrawal timing (§3.5) was reworded to remove the specific "1–2 business days" figure entirely rather than inventing a source, which is the correct move per the unsourced-cost rule (a qualitative statement, not a bare number, needs no evidence row).
- **The compounded-vs-simple arithmetic (Finding 4, round 1) is correct.** I hand-computed (1+0.0083)/(1+0.105)−1 independently: 1.0083 ÷ 1.105 ≈ 0.912489, so the result is −0.08751, i.e. **−8.75 percentage points**, matching the dossier's and CASH-0035's stated figure exactly. The dossier's note ("simple subtraction gives 9.7 percentage points, while the compounded formula gives 8.75 percentage points") does not overstate or understate this — it's accurate and appropriately labelled as a real difference "at that inflation level, though a small one at the 1.4-point central scenario."
- **CASH-0034 and CASH-0035 are correctly typed `structural`** (a calculated figure with no independent external source), correctly carry no tier (tier is not applicable to `structural` rows per the README), and correctly carry no `EXCEPTION APPROVED` marker (none is needed, since no Tier-C-sole-support claim is being made by a derived, disclosed-as-a-calculation figure).
- **CASH-0031 is correctly Tier A with no exception marker** — appropriate, since gov.uk needs no exception.
- No other stray "Tier B" reference to NS&I exists anywhere else in the dossier text (I grepped the whole file; the only three hits are the two correct historical/corrected references in section 1 and Confidence, and the one uncorrected instance in Finding 1 above).
- **Full read-through found no other newly-introduced unbracketed number.** The one repeated, unbracketed second mention of "£1 million" in section 6 ("a very small number win very large prizes, up to £1 million") is a repeat of an already-cited fact (CASH-0033, cited on its first appearance in section 1) rather than a fresh, unlogged claim — this matches the dossier's existing convention elsewhere (e.g. the Confidence section restates "1.65% vs 3.1%" and "0.83% vs 10.5%" without rebracketing already-cited figures), a convention round 1 implicitly accepted by not flagging those instances. I am not blocking on this, but note it for consistency's sake only.

---

## What I couldn't check

- **`validate.py` itself** — no Bash access this session either. I checked the specific rows named in this round's brief (CASH-0001–0035, all NS&I-tagged rows, the withdrawn/structural rows) by hand against `data/evidence/README.md`'s rules rather than running the script, as instructed.
- **Whether the orchestrating session's prior validator run** (reported as "263 rows all pass") would have caught the two inaccurate quotes in Finding 2 — I doubt it would, since nothing in the validator's documented rule set (per the README's "Running the validator" section) checks quote *accuracy* against the live source, only quote *presence* and that it isn't a "description of why one couldn't be found." A wrong-but-present quote passes mechanically; only a human re-fetch catches it, which is what I did.
- I did not re-fetch every other unaffected CASH row a third time (FSCS, ONS, BoE, gov.uk tax pages) since round 1 already fetched and confirmed all of these verbatim and none of them were touched by this round's fixes; re-checking untouched, already-verified rows a second time would not have been a good use of this round's scope.

---

## Recommendation

Fix, then a third and hopefully final round. Both new findings are small, mechanical text edits to `dossiers/cash.md` (one word: B→C) and `data/evidence/evidence.csv` (two `source_1_quote` fields corrected to match wording already independently verified twice over, in round 1 and again here) — no new research is needed, and the correct wording for both quotes is already sitting in `reviews/cash-review-2026-09-21-v1.md` and in this review. This should be a fast, final pass to close out.
