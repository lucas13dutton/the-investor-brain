# Asset Scorecard: factor research and proposed method

**Status:** research note, not a decision — **escalated to Lucas for approval before anything is built.**
**Date checked:** 2026-09-21
Built per `docs/methodology.md` and `docs/house-rules.md`. Where this note and those documents disagree, the documents win.

This answers a narrower question than "how do we rate assets": what factors can this company measure, honestly and from data it already collects, that describe an asset class without forecasting its future returns or rating any individual security within it. It's written to support the planned **Asset Scorecard** product (see `docs/products.md`), but does not itself build that product — see "Escalation to Lucas" at the end.

---

## 1. How professional and academic sources characterise asset classes

A genuinely wide range of institutions publish frameworks for describing — not forecasting — an asset class. Three real ones, checked directly for this note:

- **FCA Consumer Duty, "price and value" outcome.** The FCA's own description of this outcome (fetched directly from `fca.org.uk/firms/consumer-duty/about`, 2026-09-21) states firms must ensure **"the price a customer pays for a product or service is reasonable compared to the overall benefits they receive,"** considering **"benefits, limitations and non-financial costs."** This is a regulator, not an academic source, but it's directly relevant: it frames cost as something to be judged *relative to* what an investor actually gets, not in isolation — which is why the factor below is "cost as a share of return," not just "cost."
- **The CFA Institute curriculum's standard way of introducing asset classes** (general, well-established professional-education material, not a single quotable page fetched for this note — flagged honestly rather than dressed up as a direct citation) typically distinguishes asset classes by return, risk/volatility, correlation to other asset classes, income generation, inflation-hedging behaviour, and liquidity. Several of those — volatility "going forward," correlation used for portfolio construction — are explicitly forward-looking or advice-adjacent uses, which is exactly the territory this company's factors must stay out of (see section 2).
- **Fund-rating and benchmark-governance practice more broadly** (Morningstar-style cost/liquidity classifications; IOSCO's Principles for Financial Benchmarks on data transparency and governance) treats *cost*, *liquidity*, and *data quality/transparency* as legitimate, purely descriptive axes distinct from any performance rating — this note leans on that same separation rather than on a single fetched source, since attempts to fetch specific Morningstar/IOSCO methodology pages for this note returned errors (404/403) and are not cited as if verified; the concepts referenced are standard, uncontested industry practice, not a specific disputed claim.

**The common thread, useful for this company specifically:** every serious framework separates *descriptive* characteristics (what actually happened, what it actually costs, how tradeable it actually is) from *predictive* ones (what it's expected to return, how it's rated for skill or credit quality). This company's evidence-log discipline — every number traces to a real, dated source, and nothing is asserted about the future — already sits naturally on the descriptive side. The factors below are chosen because they're extensions of data this company already collects for its dossiers and `costs/benchmark/`-style calculations, not a new research programme.

---

## 2. What's explicitly excluded, and why

Per the task's constraint, no recommended factor may require forecasting future returns or rating an individual security. Excluded, with the reasoning:

- **Expected or forecast return** (of any kind — "expected annual return," implied yield-to-maturity as a forward return estimate, etc.) — a forecast by definition.
- **Star ratings, analyst buy/sell/hold calls, "quality" or "conviction" scores** — these rate individual funds/managers/securities, and usually embed a forecast of future skill.
- **Credit ratings of individual bonds or issuers** — rates a specific security, not the asset class, and is itself a third-party forward-looking judgment this company didn't produce or verify.
- **Volatility *forecasts*** (e.g. implied volatility, VIX-style forward-looking risk measures) — as opposed to *historical* volatility/drawdown, which is descriptive and is included below.
- **Momentum or technical signals** — by construction, an implicit prediction of near-term price direction.
- **ESG or "sustainability" scores** — these are third-party subjective judgments, not measured facts this company has independently verified, and they routinely embed forward-looking claims about risk or impact.
- **Correlation to other asset classes** — considered and left out for now, not on principle (a purely historical correlation figure would be genuinely descriptive) but because it needs overlapping historical return series across many asset pairs at consistent frequencies, which this company's dossiers don't yet consistently provide. Worth revisiting once more than two or three assets have a `costs/benchmark/`-style historical calculation built, not before.

---

## 3. Recommended factors (7), each measurable today or with modest, already-planned tooling

Every factor below is computed from data this company already collects — a dossier's cost stack (`docs/methodology.md` section 3), its time-to-sell figure (section 3.5), its tax treatment (section 2.2), its item-vs-index classification (section 5), or the evidence log itself (`data/evidence/evidence.csv`) — not from a new external data source or a subjective judgment call.

### 3.1 Cost drag
**What it measures:** how much of an asset's gross historical return its own cost stack consumes.
**Method:** the central-cost-scenario figure already required in every dossier's section 3, annualised over a stated standard holding period (10 years, per methodology section 4's standard windows) — one-off buying/selling costs amortised over the period plus annual holding costs, summed. Where a full historical rolling-window calculation exists (as now built for the S&P 500 in `costs/benchmark/`), the actual computed gap between the gross and cost-adjusted nominal annual return is used directly instead of the amortised estimate, since it's a stronger, historically-real figure.
**Scale:** a continuous annualised percentage, displayed banded for readability: <0.5% / 0.5–1.5% / 1.5–3% / >3%.
**Why it's descriptive, not predictive:** every input is a currently-quoted or historically-realised cost, never a projection of what costs will be.

### 3.2 Liquidity (time to sell)
**What it measures:** how long it typically takes to convert the asset to cash at a fair price.
**Method:** taken directly from the dossier's section 3.5 low/central/high days-to-sell figures — already a required field for every dossier.
**Scale:** a plain ordinal band — same-day, days (1–7), weeks (1–4), months (1+) — not a numeric forecast of future liquidity conditions.
**Why it's descriptive, not predictive:** it states how long selling has actually taken historically or currently takes by the product's own rules (e.g. a fixed-rate bond's notice period), not a prediction of market conditions at some future sale date.

### 3.3 Historical drawdown
**What it measures:** the worst real-terms loss actually observed over the shortest standard window (1 year), for assets with a historical return series.
**Method:** directly reuses the rolling-window calculation methodology already built for the S&P 500 benchmark (`costs/benchmark/build_benchmark.py`) — the worst single 1-year rolling window's net real return in the available history. Applied to any other asset once (and only once) it has an equivalent historical series.
**Scale:** a percentage (the worst observed 1-year real return), with an explicit "insufficient history" flag rather than a number when an asset's data history is too short to compute this reliably (this is a data-availability caveat, not a stand-in forecast).
**Why it's descriptive, not predictive:** it reports what has actually happened in the worst historical window on record — explicitly not a Value-at-Risk-style forward estimate.

### 3.4 Dispersion of historical outcomes
**What it measures:** how wide the spread of real returns has been across all available historical starting points, at a fixed window length.
**Method:** best-window return minus worst-window return (plus the median), at the 10-year standard window length, using the same rolling-window rule already in methodology section 4 (every available start point at the frequency of the best-licensed data for that asset).
**Scale:** a percentage-point spread, banded narrow / moderate / wide, calibrated once more than one or two assets have this computed (do not invent band cut-offs from a single asset's data).
**Why it's descriptive, not predictive:** it's a historical fact about how different an investor's outcome would have been depending on start date — not a probability distribution projected forward.

### 3.5 Tax treatment and shelter eligibility
**What it measures:** (a) whether the asset can be sheltered from UK tax at all, and (b) where a full calculation exists, how much of its historical return tax actually removes.
**Method:** (a) a categorical fact taken directly from the dossier's section 4 — ISA-eligible, SIPP-eligible, or neither; (b) where both a Sheltered and a Taxable scenario have been fully computed (as now exists for the S&P 500 in `costs/benchmark/`), the percentage-point gap between the two scenarios' net real returns at the 10-year standard window.
**Scale:** categorical for (a); a percentage-point gap for (b) where available.
**Why it's descriptive, not predictive:** UK tax rules and wrapper eligibility are current facts with a checked date (per methodology section 2.2), and the tax gap, where computed, is drawn from realised historical returns, not a projection of future tax policy.

### 3.6 Data quality / evidence strength
**What it measures:** how well-evidenced this company's own dossier for the asset actually is — genuinely unique to this company, since it's a fact about our own sourcing discipline, not the asset itself.
**Method:** mechanically counted from `data/evidence/evidence.csv`, filtered to the asset — the share of `claim`-type rows that are Tier A, Tier B and Tier C, plus the share flagged `NEEDS RE-VERIFICATION` or `withdrawn` with no replacement yet.
**Scale:** a published breakdown, e.g. "82% Tier A/B sourcing, 3% flagged for re-verification, 0 unresolved withdrawn claims" — not a single composite score, since collapsing tier mix and open-item counts into one number would hide exactly the kind of gap this company's evidence-log discipline exists to surface.
**Why it's descriptive, not predictive:** it is a literal, automatable count of this company's own existing records — no judgment call, no external rating.

### 3.7 Structural/selection-bias exposure
**What it measures:** whether the asset's price history comes from a broad index (low survivorship-bias risk) or from individually selected items (higher risk, requiring a disclosed sampling rule).
**Method:** a categorical fact taken directly from the dossier's section 6 — "index-based" or "item-based" — plus, for item-based assets only, the dossier's own disclosed median-item, share-of-items-that-lost-money, and 10th/90th percentile figures (already required by methodology section 5 wherever the asset is item-based).
**Scale:** categorical (index-based / item-based) plus, for item-based assets, the percentile spread already on record.
**Why it's descriptive, not predictive:** it states a structural fact about how the asset's data is constructed, and reports percentile figures already computed from historical transactions — it does not predict which future item would outperform.

---

## 4. What this note deliberately does not decide

- **Whether to combine these seven factors into a single composite score.** A weighting scheme (e.g. "cost matters twice as much as liquidity") embeds a value judgment about what matters to an investor, which risks tipping a purely descriptive scorecard into an implicit recommendation — the exact thing `docs/products.md` says the Asset Scorecard must never do. The default assumption in this note is that the scorecard shows all seven factors side by side, unweighted and uncombined, but this is itself a decision for Lucas, not assumed here.
- **The exact visual scale/banding cut-offs** for cost, drawdown and dispersion — deliberately left uncalibrated until more than the current two assets (`sp500`, `gold`) have full historical figures computed, so bands aren't accidentally fitted to one asset's numbers.
- **Which assets get a Scorecard entry first**, or how an asset with no historical return series (e.g. cash, most of buy-to-let) is scored on 3.3/3.4 — flagged as an open question, not resolved here.

---

## Escalation to Lucas

This note recommends seven factors and stops there, per the task's own instruction: **do not build anything until this is approved.** Specifically needing a decision:

1. Are these seven factors the right set, or should any be dropped, or correlation-to-benchmark (section 2, "excluded... for now") be added back once the data exists?
2. Should the Scorecard show factors side by side (this note's default assumption) or as some combined score — and if combined, who decides the weights, and how is that decision itself disclosed to a viewer, given the risk of implying a recommendation?
3. How should assets with no historical return series (most of cash, buy-to-let) be shown for the two history-dependent factors (3.3, 3.4) — blank, "insufficient history," or excluded from the Scorecard until a series exists?

No dossier, evidence-log row, or product code has been changed to build the Scorecard itself in this pass.
