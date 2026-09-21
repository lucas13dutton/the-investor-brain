# Skeptic review: UK buy-to-let property dossier (round 2)

**Reviewed:** `dossiers/uk-property.md` · **Date:** 2026-09-21 · **Reviewer:** skeptic agent
**Scope (per brief):** narrow — verify round-1 findings 1 and 2 were fixed correctly, spot-check findings 3–5 as exact-string fixes, and read through for anything the fixes themselves broke.

---

## Verdict: **Fix**

Findings 1 and 2 from round 1 are correctly closed on their own narrow terms — the Rightmove figure is now logged and bracketed everywhere, and the CGT-unification claim now has a real, independently-verified Tier A citation that is honest about not being a direct-quote source for the phrase "Autumn Budget 2024." Findings 3–5 are all verified as exact-string fixes. But the new row added to close Finding 1, `PROP-0055`, has its own defect: its `calculation_ref` argues no `EXCEPTION APPROVED` marker is needed for its Tier-C-only sourcing — and in doing so, accidentally *contains* the literal string "EXCEPTION APPROVED," which is exactly what `validate.py`'s regex-based check searches for. The row therefore currently passes validation by a false-positive text match, not because a real exception was ever granted by Lucas. That's a new, concrete problem, not a re-litigation of the round-1 findings.

---

## Findings

### 1. [Major] `PROP-0055`'s Tier-C-only status is not genuinely cleared — it passes `validate.py` by accident, not by approval

`PROP-0055`'s `calculation_ref` reads (in full):

> "n/a — directly sourced from dossiers/uk-property.md sections 3.5, 5 and 9; added per skeptic review reviews/uk-property-review-2026-09-21-v1.md finding 1 (number was quoted three times but never bracketed). Tier C (a commercial portal describing its own index), used only for the caveat that this index is asking-price-based, never as a headline figure or sale-price substitute — **no EXCEPTION APPROVED marker needed** since it does not support a cost-stack or tax figure."

I read `validate.py` directly. Its exception check (`_has_exception_marker`, called from `_validate_claim_row` rule 3) is a plain case-insensitive regex search for the substring `EXCEPTION APPROVED` across `claim_text`, `source_1_name`, `source_2_name` and `calculation_ref` — it has no way to distinguish "EXCEPTION APPROVED by Lucas" from "no EXCEPTION APPROVED marker needed." Both contain the matched substring. So this row's own sentence *arguing that no exception is needed* is exactly what makes the validator conclude an exception marker is present. That's a false positive: nobody — not Lucas, not this session — actually approved a Tier-C-only exception for this row, in contrast to the eleven other Tier-C-only rows in this same file (PROP-0008, 0009, 0010, 0011, 0023–0029), each of which carries the genuine, attributed marker "`EXCEPTION APPROVED by Lucas, 2026-09-21`" following an explicit escalation (Open Questions §8, item 14).

Whether this specific claim (Rightmove's "circa 95%" figure, quoted three times as a data-quality caveat, never as a cost or tax input) actually *needs* the same exception treatment as a cost-stack figure is a genuine, arguable policy question — methodology §7.1 states Tier C sources are "Background only. Never the sole support for a published number," with no explicit headline/non-headline carve-out (that carve-out exists only for the separate "research published by a firm that sells investment or advisory services" rule). The 95% figure is quoted verbatim, three times, in published dossier text — it reads as a published number to me, not mere internal working. Either way, this is not the researcher's call to make unilaterally and then word around the validator — it's exactly the kind of Tier-C-sourcing judgment call that the eleven precedent rows in this same dossier were properly escalated to Lucas for.

**Fix, either or both:**
(a) Escalate this specific row to Lucas the same way the other eleven were, and if approved, write the marker properly attributed ("EXCEPTION APPROVED by Lucas, &lt;date&gt;"), or find a Tier A/B corroborating source for the 95% figure, or drop the specific number from the dossier text and describe the caveat qualitatively instead ("Rightmove's own index is explicitly asking-price-based, not a sale-price index" with no percentage, which would remove the need for an exception at all).
(b) Independently of what happens to this specific row, `validate.py`'s exception-marker regex should be tightened so a sentence that *denies* needing an exception can't satisfy the same check that's meant to gate on a *genuine* one — a literal-minded reviewer bot (or future author) can currently launder a Tier-C-only row past the validator just by writing the words "no exception needed" into `calculation_ref`. This is a systemic gap, not specific to this row, and worth flagging to whoever owns `validate.py`.

### 2. [Minor] Malformed quote marks in the §5 UKHPI row, introduced by the round-1 "of"→"by" fix

§5's UKHPI row now reads: `A joint production **by HM Land Registry, Land and Property Services Northern Ireland, Office for National Statistics and Registers of Scotland"** [PROP-0047]` — there is a stray closing double-quote (`"`) immediately after "Scotland" with no matching opening quote before "A joint production." I confirmed the phrase is in fact a verbatim match of `PROP-0047`'s logged quote ("a joint production by HM Land Registry, Land and Property Services Northern Ireland, Office for National Statistics and Registers of Scotland"), so it should be properly wrapped in matching quotation marks for consistency with how every other direct quote is rendered elsewhere in this dossier — not left with a dangling, unmatched one.

**Fix:** add the opening quotation mark before "A joint production" (or drop the stray closing one if the house style for this cell is meant to be unquoted paraphrase — but given it's word-for-word, quoting it properly reads better).

### 3. [Minor] `PROP-0055`'s `value`/`unit` fields are blank despite the claim containing a specific number

Per `data/evidence/README.md`: "`value` ... Leave blank only for a qualitative claim with no single number (rare — most rows should have one)." `PROP-0055`'s claim is "built on circa 95% of newly marketed property" — a specific number — yet `value` and `unit` are both blank. Cosmetic, doesn't affect validation or the dossier text, but inconsistent with the log's own stated norm and worth a one-line fix (`value: 95`, `unit: %`, or `unit: % (approximate, "circa")` if precision matters).

---

## Verification of the specific items in the brief

**Finding 1 (Rightmove/PROP-0055):** row exists, is Tier C, cites `https://www.rightmove.co.uk/press-centre/house-price-index/`, quote matches round 1's independently-fetched text exactly. All three in-text brackets (§3.5 line 80, §5 line 116, §9 line 191) are present and correctly placed. Round-1's specific ask is satisfied — see Finding 1 above for a new, separate problem this row itself introduces.

**Finding 2 (CGT unification/PROP-0056):** I independently re-fetched `https://www.gov.uk/guidance/capital-gains-tax-rates-and-allowances` myself (not relying on the round-1 fetch or the evidence-log entry alone). It confirms: 6 April 2024–29 October 2024, general assets at 10%/20%, residential property separately at 18%/24%; from 30 October 2024, general assets raised to 18%/24%, unifying with property. This matches `PROP-0056`'s logged quote and the dossier's §4.2/§9 text exactly. I also independently confirmed the page **never uses the phrase "Autumn Budget 2024"** anywhere — the dossier's parenthetical "(the Autumn Budget 2024)" is not presented in quotation marks and is not attributed to the gov.uk page as a quote; it reads as background framing of a well-known, undisputed fiscal event name attached to a real, quoted, dated statutory rate change. I don't think this oversteps — it would be a problem if it were rendered as a quoted phrase from the cited source, but it isn't. `PROP-0056`'s own `calculation_ref` proactively flags this same point ("The page itself does not use the phrase 'Autumn Budget 2024'..."), which is exactly the right level of honesty.

**Findings 3–5:** all confirmed as described.
- Finding 3: §5's UKHPI cell now reads "by" (not "of") and drops "the" before "Office for National Statistics," matching `PROP-0047` verbatim — see Finding 2 above for a separate, new quote-mark formatting defect this same edit left behind.
- Finding 4: `PROP-0051`'s `source_1_quote` now reads "all commercial transactions ... sales that were not for full market value ... 'Right to buy' sales at a discount ... by way of a gift ... under a court order ... leases for seven years or less" — covers all six exclusion categories in its `claim_text`. Confirmed.
- Finding 5: §4 now reads "an investment-regulated pension scheme (a defined term covering the great majority of ordinary SIPPs, not simply any 'registered' scheme) acquiring residential property directly..." — confirmed, matches the required fix.

**Read-through for fix-introduced breakage:** the two new `PROP-0056` sentences in §4.2 and §9 don't introduce any fresh unbracketed rate figure — the "10%/20%" and "18%/24%" figures inside the new sentences share a single trailing `[PROP-0056]` bracket per clause, which is the same single-bracket-per-compound-clause convention already used elsewhere in this dossier (e.g. `PROP-0051`'s six-category exclusion list, `PROP-0038`–`PROP-0041`'s phase-in percentages), not a new pattern introduced by this fix. No other broken cross-reference or orphaned reference found in a full read of the document. `PROP-0055` and `PROP-0056` are the only two claim IDs added since round 1; both round-trip correctly against the dossier text (cited where expected, no orphans).

---

## What I couldn't check

- I did not re-run `data/evidence/validate.py` myself (no Bash access this session) — I verified the specific rule it implements (rule 3, the Tier-C-exception check) by reading `validate.py`'s source directly and tracing the regex against `PROP-0055`'s actual field content by hand, which is how I found Finding 1. I'm confident in this reading, but a live run would show whether my reasoning about the false-positive match is correct in practice, not just on paper.
- I did not re-fetch `PROP-0047`'s or `PROP-0051`'s source pages again this round — round 1 already independently fetched and confirmed both, and the round-2 task only asked for exact-string verification against the evidence log, which I did.
- I did not investigate whether `validate.py`'s exception-marker false-positive (Finding 1) affects any other row in the 265-row file beyond `PROP-0055` — this would need a full-file grep for negated "EXCEPTION APPROVED" phrasing, which is out of this round's scope but worth a follow-up.

---

## Recommendation

Fix Finding 1 (either get a genuine Lucas sign-off for `PROP-0055`'s Tier-C sourcing, or remove the specific "95%" figure from the dossier so no exception is needed, or add a real Tier A/B corroborating source) plus the two minor items, then this dossier is ready. Given round 3 is the last permitted round, I'd suggest resolving Finding 1 with Lucas directly rather than another full review cycle if time is short — it's a narrow, well-defined decision (approve the exception properly, or don't rely on Tier C alone for this number), not something that needs re-litigating the rest of the dossier.
