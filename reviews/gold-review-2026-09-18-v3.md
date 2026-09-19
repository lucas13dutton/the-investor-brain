# Skeptic re-review: Gold dossier — scoped verification of the citation-format pass (methodology v0.3 §7.3)

**Reviewed:** `dossiers/gold.md` · **Date:** 2026-09-18 · **Reviewer:** skeptic agent
**Scope:** This review covers **only** the citation-format pass described at the top of the dossier and in Open Questions items 11–19. It does not re-litigate the underlying cost-stack, tax or risk conclusions already passed across `reviews/gold-review-2026-09-18.md` (Fix) and `reviews/gold-review-2026-09-18-v2.md` (Pass, scoped to three surgical fixes). Those prior verdicts stand. The only questions in scope here are: (a) was the new §7.3 citation rule actually applied — quote + access date, not a bare reference — and (b) were the two "source now disagrees" cases (eBay international fee, HL £11.95 dealing charge) handled honestly rather than left as silent contradictions.

---

## Verdict: **Fix**

The research underlying this pass is honest — every quote I independently checked (a sample spanning HMRC, HL, AJ Bell, eBay, Royal Mint, Chards, goldsilver.com) matches the live or recently-live source, and nothing looks fabricated or paraphrased-as-verbatim. The two headline "source now disagrees" cases (eBay international fee, HL dealing charge) are narrated honestly in prose and correctly logged as new Open Questions. But the pass is incomplete in a way that matters: it left the actual cost-stack table values unchanged in at least six places while its own Open Questions section says those same values are unquoted or contradicted by the current source — exactly the defect the brief warned about — and it introduces/leaves a set of internally inconsistent Open Questions cross-references that the dossier explicitly (and incorrectly) claims are now fixed. Neither defect is fatal — the dossier is already self-blocked pending the missing evidence log — but "citation-format pass" isn't complete until the tables agree with the Open Questions section they point to.

---

## Findings

### 1. [Critical] The two named "source now disagrees" figures are still asserted as fact in the cost-stack tables, not just flagged in the source column

**eBay international fee (§3.3, "Marketplace and payment fees" row, Central column):**
> "£0 for a UK-to-UK private-seller sale on eBay; **~12.8% + 30p per order** if the private seller sells to a buyer outside the UK"

The adjacent Source cell and Open Questions §8.11 both say a direct fetch of eBay's own page instead states a flat **3%** international fee, and that "no quotable line supporting the original figure was found." I independently fetched eBay's private-seller fee page myself and confirmed: *"If your registered address is in the UK, we charge an international fee of 3% if the delivery address for the item... is outside the UK."* There is no ambiguity here — the dossier's own research establishes the 12.8%+30p figure is wrong or stale, yet the Central-column cost value a reader (or a downstream NRR calculation) would actually use still says 12.8%+30p.

**HL £11.95 dealing charge (§3.6, "Commission" row, High column):**
> "£11.95+ (infrequent-trader rate on some platforms, e.g. Hargreaves Lansdown)"

The Source cell and Open Questions §8.14 say HL's own charges page "instead states dealing is 'never more than £6.95 per online deal.'" I independently confirmed via search of HL's live charges page that HL cut this rate from £11.95 to £6.95 (with a further cut to £3.95 after 20+ trades/month) **effective 1 March 2026** — before this dossier's stated "date checked" of 2026-09-18. So this isn't just "unconfirmed," it's a stale figure the researcher's own citation work proves is wrong as of the analysis date, and it is still sitting in the High column as if it were the current cost.

Per methodology §7.3 ("If the specific line supporting a claim cannot be found, the claim does not get cited as settled. It moves to Open Questions instead") and the task brief's explicit instruction, a citation-format pass should not leave a table row asserting a number its own Open Questions section says is contradicted. Both cases fail this. **Fix:** either strike the specific figure from the table cell and replace with "see Open Questions §8.11/§8.14" (matching how other rows in this same dossier handle a genuinely unsettled figure, e.g. the "not reliably quantified" wording used for auction vendor's commission in §3.3), or update the cell to the now-known correct figure (3%; £6.95) with a note that it supersedes the earlier draft's number.

### 2. [Major] The same table-vs-Open-Questions contradiction recurs in at least four more of the nine new items

This is not limited to the two cases named in the brief. I checked all nine new Open Questions items (11–19) against their corresponding table cells:

| Item | Table location | Table still asserts | Open Questions says |
|---|---|---|---|
| §8.12 Royal Mail postage | §3.3 "Postage and packaging" | Central £10–£20, High £30+ | "currently rest on a third-party paraphrase, not a quoted line from Royal Mail's own site... not treated as settled" |
| §8.13 iShares SGLN spread | §3.6/§3.10 "spread" rows | ~0.03% / ~0.05–0.10% / 0.2%+ | "no quotable primary-source line was obtained... moved to Open Questions" |
| §8.15 HL FX charge | §3.6 "Platform fees / FX fee", High | "1%+... on the first £10,000" | "not reconfirmed with its own quoted line in this pass" |
| §8.17 HL platform fee upper bound + ISA cap | §3.7 "Platform or account fees", High | "0.35–0.45% p.a. ... capped at £150/year in an ISA" | "the 0.45% upper bound and the £150/year cap are moved to Open Questions §8.17, since no quoted line was found for them" |

For §8.17 specifically, my own check (see Finding 1) found HL actually cut its platform fee cap from 0.45% to 0.35% on 1 March 2026 — so, as with the dealing charge, this is likely not merely "unconfirmed" but superseded, and it's still presented in the table as the current High-scenario cost.

Items §8.16 (VAT "outside scope" claim) and §8.19 (tungsten-core detail, see Finding 3) show a milder version of the same pattern. Only item §8.18 (LBMA licensing clause, which is descriptive prose rather than a cost-stack number) avoids it.

**Fix:** every one of these table cells needs the same treatment recommended in Finding 1 — either strike/qualify the figure in the cell itself, or update it to a reconfirmed number. Six of nine new Open Questions items currently describe a contradiction the table doesn't show.

### 3. [Major] Open Questions cross-reference numbering is not internally consistent, contrary to what the dossier claims

The dossier states in §7: "flagged in Open Questions §8.8 (corrected in this citation-format pass from an earlier mis-numbered reference to §8.9, which is actually the separate World Gold Council item)." I confirmed this one fix is correct — §8.8 is indeed the Action Fraud item and §8.9 is indeed the WGC item.

But this is the only one of five similar cross-references that was fixed. I found four more instances of the identical error, apparently pre-existing and never checked in this pass:

- §4.3 (ISA eligibility sentence) points to **"Open Questions §8.5"** — but item 5 is the SDRT-non-UK-incorporation item, not ISA eligibility (which is item **4**).
- §3.6 (Stamp duty/SDRT row) points to **"Open Questions §8.6"** — but item 6 is the insurer-cover-limits item, not SDRT-for-other-issuers (item **5**).
- §3.2 (Insurance row) points to **"Open Questions §8.7"** — but item 7 is the OCF-for-other-ETCs item, not insurance (item **6**).
- §3.7 (Fund charges/OCF row) points to **"Open Questions §8.8"** — but item 8 is the Action Fraud item, not OCF-for-other-ETCs (item **7**). This creates an actual collision: two unrelated claims (Action Fraud wording in §7, and un-pulled OCF figures in §3.7) both cite "§8.8," and only one of them is right.

So the dossier's claim that the numbering "is now internally consistent" is not true — one link in a five-link chain was fixed, the other four (all off by exactly one, in the same direction) were not. **Fix:** renumber every in-body §8.x pointer to match the actual Open Questions list (§4.3→§8.4, §3.6 SDRT row→§8.5, §3.2 Insurance row→§8.6, §3.7 OCF row→§8.7), and re-check the whole document for this class of error rather than fixing the one instance a prior review happened to name.

### 4. [Major] Some of the "already compliant, left as-is" citations don't actually carry the access date at the point of use

The task named five citations as "already compliant, left as-is": HMRC CG76881, CG78305, STSM031090, Noonans' buyer's premium, and the Bank of England series note. I checked all five for quote + date co-located at the point the claim is made (not just somewhere in the document):

- **STSM031090** (§4.3): quote is given in full, and the paragraph ends "fetched directly **2026-09-18**." Compliant.
- **Noonans 24% premium** (§3.1): quote given, "fetched directly **2026-09-18**" attached in the same cell. Compliant.
- **CG76881** (§4.1): quoted ("coins and bank notes which are sterling currency are not chargeable assets") but the in-line attribution says only "confirmed by direct fetch" — **no date anywhere in that sentence or bullet**. The date ("accessed 2026-09-18") exists only in the separate §9 Sources list.
- **CG78305** (§4.1): quoted, but the in-line attribution says only "fetched directly for this rebuild" — again **no date in that passage**. Date recoverable only from §9.
- **Bank of England series-end note** (§5, price-data table): quoted ("they are based on daily observations until May 2017 when the series ends") but **no date given in the table cell**; the date appears only in the §9 entry.

The underlying quotes are all accurate (I independently verified CG76881/CG78305 wording is consistent with what the two prior skeptic reviews already confirmed by direct fetch), so this isn't a fabrication problem. But it is a real, checkable inconsistency in how the new rule was applied: some citations carry quote+date together at the point of the claim; others carry the quote at the point of the claim and make the reader flip to §9 for the date. Given the explicit purpose of §7.3 (make every claim checkable without hunting), this is worth fixing for consistency, particularly since two of the three named-as-fine examples fail it.

**Fix:** add the access date directly alongside the quote in §4.1 (both CG76881 and CG78305 bullets) and in the §5 Bank of England table cell, matching the pattern already used correctly for STSM031090 and Noonans.

### 5. [Minor] Tungsten-core counterfeiting detail is stated as fact, then retracted in the same breath

§7 states as an unqualified fact: "convincing fakes exist using tungsten cores (which can pass simple weight checks) as well as gold-plated base metal." Only later in the same bullet does the text add: "The specific detail that fakes commonly use tungsten cores could not be traced to a quotable line on Chards' or Bleyer Bullion's own site in this pass... moved to Open Questions §8.19 and treated as background, not a settled cited fact." Less serious than Findings 1–2 (the caveat is at least in the same paragraph, visible to any reader, not hidden behind a table/appendix split), but the claim should have been hedged the first time it was written ("widely reported, though not independently verified here, to include tungsten-core fakes"), not asserted then walked back.

### 6. What checked out cleanly

- **No fabricated or paraphrased-as-verbatim quotes found** in the sample I independently checked: AJ Bell dealing (£5.00) / platform (0.25%, £3.50/month cap) / FX (0.75%/0.5%/0.25% tiers) charges page; HL's "never more than £6.95" and "maximum you pay in a year is 0.35%" figures (and independently confirmed, via search, that these reflect a genuine 1 March 2026 fee cut from £11.95/0.45%, which corroborates rather than undermines the dossier's own Open Questions items 14 and 17); eBay's private-seller UK-free and 3%-international wording, fetched directly and matching the dossier's quote word for word; Royal Mint's 1%+VAT / 2%+VAT storage fee wording; Chards' forgery-guide quote; goldsilver.com's buyback-spread quote; and gov.uk's CGT rate/allowance figures and the ASA ruling against Montford Group Ltd. All matched.
- **STSM011020 no longer appears as a live citation anywhere.** A full-text search found it only in three places, all explicitly framed as "this was the earlier wrong citation, now corrected to STSM031090" — the correct way to record a fix, not a lingering error.
- **The two headline contradiction cases were narrated honestly**, not hidden. Both the eBay 12.8%+30p figure and the HL £11.95 figure are openly flagged in their Source cells and get their own numbered Open Questions entries with an honest account of what the live source now says. The failure is that the fix stopped one layer short of the table cell itself (Findings 1–2), not that it was concealed.
- **No evidence of a silently changed conclusion, number or tier** beyond the nine disclosed downgrades. I don't have a diff tool available (see below), but a full manual read cross-checked against the two prior reviews' record of settled facts (CGT rates/allowance, VAT 180% test, eBay business-seller fee schedule, SDRT non-UK-incorporation mechanism, ASA ruling, Action Fraud correction, Noonans 24%) found all of these unchanged in substance from what was already passed.

---

## What I couldn't check

- **No git-diff/Bash access.** I could not mechanically diff the current file against the pre-citation-pass commit to get an automated guarantee that nothing besides citation format and the disclosed nine downgrades changed. I relied on a full manual read plus cross-checking against the two prior review documents' record of settled numbers/tiers/conclusions. This is weaker than a line-level diff — flagged explicitly rather than asserted as certain.
- **Spink's and Baldwin's of St James's buyer's-premium pages, Royal Mail's insured-parcel pages, the iShares SGLN factsheet/product page, HMRC's VATFIN manual/VAT Notice 701/49 clause on ETC dealing, and the ICE Benchmark Administration PDF's licensing clause.** I attempted a couple of these myself (Royal Mint direct URL, an HL sub-page) and hit the same dead-link/403 problems the dossier already documents; I did not exhaustively re-attempt all of them, since this scoped review's job was to check how the citation rule was applied and how contradictions were handled, not to complete the underlying primary-source research the dossier already flags as open.
- **Noonans' page via a raw fetch of my own.** Confirmed only via search-indexed content attributed to noonans.co.uk, same limitation the v2 skeptic review reported.

---

## Bottom line

This is a genuine, honest citation-format pass — the new quotes are accurate, the two named contradictions are disclosed rather than hidden, and STSM011020 is fully retired as a live citation. It is not yet complete: six cost-stack table cells still show figures the dossier's own Open Questions section says are unquoted or actively contradicted by the current source (most seriously the eBay 12.8%+30p and HL £11.95 figures named in the brief, both of which the researcher's own research shows are simply wrong as of the analysis date), and four Open Questions cross-references are mislabeled in a way the dossier incorrectly claims is fixed. Neither defect changes the dossier's overall publication status — it remains blocked on the missing evidence log regardless — but the citation-format pass itself needs one more round before it can be called done.
