# Methodology

**Version 0.9** · Status: approved by Lucas (open decisions settled 17 Sep 2026; citation rule, published-vs-interactive scale rule and naming hierarchy added 18 Sep 2026; benchmark implementation, unsourced-cost sensitivity rule, seller-research tier rule, benchmark fund-choice test/result, single-product-dependency rule and interim issuer-factsheet sourcing added 19 Sep 2026; public-data benchmark chain (Damodaran/BoE/ONS), rolling-window frequency rule and Shiller non-adoption added 19 Sep 2026) · Owner: Lucas

This document defines how the company measures, compares and publishes investment returns. Every agent works from it. If a result can't be produced within these rules, it isn't published.

---

## 1. What we measure

### 1.1 The headline metric: Net Real Return (NRR)

**Net Real Return** is the average yearly return an ordinary UK investor would actually have kept, after:

- every cost of buying, holding and selling,
- tax (under a stated tax scenario),
- currency conversion into pounds,
- inflation.

It is always stated together with its **window** (start and end dates) and its **cost scenario** (low, central or high). A number without both is not publishable.

### 1.2 How it is calculated

**Single purchase and sale**

1. Total cash in = purchase price + all buying costs + all holding costs paid, in GBP.
2. Net proceeds = sale price − all selling costs − tax, in GBP.
3. Nominal annual return = (Net proceeds ÷ Total cash in)^(1 ÷ years held) − 1
4. Net Real Return = (1 + nominal annual return) ÷ (1 + average annual inflation over the same window) − 1

**Multiple cash flows** (regular investing, ongoing costs, rental income)

Use the money-weighted return (XIRR) on dated GBP cash flows, then adjust for inflation as in step 4.

**Holding costs paid over time** (storage, insurance, platform fees) are entered as dated cash flows, not lumped into the purchase price, whenever the data allows.

### 1.3 Supporting measures

Every asset result also shows:

| Measure | What it tells the viewer |
|---|---|
| Headline return | The number people usually quote (price change only), for comparison |
| Cost drag | Headline return minus NRR: how much the costs ate |
| Worst window | The worst result across all rolling windows of the same length |
| Largest fall | The biggest peak-to-trough drop in the price series |
| Time to sell | Typical days to sell at a fair price |
| Sell spread | Typical gap between what dealers pay and what they charge |

---

## 2. Reference investor and scenarios

### 2.1 The reference investor

- Lives in the UK and invests in pounds.
- Basic-rate taxpayer, unless a scenario says otherwise.
- Buys and sells through ordinary retail channels (retail platforms, dealers, eBay-type marketplaces, auction houses), not institutional ones.
- Has no special access, discounts or insider knowledge.

### 2.2 Tax scenarios

| Scenario | Meaning |
|---|---|
| Sheltered | Held in an ISA or pension where the asset is allowed there. Not available for most physical assets. |
| Taxable | Held outside any wrapper, basic-rate taxpayer, tax rules as at the analysis date. |

- Tax rules are recorded with the date they were checked and a source.
- Special treatments (for example, rules for personal possessions, or UK gilts and certain coins) are handled per asset in its write-up and must be checked against current HMRC guidance before publication.
- We state the tax scenario. We never tell a viewer what their own tax position is.

### 2.3 Cost scenarios

Every cost has three values, each backed by a source:

- **Low:** a careful, well-informed buyer and seller.
- **Central:** a typical retail investor. This is the default for headlines.
- **High:** a casual buyer using convenient but expensive channels.

---

## 3. The cost stack

Every asset write-up fills in all of these lines. If a cost does not apply, write "none" and say why. A blank line blocks publication.

**Where a cost cannot be sourced** despite a genuine attempt, it is not left blank and does not block publication. Instead it is published as a **labelled sensitivity**: the result is shown both with the cost excluded and with a stated upper bound applied, and that upper bound is explicitly labelled as an assumption, not a verified figure. An invented central figure is never used in its place.

| Stage | Costs to include |
|---|---|
| Buying | Dealer premium or spread, commission, platform fees, stamp duty or VAT, buyer's premium, delivery, authentication or grading |
| Holding | Storage, insurance, platform or account fees, fund charges, maintenance or servicing, mortgage interest, voids, management fees |
| Selling | Seller's fees, marketplace and payment fees, postage and packaging, dealer buy-back spread, agent or legal fees |
| Tax | Tax on gains, income and dividends under the stated scenario |
| Currency | Conversion cost when the asset is priced in another currency |
| Time | Days to sell, recorded separately (not converted into money) |

---

## 4. Time windows

To prevent cherry-picking dates:

1. **Standard windows:** 1, 5, 10 and 20 years, all ending on the same stated end date. Every published asset shows all the standard windows its data covers.
2. **Rolling windows:** for each window length, every available start period at the frequency of the best-licensed data for that asset — monthly where a monthly series is licensed, annual where only an annual series is licensed. **Reasoning (19 Sep 2026):** the purpose of this rule is to prevent a single, hand-picked start date from flattering a result. An annual frequency still satisfies that purpose — it still rolls through every available start point rather than picking one — even though it produces fewer rolling windows than a monthly series would. Report the median, the worst and the best.
3. **Event windows** (for example, "bought at the January 2026 gold record") are allowed for storytelling, but must be labelled as event windows and shown next to at least one standard window.
4. The **end date** is fixed per publication cycle, so that every asset in one Everything Index update uses the same end date.

### Published scale versus interactive comparison

Published content always uses the standard fixed windows (1, 5, 10 and 20 years, all ending on the same stated month end) benchmarked against the S&P 500, so every asset is comparable with every other.

The app additionally offers a user-chosen purchase date, comparing that asset against the S&P 500 from that date and against any other asset the user picks. A user-chosen date is an event window under the rules in this section: it must be labelled as chosen dates for illustration and shown alongside at least one standard window. It may never be used as a published headline.

---

## 5. Items versus indices

Some assets are one price series (an index fund, gold). Others are many separate items (LEGO sets, cards, watches). For item-based assets:

- Report the **median** item, not just the average. Averages can be pulled up by a few big winners.
- Also report the **share of items that lost money** after costs, and the 10th and 90th percentiles.
- **Survivorship bias:** the sample must include items that fell in value or stopped trading. If the data source only lists items that still sell well, say so and treat the result as a best case.
- **Selection rules** (which items are in the sample and why) are written down before the analysis runs, never after seeing the results.

---

## 6. Benchmarks

Every result is shown next to the same three benchmarks, over the same window, using the same method:

1. **Global shares:** the S&P 500 as a total return index (dividends reinvested), converted to GBP, with the costs of a typical low-cost UK-available S&P 500 tracker applied.

   **Benchmark chain, adopted 19 Sep 2026** (superseding the fund-NAV approach tested and briefly adopted earlier the same day — see Decisions log for that history):
   - **Returns:** Aswath Damodaran's annual "Historical Returns on Stocks, Bonds and Bills" dataset (NYU Stern) — its S&P 500 column already includes dividends, i.e. is already a total return series, no further work needed — **Tier B**, free, no login. His own usage-rules text, quoted and dated: **"I am not good at making rules and thus have very few related to the use of my data. I want the data to be widely used and to be a help, rather than a hindrance"**, and, on permission: **"you do not need to explicitly ask me for permission"** (pages.stern.nyu.edu/~adamodar, fetched 2026-09-19). This is annual data, 1928–2025.
   - **Currency:** Bank of England's own published USD/GBP exchange rate statistics, at the period matching each annual data point — **Tier A**.
   - **Inflation:** ONS Consumer Prices Index (CPI), per section 7.2 — **Tier A**.
   - This chain is annual-frequency, not daily — see the rolling-window rule (section 4, item 2), updated the same day to use the frequency of the best-licensed data.
   - **Shiller's dataset (Yale) was investigated and not adopted.** It would be a better technical fit if adopted (monthly, back to 1871), but its current host (shillerdata.com, run by a private company, RSBB-I LLC — the original Yale-hosted page is dead) is genuinely silent on reuse rights: no grant, no prohibition. Silence is not read as permission. Kept as an option if monthly resolution is needed later, once its reuse-rights question is resolved.
   - **Single-source dependency:** implementing the benchmark through one named dataset creates a dependency on that dataset continuing to be maintained and freely usable. If Damodaran's dataset stops being available or its terms change, the benchmark switches to the next-best licensed source (re-running the same fund-NAV and vendor evaluation already done in `dossiers/sp500.md` and `docs/data-licensing.md`, or a newly checked source), the switch is recorded in this Decisions log, and any published figures built on the old source are re-run and go through the corrections process (section 8).
2. **Cash:** an easy-access savings rate series.
3. **Inflation:** so viewers can see whether money kept its buying power.

---

## 7. Data

### 7.1 Source tiers

| Tier | What it is | Use |
|---|---|---|
| A | Official statistics, or licensed actual sale prices | Can support a headline on its own |
| B | Published indices and peer-reviewed or well-documented research | Can support a headline if its method is documented |
| C | Asking prices, single reports, press claims, vendor marketing | Background only. Never the sole support for a published number |

Rules:

- **Asking prices are never treated as sale prices.**
- A source written by someone selling the asset (a dealer, a platform, a tool vendor) is at most Tier C, unless it publishes its underlying data and method.
- **Research published by a firm that sells investment or advisory services is Tier C by default.** Where it names a primary source and an as-of date, it may support a directional, non-headline claim, but never a headline number alone — and two such sources do not make each other independent.
- Every source must be used within its licence terms. No scraping against a site's terms.

### 7.2 Currency and inflation

- All results are in GBP. Foreign prices are converted at the exchange rate on the transaction date.
- Inflation uses the ONS Consumer Prices Index (CPI) throughout, for consistency.

### 7.3 Citations

- Every citation must quote the exact sentence or clause being relied on, taken from the page, plus the date it was accessed. A citation that names only a page or document reference, with no quoted line, is not acceptable.
- If the specific line supporting a claim cannot be found, the claim does not get cited as settled. It moves to Open Questions instead.

### 7.4 Missing and messy data

- Gaps longer than three months in a monthly series are not filled in. The affected windows are marked "insufficient data".
- A window is only published if at least 90% of its expected data points exist.
- Outliers are kept unless they are shown to be errors. Removing a data point requires a note in the evidence log.

---

## 8. The evidence log

Every published number has an entry. No entry, no publication.

| Field | Content |
|---|---|
| Claim ID | Unique reference |
| Claim | The exact number or statement as published |
| Asset and window | What it is about |
| Cost and tax scenario | Which scenario was used |
| Sources | Each source, its tier, and the date accessed |
| Calculation | Link to the code or notebook that produced it |
| Checked by | Which agent checked it, and Lucas's approval |
| Published in | Video, newsletter or page, with dates |
| Status | Live, corrected or withdrawn |

Corrections are logged, never silently edited, and listed on a public corrections page.

---

## 9. Strategy Lab rules

1. **Paper portfolios only.** No real money is traded on behalf of the company or its audience.
2. **Pre-registration:** a strategy's rules, assets, start date and success test are written down and date-stamped before testing.
3. **No look-ahead:** a strategy may only use information that was available on each decision date.
4. **Out-of-sample testing:** tune the rules on one period, and judge them only on a later period they never saw.
5. **Full costs** from this methodology, central scenario, on every trade.
6. **Kill rule:** a strategy that fails its pre-registered test is retired and reported, not tweaked until it passes.
7. Results are labelled as research on historical data. They are never presented as signals or a suggestion to act.

---

## 10. Publication standards

- Each published figure states its window and cost scenario on screen.
- Round returns to one decimal place (percentages) and money to sensible whole units.
- Every piece of content carries a visible risk line: past results do not predict future ones, and the value of investments can fall as well as rise.
- We describe what happened and what it cost. We do not say what any viewer should buy, sell or hold.

---

## 11. Changing this document

- Changes are made through the repo, with a note explaining why.
- The version number goes up with every change.
- When a change affects published results, affected results are re-run and any differences go through the corrections process.

---

## Decisions log

Settled by Lucas.

| Date | Decision | Outcome |
|---|---|---|
| 17 Sep 2026 | Default tax scenario for headlines | Taxable, with Sheltered shown alongside where it applies. |
| 17 Sep 2026 | Inflation measure | CPI (Consumer Prices Index). |
| 17 Sep 2026 | Standard end date | Month end. |
| 17 Sep 2026 | Global shares benchmark | The S&P 500 as a total return index (dividends reinvested), converted to GBP at daily rates, with the costs of a typical low-cost UK-available S&P 500 tracker applied. |
| 17 Sep 2026 | Data threshold | 90% coverage per window is the minimum bar for publication. |
| 18 Sep 2026 | Published scale vs. interactive comparison | Published results use fixed windows; user-chosen purchase dates are an interactive app feature only. |
| 18 Sep 2026 | Naming hierarchy | Confirmed: Asset Theory (company, app, channels, subscription), Research (evidence library), Asset Autopsy (comparison feature and video series), Strategy Lab (strategy testing). |
| 19 Sep 2026 | Global shares benchmark implementation | The benchmark is implemented as the NAV total return of a named low-cost, accumulating, UK-available S&P 500 tracker, cited to the issuer at Tier B, rather than S&P Dow Jones Indices' own index series directly. This avoids needing an index data licence. The index remains the conceptual reference. |
| 19 Sep 2026 | Benchmark fund choice, tested and confirmed | Adopted the rule that the benchmark fund is whichever has the longest continuous, downloadable, citable daily NAV history, with cost and durability as tie-breakers. Tested Fidelity Index US Fund (P Acc) against iShares Core S&P 500 UCITS ETF (CSPX) the same day: CSPX's own download tool gives only ~21 months of daily NAV despite a 16-year trading history; Fidelity's downloadable-history status could not be confirmed either way (one page was inaccessible, not found empty). Held Fidelity Index US Fund as the benchmark rather than switch to a confirmed-shorter alternative. Both funds' licence terms for reusing NAV data to calculate a derived figure are unresolved and flagged to Lucas. If CSPX had won, Fidelity Index US Fund would have been kept only as the low-cost OEIC cost-stack example, not the benchmark. |
| 19 Sep 2026 | Unsourced-cost sensitivity rule | Where a cost cannot be sourced, it is published as a labelled sensitivity showing the result with and without a stated upper bound, never as an invented central figure. Unsourced costs no longer block publication, provided the sensitivity and its label are shown. |
| 19 Sep 2026 | Seller-research source tier rule | Research published by a firm that sells investment or advisory services is Tier C by default. Where it names a primary source and as-of date, it may support a directional, non-headline claim, but never a headline number alone, and two such sources do not make each other independent. |
| 19 Sep 2026 | Interim issuer-factsheet sourcing — investigated, not adopted | Checked whether CSPX's and Fidelity Index US Fund's own factsheets/KIIDs publish fixed-period, NAV-based, net-of-charge, dated, quotable total returns, as a possible interim benchmark source pending a full data licence. Mixed result: CSPX's factsheet and KIID confirm this for its 1-year and 5-year windows only (no 10-year figure exists; 20-year is structurally impossible, as the fund only launched in May 2010). Fidelity Index US Fund's equivalent documents returned 403 on every attempt, and its retail web page states trailing returns with no statement of NAV basis or net-of-charge treatment. Since Fidelity is the actual benchmark fund, this does not clear the bar for adoption — no interim fixed-window source is adopted. `dossiers/sp500.md` records the full findings in Open Questions §8.10; sections 1.1 and 5 are unchanged. |
| 19 Sep 2026 | Rolling-window frequency rule | The rolling-window rule (section 4, item 2) now runs at the frequency of the best-licensed data for the asset, not necessarily monthly. Reasoning: the rule's purpose is to stop a single hand-picked start date being used, and rolling through every available annual start point still satisfies that purpose, even with fewer windows than a monthly series would give. Adopted so an annual-only licensed source (see the next decision) can still be used for rolling-window analysis. |
| 19 Sep 2026 | Global shares benchmark chain adopted: Damodaran + Bank of England + ONS | Superseding the same-day fund-NAV approach. Returns: Aswath Damodaran's annual S&P 500 total-return series (NYU Stern, Tier B, free), already dividend-inclusive, 1928–2025 — his usage-rules text quoted and dated: "I want the data to be widely used and to be a help, rather than a hindrance" and "you do not need to explicitly ask me for permission" (fetched 2026-09-19). Currency: Bank of England USD/GBP exchange rate statistics (Tier A). Inflation: ONS CPI (Tier A), per section 7.2. This chain is annual, not daily, hence the rolling-window frequency rule above. |
| 19 Sep 2026 | Shiller's dataset — investigated, not adopted | Would be the better technical fit (monthly, back to 1871) but its current host (shillerdata.com, a private company, RSBB-I LLC — the original Yale page is dead) is silent on reuse rights: no grant, no prohibition. Silence is not read as permission. Not adopted for now; kept as an option if monthly resolution is needed later, once its reuse-rights question is resolved. |
