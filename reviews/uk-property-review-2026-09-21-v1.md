# Skeptic review: UK buy-to-let property dossier (round 1)

**Reviewed:** `dossiers/uk-property.md` (draft v1) · **Date:** 2026-09-21 · **Reviewer:** skeptic agent
**Scope:** full adversarial review per `docs/methodology.md` and `docs/house-rules.md` — quote integrity, the Tier-C-only exception scope, URL hygiene, sensitivity-row labelling, cost-stack completeness, tax-scenario framing, and the evidence-log claim-ID rule. Per the brief, the 11 approved Tier-C exceptions (PROP-0008, 0009, 0010, 0011, 0023–0029) are **not** re-litigated as a policy matter — Lucas has already settled that. What is checked is whether the marker is on exactly those 11 rows and whether a missed Tier A/B alternative exists for any of them.

---

## Verdict: **Fix**

The tax and statutory sourcing in this dossier is genuinely strong — every HMRC/gov.uk citation I independently re-fetched (SDLT bands and surcharge, the 3%→5% surcharge date change, CGT rates and the 60-day deadline, Section 24's full phase-in table, PRR conditions, the UKHPI's licence and construction, the MHCLG survey figures, the MoJ possession statistic, the Renters' Rights Act date) matched both the dossier's quote and the evidence log's quote, word for word. The 11 Tier-C exception rows are correctly and exclusively marked, with no leakage onto rows that don't need it and no gaps on rows that do. But the dossier fails its own stated rule at least once (a number with no bracketed claim ID anywhere), and asserts one specific, dateable tax-policy fact — when general-asset CGT rates were raised to match property rates — with no citation and no evidence-log row at all, despite the same dossier being scrupulous about dating every other tax change it discusses. Both are fixable without touching the rest of the document.

---

## Findings

### 1. [Major] A quoted numeric claim has no evidence-log ID anywhere — fails the dossier's own stated rule

The dossier's own preamble (line 6) states: "**Every numeric claim carries its evidence-log claim ID in brackets immediately after it**... No number is published without one." This is violated by the Rightmove figure, which appears **three times**, always in quotes, never bracketed:

- §3.5 (Time to sell), source cell: `"This is an asking-price index, built on "circa 95% of newly marketed property" — not a sale-price index."`
- §5 (Price data sources), Rightmove row: `"This is an asking-price index, built on "circa 95% of newly marketed property"..."`
- §9 (Sources, Tier C background list): `"confirms the index is asking-price-based ("circa 95% of newly marketed property")..."`

I searched `data/evidence/evidence.csv` for a PROP row backing this figure — none exists (I confirmed all 54 existing PROP rows, PROP-0001 through PROP-0054, are accounted for elsewhere and none covers this claim). I independently fetched `rightmove.co.uk/press-centre/house-price-index/` and confirmed the figure is real and accurately quoted: **"Based on circa 95% of newly marketed property, the Rightmove House Price Index is the leading indicator of residential property prices..."** — so this isn't fabricated, just unlogged. Per the review brief's own test ("A number with no bracketed ID... blocks the dossier") and house rule B1 ("Every number has an evidence log ID"), this needs fixing before publication, even though it's caveat/background text rather than a headline figure.

**Fix:** add a row (e.g. `PROP-0055`, `row_type: claim`, Tier C, quote as above, `source_1_url: https://www.rightmove.co.uk/press-centre/house-price-index/`, accessed 2026-09-21), and add `[PROP-0055]` at all three locations above.

### 2. [Major] The CGT-rate-unification claim is asserted with no citation and no claim ID

§4.2 states: "Historically this was not always true — residential property carried its own higher CGT rates for a period, separate from the lower general-asset rates — but **the general-asset rates were raised to match the property rates from the Autumn 2024 Budget onward**, and the two remain aligned at the current 6 April 2026 rates checked here." This exact framing is repeated in §9's sources-disagreement note.

This is a specific, dateable, checkable policy claim (a rate change, tied to a named fiscal event), of exactly the kind this dossier is otherwise careful to source precisely (compare the SDLT surcharge's 31 October 2024 effective date, cited to SDLTM09845a with a verbatim quote). But here there is **no citation, no quote, and no claim ID** — PROP-0032/PROP-0033 only establish the *current* 18%/24% rates ("you'll pay 18% on your gains... made from 6 April 2026"); neither their quote nor any other row in evidence.csv says anything about the Autumn 2024 Budget or a prior unification event. I independently fetched the live `gov.uk/capital-gains-tax/rates` page and confirmed it **does not mention "Autumn Budget" or "30 October 2024" anywhere** — the page only states current-year rates and links out to a separate historical-rates page that wasn't checked. `dossiers/sp500.md`, which this dossier cross-references for corroboration ("cites the identical 18%/24% rates from the same gov.uk page"), has the identical gap — it doesn't source the Autumn 2024 Budget claim either, so the cross-reference doesn't actually corroborate anything beyond the current rate itself.

**Fix:** either (a) find and cite the actual source for when/why general-asset CGT rates rose to 18%/24% (the historical rates page linked from the current one, or the original Autumn Budget 2024 policy documents), give it its own claim ID, and quote it; or (b) if that can't be done quickly, strip the specific "Autumn 2024 Budget" attribution from both §4.2 and §9 and move the claim to Open Questions as unconfirmed, per methodology §7.3 ("If the specific line supporting a claim cannot be found, the claim does not get cited as settled. It moves to Open Questions instead").

### 3. [Minor] UKHPI joint-publisher line: dossier prose doesn't match its own evidence-log quote verbatim

§5 renders the citation as: "A joint production **of** HM Land Registry, Land and Property Services Northern Ireland, **the** Office for National Statistics and Registers of Scotland" [PROP-0047].

The evidence log's own `PROP-0047` quote (and the live gov.uk page, which I independently fetched) both say: **"a joint production by HM Land Registry, Land and Property Services Northern Ireland, Office for National Statistics and Registers of Scotland"** — "by," not "of," and no "the" before "Office for National Statistics." The evidence log row is correct; only the dossier's in-text rendering has drifted from strict verbatim while still being formatted as if it were a direct quote. Small, but this is a company whose entire credibility rests on exact quotes, and the gold-dossier review history (`reviews/gold-review-2026-09-18-v3.md`, Finding 4) already flagged this exact failure mode (quote given in the dossier not matching the quote given in the evidence log) as worth fixing even when non-fabricated.

**Fix:** change "of" to "by" and remove "the" before "Office for National Statistics" in the §5 table cell, to match `PROP-0047` exactly.

### 4. [Minor] PROP-0051's logged quote doesn't cover two of the six exclusion categories in its own claim_text

`PROP-0051`'s `claim_text` asserts six exclusion categories (commercial transactions, non-market-value sales, Right to Buy discounts, **gifts**, **court-ordered transfers**, and short leases), but its `source_1_quote` field only stitches together fragments for four of them via ellipsis ("all commercial transactions ... sales that were not for full market value ... Right to buy ... leases for seven years or less") — "gifts" and "court-ordered transfers" are named in the claim but absent from the quote. I independently fetched the live page and confirmed both missing fragments are genuinely there ("transfers 'by way of a gift'" and "those 'under a court order'"), so nothing is fabricated, but as logged, the quote doesn't fully back the claim it's attached to — a future checker relying only on the evidence log (per the README's own instructions) wouldn't be able to verify the gift/court-order half of this claim from the quote alone.

**Fix:** extend `source_1_quote` to include the gift and court-order fragments (matching the ellipsis pattern already used for the other four).

### 5. [Minor] PTM125100 characterisation drops a qualifying term that narrows the rule

§4 states: "a registered pension scheme acquiring residential property directly 'will create an unauthorised payment...'" I independently fetched HMRC's PTM125100 and confirmed the actual mechanism is scoped more narrowly: it applies when **"an investment-regulated pension scheme... acquires taxable property"** — "investment-regulated" is a defined term, not a synonym for "registered." In practice, essentially every ordinary SIPP is an investment-regulated scheme, so this doesn't change the substantive conclusion for this dossier's reference investor, but it is a precision slip in a section that is otherwise very careful about exact wording (e.g. it correctly hedges the ISA claim with "generally").

**Fix:** add the qualifier, e.g. "...an *investment-regulated* pension scheme (which covers the great majority of SIPPs) acquiring residential property directly..."

### 6. [Minor, optional] Open Question §8.9 could be partly resolved rather than left fully open

The dossier states the MoJ possession-statistics release doesn't break out figures by private landlord specifically. I independently fetched the same release and found its Statistician's Comment does contain one private-landlord-specific data point on the same page already cited for PROP-0031: **"private landlord repossessions have seen the largest decrease, by just under 3 weeks compared to the same period last year."** Not an error in the dossier — it's honestly flagged as an open gap rather than invented — but this specific qualitative fact was sitting on the very page already fetched and could upgrade the open question from "no private-landlord breakout at all" to "a partial qualitative breakout exists; no quantified median specific to private landlords." Not required for a Fix verdict; flagged as a low-cost improvement.

---

## Verification of the specific items in the brief

**Quote integrity, sampled and independently re-fetched (well beyond the requested 5–6):**
SDLT rate bands and 5% surcharge; the 3%→5% surcharge change effective 31 October 2024 (SDLTM09845a); CGT rates 18%/24% and the "made from 6 April 2026" wording; the £3,000 2026/27 annual exempt amount; the 60-day CGT reporting deadline; Private Residence Relief's conditions; gov.uk's list of taxable property types including buy-to-let; the Section 24 phase-in table (75/25 → 50/50 → 25/75 → 0/100) and the 20%-of-the-lowest-of mechanism and the 82% HMRC estimate; the UKHPI's OGL v3.0 licence statement; the UKHPI's publisher list, 1995 start date, completed-transaction basis and exclusions; HMRC PTM125100's unauthorised-payment mechanism (see Finding 5); gov.uk's ISA holdings list; the MHCLG English Private Landlord Survey 2024's void/reletting/agent-usage percentages; the Ministry of Justice's 27.1-week possession statistic; HomeOwners Alliance's BTL deposit (20–25%, 40%+) and arrangement-fee wording; HomeOwners Alliance's estate-agent commission ranges (1.42% average, 1.2–1.8% sole, 3–3.6% multiple); NatWest's interest-only confirmation; and the Renters' Rights Act's Royal Assent date (with the page confirmed to say nothing about a commencement date, matching the dossier's own honest flag). **All matched, aside from Findings 3 and 4.** No fabricated or invented figure found anywhere in this sample.

**The Tier-C-only exception marker (PROP-0008, 0009, 0010, 0011, 0023–0029):** confirmed present on exactly these 11 rows and on no others, by reading every PROP row in `data/evidence/evidence.csv` directly. The exception language is identical and correctly formatted across all 11. No row that should carry it is missing it; no row that shouldn't carry it has it.

**Whether a missed Tier A/B alternative exists for 2–3 of the 11:** I attempted (constrained by this session's exhausted web-search budget, so via direct WebFetch only) to find a Tier A/B alternative for the BTL mortgage deposit/rate figures and the estate-agent/conveyancing fee figures. Bank of England's mortgage-lenders statistics landing page gave no clear BTL-specific LTV or rate breakout on the page I could reach; UK Finance's equivalent data sits behind a "My UK Finance" member portal login, which is consistent with (not a contradiction of) the dossier's own finding. A direct guess at Reallymoving's own conveyancing-fee page 404'd. I did not find a missed Tier A/B source for any of the 11 rows — this is not proof none exists, but it did not surface one, and I recommend not re-opening the exception on the strength of this alone.

**Sensitivity rows (PROP-0012/0013, PROP-0021, PROP-0022):** `PROP-0013` (BTL mortgage rate upper bound, 7%), `PROP-0021` (letting/management fee upper bound, 15%) and `PROP-0022` (maintenance upper bound, 1.5%) are all correctly `row_type: sensitivity` with every `source_*` field blank, per `data/evidence/README.md`'s rule. `PROP-0012` (Bank of England Bank Rate, 3.75%) is correctly a Tier A `claim` row, not a sensitivity — it is genuine, sourced, current fact, used only as background context, and its own `claim_text` explicitly says "cited as rate-environment background context, not as a mortgage rate itself," so it is not conflated with the sensitivity figure. In the dossier prose, all three sensitivity values are consistently introduced with "labelled sensitivity," "explicitly an unverified upper-bound assumption," or equivalent, at every point of use — I did not find any place where a sensitivity figure is presented as if it were a verified number.

**Cost-stack completeness against the task's required scope:** SDLT surcharge (§3.1, sourced), mortgage costs (§3.1 arrangement fee, §3.2 interest — sourced/sensitivity), voids (§3.2, sourced qualitatively via MHCLG, no quantified average — honestly flagged), maintenance (§3.2, sensitivity), letting fees (§3.2, sensitivity), Section 24 (§4.1, fully sourced), CGT on sale (§4.2, fully sourced), time to sell (§3.5, sourced). Nothing from the required list is silently dropped.

**Tax-scenario framing (ISA/SIPP exclusion):** the ISA claim is correctly hedged ("generally cannot be held," reasoning from the absence of property in gov.uk's own list rather than claiming an explicit prohibition that isn't stated). The SIPP/PTM125100 claim is accurate but drops a qualifying term — see Finding 5.

**Arithmetic:** the one worked calculation in the dossier (SDLT on a £250,000 additional property: £2,500 standard + £12,500 surcharge = £15,000) is independently correct, and is honestly labelled "illustration only, not a separate sourced claim," so it doesn't need its own evidence-log row.

**Cherry-picking:** not applicable yet — this dossier is cost-stack/tax scaffolding, no return windows are calculated or shown.

**Overreach:** a full-text scan for recommendation, prediction or guarantee language ("should buy/sell/hold," "safe," "guaranteed," "passive income," "undervalued/overvalued," "will rise/fall") found nothing.

**URL hygiene:** every `source_1_url`/`source_2_url` across all 54 PROP rows starts with `https://`; no guessed URLs, no unexplained `NEEDS RE-VERIFICATION` flags (there was no need for one — every source was reachable this session).

**Claim-ID round trip:** every `PROP-0001`–`PROP-0054` ID cited in the dossier text exists in `evidence.csv`, and every PROP row in `evidence.csv` is cited at least once in the dossier — no orphans in either direction, aside from the unlogged Rightmove figure in Finding 1.

---

## What I couldn't check

- **This session's web-search tool was exhausted after my first three queries** (checking for a Tier A/B alternative to the BTL mortgage-rate and estate-agent-fee Tier C sources), so my search for a missed alternative source relied on direct WebFetch guesses rather than a broad search. I don't consider this a live risk to the verdict — the dossier's own documented attempt (a dozen-plus pages tried and logged) is more thorough than what I could redo here — but a human with search access could still usefully double-check this.
- **Reallymoving's own conveyancing-fee page directly** (as opposed to HomeOwners Alliance's citation of it) — my one guessed URL 404'd, and I didn't have search to find the live one. Even if found, it's a commercial quote-comparison vendor and likely still Tier C under the "vendor marketing" rule, so I don't expect this would change the exception's validity, only (possibly) let the dossier cite the primary rather than secondary source.
- **HM Land Registry Price Paid Data's own licence terms specifically** (as distinct from the UKHPI's, which I did verify) — the dossier itself flags this as not independently explored (§8.8), so this is a pre-existing, disclosed gap, not a new one.
- **The historical CGT-rates page** (`gov.uk/guidance/capital-gains-tax-rates-and-allowances`) that the current rates page links out to — I did not fetch this, so I cannot say whether it would actually support the "Autumn 2024 Budget" claim in Finding 2; I can only confirm the currently-cited page doesn't.
- **Bank of England and UK Finance's full statistical release catalogues** — I checked landing/overview pages only, not every sub-page or data table, so I cannot rule out a BTL-specific series existing somewhere deeper in either site that neither the researcher nor I happened to find.

---

## Recommendation

**Fix, then a second review round.** Findings 1 and 2 are both concrete, specific, and easy to verify once addressed — I'd recommend a scoped round-2 review (like `reviews/gold-review-2026-09-18-v2.md`'s pattern) that checks only: (a) the new Rightmove claim-ID row and its three in-text brackets, and (b) either a real citation for the CGT-unification claim or its removal/downgrade to Open Questions. Findings 3–5 are minor and could reasonably be fixed and waved through without a further dedicated check, but should still be corrected before this leaves draft status. This dossier is materially closer to publishable than gold.md's round 1 was — nothing here suggests a fabricated number, a misapplied exception, or a mischaracterised tax rule, only two rule-compliance gaps and a few quote-fidelity slips.
