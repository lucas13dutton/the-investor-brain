# Skeptic review: UK buy-to-let property dossier (round 3, final)

**Reviewed:** `dossiers/uk-property.md` · **Date:** 2026-09-21 · **Reviewer:** skeptic agent
**Scope (per brief):** narrow, final pass — confirm the round-2 quote-mark fix, confirm PROP-0055/"circa 95%" are gone from the dossier, confirm §3.5/§5/§9 still read sensibly, confirm PROP-0055's withdrawn row is correctly formatted, and one last quick scan.

---

## Verdict: **Fix**

Four of five checks pass cleanly. But "circa 95%" is **not** actually gone from the dossier text — it survives, unbracketed, in §9's Tier C sources note. That's a small, one-line fix, not a re-litigation of anything.

---

## Findings

### 1. [Minor] "circa 95%" still appears in §9, quoted but unbracketed

Line 190 (§9, "Tier C (background only, not cited for a specific figure)"):

> Rightmove House Price Index press page and Rightmove landlord guides — fetched directly 2026-09-21; confirms the index is asking-price-based (built on newly-marketed listings, not completed sales) and carries no time-to-sell metric; **the specific "circa 95%" coverage figure quoted on Rightmove's own press page is not cited here as a claim**, since it is Rightmove's own unverified claim about its own market coverage with no Tier A/B alternative, and is not load-bearing for the asking-price-vs-sale-price point this dossier actually needs; several individual guide pages returned access errors and yielded no usable figure

This is explanatory prose about a research decision (why a number was found and excluded), not an assertion of fact about the world, and it explicitly disclaims the figure — so it's a different situation from a live, relied-upon claim, and I don't think it's misleading a reader. But it does mean the task's own success criterion ("grep for … 'circa 95%' — both should be gone from the dossier text") is not actually met, and it leaves a specific number sitting in published text with no bracketed claim ID, which is the exact pattern the evidence-log rule exists to prevent — a future editor skimming this file could plausibly copy this number into a headline sentence later, unaware it was only ever mentioned to be rejected.

**Fix:** drop the literal number from this sentence too, e.g. "...confirms the index is asking-price-based … and carries no time-to-sell metric; Rightmove's own press page also states a market-coverage percentage, which is not cited here as it is an unverified, Tier-C-only claim about the portal's own coverage and not load-bearing for this dossier's point..." — same meaning, no bare number left unbracketed. One sentence, no other changes needed.

---

## Verification of the specific items in the brief

1. **Quote-mark fix (§5 UKHPI row):** Confirmed correct. Line 115 now reads `**"A joint production by HM Land Registry, Land and Property Services Northern Ireland, Office for National Statistics and Registers of Scotland"** [PROP-0047]` — properly opened and closed, and I checked it against `PROP-0047`'s logged `source_1_quote` in `data/evidence/evidence.csv`: exact verbatim match.

2. **PROP-0055 / "circa 95%" removed:** `PROP-0055` — confirmed zero occurrences anywhere in `dossiers/uk-property.md` (full-file grep, no matches). `circa 95%` — **not fully removed**, see Finding 1 above. `PROP-0055` itself still exists in `evidence.csv` as `row_type: withdrawn`, which is correct and expected.

3. **§3.5, §5, §9 read sensibly:** §3.5 (line 80) and §5 (line 116) are both now clean qualitative statements ("built on newly-marketed listings — i.e. asking prices... not completed sales", "This is an asking-price index, built on newly-marketed listings — not a sale-price index") that make the substantive point clearly with no unsourced percentage. §9 makes the same point but, per Finding 1, still names the specific number it's declining to use.

4. **PROP-0055's withdrawn row format:** Checked against `data/evidence/README.md`'s row-type rules and directly against the file's own established precedent, `CASH-0022` (also `withdrawn`, also closing a prior skeptic finding). Field-for-field, the blank pattern is identical: `value`/`unit`/all `source_1_*`/`source_2_*` fields blank, `window`/`cost_scenario`/`tax_scenario` all `n/a`, `calculation_ref` explains no replacement is needed rather than falsely naming one, `status: draft`, dated. I also checked `validate.py`'s `_validate_withdrawn_row` and `replacement_id`/`REPLACED_BY_RE` directly: the row's `calculation_ref` text ("no replacement needed") does not match the `replaced by\s+([A-Z]+-\d{4})` regex, so it correctly registers as "no replacement claimed" rather than falsely triggering a replacement-ID check. Correctly formatted.

5. **Final scan:** Read through §§1–9 and Confidence. No other stray quotes, orphaned brackets, or broken cross-references found. The eleven genuine Tier-C exceptions (PROP-0008–0011, 0023–0029) still carry properly attributed `EXCEPTION APPROVED by Lucas, 2026-09-21` markers, distinct from PROP-0055's now-resolved situation. PROP-0056 (CGT unification) is unchanged from round 2's clean verification.

---

## What I couldn't check

- No Bash access this session — I did not re-run `validate.py`/`test_validate.py`. I verified the withdrawn-row and exception-marker logic by reading the script's source directly, as in round 2, and traced the specific regex paths relevant to `PROP-0055`. A live run would confirm this in practice.
- Did not re-fetch any source pages this round — out of scope for a narrow final pass; round 1 and round 2 already independently fetched and confirmed everything relevant.

---

## Recommendation

One-line fix to §9 (Finding 1) and this dossier is ready to publish as a draft. Everything else — the quote fix, PROP-0055's removal from the live dossier text, its withdrawn-row formatting, and the substantive Rightmove point itself — is confirmed clean.
