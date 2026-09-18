# Skeptic review: Gold dossier (rebuild v2)

**Reviewed:** `dossiers/gold.md` · **Date:** 2026-09-18 · **Reviewer:** skeptic agent
**Context:** rebuild after a prior BLOCK verdict dated 2026-09-18 (that review has been deleted; this is a fresh, independent check of the rebuild, not a diff against it).

---

## Verdict: **Fix**

The rebuild is a genuine improvement and most of the five claimed fixes hold up under independent checking. But two of the specific claims I was asked to verify have real defects — one is a mis-cited Tier A source (the source exists but does not say what the dossier says it says), the other is a set of specific numbers that don't match independent verification for two of three named sources. Per my own instructions ("does each claim's source exist, say what we say it says, and meet its tier? Open them"), both fail that test. Neither is fatal to the whole dossier — it is already self-blocked pending the evidence log — but both need correcting before this rebuild can be called closed, and the SDRT mis-citation in particular is the same failure mode (a specific manual page cited for a claim it doesn't contain) that sank the previous draft's "1837" sourcing.

---

## Findings

### 1. [Major] STSM011020 does not say what the dossier says it says

Section 4.3 states: SDRT under FA1986 applies to "chargeable securities," which HMRC's own manual (**STSM011020**) defines, in general terms, as securities of a **UK-incorporated** company... Non-UK incorporation... is the more likely reason SDRT does not apply.

I fetched `gov.uk/hmrc-internal-manuals/stamp-taxes-shares-manual/stsm011020` directly. It is an introductory page ("What is Stamp Duty Reserve Tax?") that explains SDRT taxes agreements to transfer chargeable securities without needing a written instrument. **It contains no definition of "chargeable securities" and does not mention UK incorporation at all.** It points readers to STSM030000 for more detail — a different section the dossier doesn't cite.

The underlying tax conclusion (SDRT generally turns on whether the issuer is UK-incorporated, subject to exceptions) is plausible and consistent with general knowledge of UK stamp taxes, and the specific fact about iShares Physical Metals plc being Irish-incorporated (ISIN IE00B4ND3602) checks out independently. But the **citation itself is wrong** — the page cited isn't the source of the claim. This is exactly the "source exists but doesn't say what we say it says" failure the methodology and my brief exist to catch, and it's the same category of error (a specific HMRC manual page mis-attributed) that the original v1 draft was blocked for on the Sovereign "1837" point — except this time it's the *replacement* fix that has the problem, not the original claim.

**What would fix it:** find and cite the actual STSM page that defines "chargeable securities" by reference to UK incorporation (likely somewhere in the STSM031000 series — "Scope of Stamp Duty Reserve Tax: chargeable securities"), fetch it directly, and quote the relevant text, the way CG78305 was correctly handled.

### 2. [Major] Auction buyer's-premium figures don't match independent verification for 2 of 3 named houses

Section 3.1 states: 18–26% on top of the hammer price... (Spink 25%, Baldwin's of St James's 25%, Noonans Mayfair 24%, on their published terms of business).

I could not fetch Spink's or Baldwin's own terms-for-buyers pages directly (certificate error on Spink's buyer T&Cs PDF path I tried; 403 on Baldwin's terms page), so this is not a full primary-source-vs-primary-source comparison. But independent secondary sources (auction-industry commentary, third-party listing sites) consistently give:
- **Spink: 22.5% + VAT** (not 25%)
- **Baldwin's of St James's: 24% inclusive of VAT** (not 25%)
- **Noonans Mayfair: 24%** (matches)

Two of the three specific numbers attributed to "their published terms of business" — wording that implies the researcher pulled these directly from the primary source — don't match what's independently findable. Auction house buyer's premiums do change over time (Noonans itself has a public history of premium increases), so this could be a stale secondary source on my end rather than an error in the dossier, but the discrepancy is consistent across more than one independent source on my side, which is enough to flag rather than wave through. The 18–26% range itself still roughly holds regardless of whose exact number is right, so this doesn't undermine the row's overall shape — but it undermines the claim that these three figures were freshly and directly verified against primary terms of business.

**What would fix it:** the researcher should re-pull the current buyer's-terms PDF/page directly from spink.com and bsjauctions.com (not a cached search result), quote the exact clause, and correct the two figures if they're wrong, or show the working if my check is the one that's stale.

### 3. [Minor] "Verified for the iShares issuer" overstates what was actually verified

Following from Finding 1: the Irish-incorporation fact for SGLN/iShares Physical Metals plc is genuinely verified (Tier B, prospectus/ISIN). But the *legal mechanism* linking that fact to "no SDRT" is attributed to a source (STSM011020) that doesn't support it. The dossier's own wording — "verified for the iShares issuer" — conflates the two. The fact is verified; the legal rule it's supposed to sit under isn't sourced to what's cited.

**What would fix it:** once Finding 1 is corrected, this resolves itself.

### 4. [Minor] Action Fraud transition date is slightly off

Section 7 says the transition to `reportfraud.police.uk` was "completed December 2025." Per City of London Police's own release, the redirect for Action Fraud traffic began 4 December 2025, but the service's "full public launch" was January 2026. "Completed December 2025" slightly overstates how finished the transition was at that date. Doesn't affect the core point (actionfraud.org.uk is not official), which is correctly established.

**What would fix it:** say "redirect began December 2025, full public launch January 2026" rather than "completed."

### 5. [Minor] eBay business-seller final value fee range is close but not exact

Section 3.3 gives business-seller FVF as "roughly 6.9–14.9%, commonly quoted around 10.9%." Current published/commentary figures I found put most categories at 9.9–12.9%, with a commonly cited standard rate of 12.8% (with a per-order fee that rose to 40p for orders over £10 in February 2026, not mentioned in the dossier). Not a material error — it's Tier C background on the ETC/physical-selling side, not a headline figure — but the "commonly ~10.9%" framing looks a little dated next to the more recent ~12.8% figure some sources cite for 2026. Not blocking, but worth a re-check given the dossier prides itself on having freshly re-verified the private-seller eBay figure.

---

## Verification of the five specific claims in the brief

1. **Buyer's premium row added, Tier C, correctly not blended** — Row exists, correctly separates 0% (dealer-direct, ordinary channel) from 18–26% (auction, explicitly labelled as not the ordinary channel), correctly kept as Tier C and not blended into a single number. **Structurally correct.** See Finding 2 for a factual-accuracy problem with the specific percentages cited.

2. **Dealer premium / buy-back spread stated as open, escalated, not settled** — Confirmed. Section 3.1, 3.3, 3.5 and Open Questions §8.1 all state plainly that no Tier A/B source was found, and this is escalated to Lucas as a judgement call rather than argued around. **Claim holds.**

3. **CG78305 cited directly as Tier A, replacing dealer-sourced claim** — I fetched `gov.uk/hmrc-internal-manuals/capital-gains-manual/cg78305` directly. It reads, verbatim: "Sovereigns minted in 1837 and later years and Britannia gold coins are currency but, like all sterling currency, are exempt because of TCGA92/S21(1)(b)." This matches the dossier's quotation exactly. I also fetched CG76881, which confirms "Coins and bank notes which are sterling currency are not chargeable assets" — also matches. **Claim holds; this fix is done correctly and is now solid Tier A.**

4. **Evidence log not invented, flagged as missing infrastructure** — Confirmed by a repo-wide file search: no evidence log file exists anywhere in the repo. The dossier flags this in Open Questions §8 (item 2) and in the Confidence section, and does not present any number as settled fact despite this — every cost figure carries a Low/Central/High/Source(tier) structure and the dossier's own Confidence section states plainly that nothing here is publishable until the log exists. **Claim holds.**

5. **Minor items:**
   - Blank rows replaced with explicit "none, because..." — confirmed throughout section 3; I did not find a single blank cost-stack row. **Holds.**
   - Currency line reasoned "none," flagged unverified — confirmed in 3.4 and 3.9; the physical-gold currency row explicitly flags the embedded-FX-cost assumption as unverified. **Holds.**
   - eBay UK fees corrected (£0 for private UK sellers since Oct 2024) — I fetched eBay's own "Fees for private sellers" page. It states: "It's now free for UK-based private sellers to sell on eBay (excluding motors)... You won't pay final value fees or regulatory operating fees when your items sell," dated "Last updated on 1 October, 2024." **Matches exactly. Holds.**
   - Action Fraud citation corrected (actionfraud.org.uk is a private company, not the police service) — independently confirmed: actionfraud.org.uk is run by a private, Liverpool-based fraud-recovery company; the official service is actionfraud.police.uk / reportfraud.police.uk, run for City of London Police. The two City of London Police press releases cited (Hatton Garden courier-fraud crackdown; the £12m boiler-room/84-gold-bars case) both exist and match the description given. **Holds, with the minor date nuance in Finding 4.**
   - ETC SDRT mechanism corrected to non-UK incorporation, verified for iShares/SGLN via STSM011020 and the prospectus — the incorporation fact (Ireland, IE00B4ND3602) is independently confirmed. **The STSM011020 citation itself does not hold up — see Finding 1.** This is the most substantive problem in this rebuild.

---

## Other checks per standard methodology

- **Arithmetic:** no headline NRR, cost-drag or return figures are calculated in this dossier yet (it is cost-stack and tax scaffolding only), so there is no arithmetic to independently recompute at this stage. Flagged for the next pass once price data and actual returns are added.
- **Cherry-picking:** not yet applicable — no time windows or event windows are used in this draft.
- **Cost-stack completeness:** every row from methodology §3 is present for both the physical and ETC routes, with an explicit reason wherever "none" is used. No blank rows found. This genuinely fixes the prior gap.
- **Survivorship / index vs items:** correctly treated as an index-type asset (section 6), with numismatic/collectible coins correctly carved out as a separate item-based category that would need its own sampling if ever covered. No survivorship-bias sample is needed or claimed here, and none is smuggled in.
- **Overreach:** I searched the full text for promissory, predictive or "safe haven"-style language and found none. No wording implies a recommendation to buy/hold/sell, and no past performance is presented as a guide to future performance beyond what's already flagged as out of scope (no returns are calculated yet).
- **Compliance flag:** the dossier names numerous specific funds, dealers and platforms (SGLN, SGLD, PHGP, RMAU, BullionByPost, Chards, AJ Bell, HL, eBay, BullionVault, Spink, Baldwin's, Noonans, and Montford Group Ltd t/a Britannia Bullion in a regulatory context). It correctly flags, in section 7, that per house-rules Part 4 this triggers mandatory escalation to Lucas before publication. Good practice, not a defect.
- **Tax facts independently checked and confirmed accurate:** CGT rates for 2026/27 (18% basic-rate band / 24% above), £3,000 annual exempt amount, and the VAT 180%-test wording for investment gold coins (HMRC Notice 701/21A) all match what I found from independent sources. The Bank of England's gold-price series ending May 2017 is also independently confirmed.
- **ASA ruling against Montford Group Ltd t/a Britannia Bullion** — independently confirmed: upheld June 2026, over a March 2026 LinkedIn ad, for failing to disclose that physical gold investment is unregulated and that investment value is variable. Matches the dossier's description.
- **Evidence-log smuggling check:** I read the entire dossier looking for any number presented as settled fact despite the missing evidence log. I did not find one — every cost figure is tabled with a source/tier, and the Confidence section states explicitly that nothing here is publishable yet. This is the correct behaviour and matches the researcher's claim 4.

---

## What I couldn't check

- **Spink's and Baldwin's current buyer's-terms pages directly.** My fetch attempts hit a certificate error (Spink buyer T&Cs PDF) and a 403 (Baldwin's terms-for-buyers page). My Finding 2 relies on independent secondary/search sources rather than a primary-source-to-primary-source comparison, so it should be treated as "the dossier's figures don't match what's independently findable," not as definitive proof the dossier is wrong. Someone with direct browser access should pull both pages and settle this.
- **actionfraud.police.uk / reportfraud.police.uk exact wording.** Same 403 problem the dossier itself flags (Open Questions §8.9) — I relied on third-party summaries of the transition, not the live page. This is already correctly flagged by the researcher as needing a human browser check.
- **SGLD, PHGP, RMAU incorporation and OCF figures.** Not individually checked by me either — consistent with the dossier's own Open Questions §8.5/§8.7, which flags these as unverified.
- **LBMA/IBA's exact licensing fee schedule.** Not independently verified in detail; the dossier appropriately escalates the licensing question to Lucas rather than asserting terms, so I didn't need to resolve it to assess the dossier, but I also can't confirm the "requires a paid Usage or Redistribution Licence" characterisation is precisely correct.
- **Insurer-specific home-contents valuables caps.** Not checked — correctly flagged by the dossier as needing a live quote, out of scope for a desk check.
- **WGC/Metals Focus UK bar-and-coin premium data.** Not exhaustively checked; the dossier's own "not conclusively ruled out" framing (Open Questions §8.9/§8.10 — note the dossier numbers two different open questions similarly around WGC data) is honest about this being a partial check.

---

## Summary for the author

Real progress here — the CGT sourcing fix (CG78305/CG76881) is done properly and is now a clean Tier A citation, the evidence-log gap is honestly surfaced rather than papered over, the eBay and Action Fraud corrections both independently check out, and the cost-stack is now genuinely complete with no blank rows. That's four of five claims holding up cleanly.

The fifth (SDRT mechanism) and the buyer's-premium row both have a specific-citation or specific-number problem: in one case the cited HMRC page doesn't contain the claim it's cited for, in the other the specific percentages for two of three named auction houses don't match what's independently findable. Both are fixable without a full rebuild — they need the researcher to re-pull the correct primary sources and quote them directly, the way CG78305 was handled. Until then, this is a **Fix**, not a Pass.
