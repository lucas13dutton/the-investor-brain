# Methodology

**Version 0.2** · Status: approved by Lucas (open decisions settled 17 Sep 2026) · Owner: Lucas

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
2. **Rolling windows:** for each window length, every possible start month in the data. Report the median, the worst and the best.
3. **Event windows** (for example, "bought at the January 2026 gold record") are allowed for storytelling, but must be labelled as event windows and shown next to at least one standard window.
4. The **end date** is fixed per publication cycle, so that every asset in one Everything Index update uses the same end date.

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

1. **Global shares:** the S&P 500 as a total return index (dividends reinvested), converted to GBP at daily rates, with the costs of a typical low-cost UK-available S&P 500 tracker applied.
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
- Every source must be used within its licence terms. No scraping against a site's terms.

### 7.2 Currency and inflation

- All results are in GBP. Foreign prices are converted at the exchange rate on the transaction date.
- Inflation uses the ONS Consumer Prices Index (CPI) throughout, for consistency.

### 7.3 Missing and messy data

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

All settled by Lucas on 17 September 2026.

| Decision | Outcome |
|---|---|
| Default tax scenario for headlines | Taxable, with Sheltered shown alongside where it applies. |
| Inflation measure | CPI (Consumer Prices Index). |
| Standard end date | Month end. |
| Global shares benchmark | The S&P 500 as a total return index (dividends reinvested), converted to GBP at daily rates, with the costs of a typical low-cost UK-available S&P 500 tracker applied. |
| Data threshold | 90% coverage per window is the minimum bar for publication. |
