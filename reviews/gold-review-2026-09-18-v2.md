# Skeptic re-review: Gold dossier — scoped verification of three surgical fixes

**Reviewed:** `dossiers/gold.md` · **Date:** 2026-09-18 · **Reviewer:** skeptic agent
**Scope:** This is a narrow re-review of exactly the three items flagged as Major/Minor findings in `reviews/gold-review-2026-09-18.md` (the prior Fix verdict). **The rest of the dossier is out of scope for this pass** — it already passed independent checking across two prior rounds and was not touched by the researcher in this third pass. Nothing below should be read as re-endorsing or re-litigating anything outside these three items.

---

## Verdict: **Pass** (scoped to the three items below)

All three fixes hold up under direct verification. Two of the three citations were confirmed by direct fetch of the primary source; the third (Noonans) was corroborated through indexed search content pulled from the same primary domain, since direct automated fetch of noonans.co.uk was blocked (403) for me — noted honestly below rather than waved through.

---

## Findings

### 1. SDRT/ETC incorporation citation (previously Major) — Fixed, confirmed

The dossier (§4.3, §9) now cites **STSM031090** ("Scope of Stamp Duty Reserve Tax (SDRT): chargeable securities — general") instead of the wrong STSM011020 page.

I fetched `gov.uk/hmrc-internal-manuals/stamp-taxes-shares-manual/stsm031090` directly, twice, with different prompts to cross-check for paraphrase drift. The page confirms, in substance and largely verbatim:

- Securities are **excluded** from "chargeable securities" where "issued or raised by a company incorporated outside the UK (and with no UK register)" **and** not paired with shares in a UK company — this exact phrasing was returned by my fetch.
- Non-UK company securities are **brought back into scope** (i.e., become chargeable) where they are registered in a UK register, or paired with UK company shares — matching the dossier's second quoted clause ("issued or raised by a non-UK incorporated company but registered in a register kept in the UK").

This is a faithful, accurate citation of the actual rule, including both the exclusion and the carve-back exception, and both the "no UK register" and "not paired with UK shares" conditions the dossier's sentence structure implies. This is a real fix, not a re-hash of the same error — it cites the correct manual page and quotes it correctly. The underlying Irish-incorporation fact for iShares Physical Metals plc was already independently verified in the prior round and is unchanged.

**Confirmed.**

### 2. Buyer's premium row (previously Major) — Fixed, confirmed with one caveat

The dossier now states, for Noonans Mayfair: "Our buyers premium is 24% on the hammer price. For UK auctions this is subject to VAT if the lots are collected or delivered within the UK," attributed to noonans.co.uk's "Help & Information" page, fetched directly 2026-09-18.

I could not replicate a direct fetch — `noonans.co.uk/help-and-information/` and `noonans.co.uk/auctions/buying/` both returned **HTTP 403** to my fetch tool (likely bot protection, since the researcher claims a successful direct fetch on the same date). I do not treat this as a red flag on its own — sites blocking one client's crawler while allowing a human browser or a different agent's fetch path is a routine, unremarkable occurrence. To corroborate independently, I ran a web search and pulled indexed content specifically attributed to `noonans.co.uk/auctions/buying/` and `noonans.co.uk/help-and-information/`. That indexed content states: "A buyers premium of 24% of the hammer price (plus VAT if lots are collected or delivered within the UK) is payable by the buyer on all lots" — matching the dossier's figure and VAT treatment exactly (word-for-word on the VAT condition).

On Spink and Baldwin's: the dossier's row and the sources table (§9, Tier C list) now state plainly that these two were **dropped** ("not stated here"), with a clear, specific reason given (Spink's terms PDF returned unreadable/encoded content; Baldwin's terms page returned a certificate error then a 404 on retry), and the prior review's mismatched figures (25%/25%) are gone — I searched the full row and the sources section and found no reintroduced or fudged number for either house. This is exactly the right behaviour under house-rules item 10 ("no made-up numbers") and methodology §7.1 (asking/unverifiable figures are not treated as sourced).

**Confirmed**, with the caveat that my own verification of the Noonans figure rests on search-indexed content rather than a raw fetch I could reproduce myself — flagged in "What I couldn't check" below, not as a defect.

### 3. eBay business-seller fee (previously Minor) — Fixed, confirmed

I fetched `ebay.co.uk/help/selling/fees-credits-invoices/selling-fees?id=4809` directly, twice, to cover both the Coins-specific figure and the wider category table. Confirmed exactly as the dossier states:

- Page states "Last Updated: August 4, 2026" — matches the dossier's "last updated 4 August 2026."
- **Coins**: 10.9% up to £450, then 3% above — matches exactly, verbatim.
- Several categories (Books, Cameras & Photography, Films & TV, Mobile Phones & Communication, Music, Sound & Vision, Video Games & Consoles) at 9.9% base rate — matches the dossier's "9.9% in several common categories (Books, Music, Video Games, Cameras & Photography)."
- **Jewellery & Watches**: 14.9% up to £1,000, then 4% above — matches exactly.
- **"Everything Else"** catch-all at 12.9% — matches.
- Per-order fee: 30p (orders ≤£10) / 40p (orders over £10) — matches.
- Regulatory Operating Fee: 0.35% of total sale amount — matches the dossier's "~0.35% Regulatory Operating Fee."

The dossier's characterisation that the fee is "genuinely category-dependent, not a single flat rate" and that there is no single "commonly quoted" figure is accurate — the live page confirms a materially more complex structure than the old "~10.9%" framing implied. The 10.9% figure the researcher chose to lead with (Coins, the category "most relevant to physical gold") is the correct one to highlight for this asset.

**Confirmed.**

---

## What I couldn't check

- **Noonans' page content via raw direct fetch.** `noonans.co.uk` returned 403 to my fetch tool on both URLs I tried. I relied on search-engine-indexed content attributed to the same domain/pages as corroboration, which matched the dossier's figure and VAT wording exactly, but this is not the same as me personally loading the live page. If a stricter bar is wanted, someone with direct browser access should reconfirm, though I have no reason to doubt the researcher's or the search index's consistent figure.
- **Whether the researcher's STSM031090 fetch and mine hit an identical, unedited version of the page** (HMRC manual pages can be revised) — both fetches were same-day (2026-09-18), so this is a negligible risk, not a real gap.
- Nothing else was checked. The rest of the dossier (cost stack completeness, CGT/VAT citations, evidence-log gap, Action Fraud citation, price-data licensing, etc.) is unchanged from the prior two rounds and is **explicitly out of scope for this pass** — see the prior review (`reviews/gold-review-2026-09-18.md`) and the round before it for that coverage. This Pass verdict applies only to the three items above, not to the dossier as a whole, which remains gated on the open items already logged in dossiers/gold.md §8 (most importantly, the missing evidence log, which the dossier itself says blocks publication of every number regardless of sourcing quality).
