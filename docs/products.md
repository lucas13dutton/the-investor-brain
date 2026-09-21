# Products

**Status: draft specs. None of the three is built.** This document describes what each is intended to do, so that what gets built matches what the brain already promises in `docs/methodology.md` and `docs/house-rules.md`. Nothing here is a commitment to a build date.

These are five surfaces of the Asset Theory brand — see the "Naming" section in the root `README.md` for the full naming hierarchy.

> **Hard constraint on the Asset Scorecard and Portfolio X-ray, specifically:** neither tool may ever produce a personalised recommendation, a forecast of future performance, or a rating of an individual security (a specific fund, ticker, property or item). Both describe asset *types*, or a user's own existing holdings, using historical and current data only. Both require a UK financial promotions specialist review before launch, per `docs/house-rules.md`'s existing rule that a specialist reviews any paid-adjacent or user-facing product before it ships. These two constraints are stated once here and referenced, not restated in full, in each product's own "Compliance constraints" section below.

---

## Research

The evidence library: studies, methods, sources, findings.

### What it does

Readers explore what each study found: the reasoning behind it, the cost models used, and the evidence behind every number. Every claim on the page links to its entry in the evidence log. The purpose is to make the brain's workings inspectable — showing the work, not just the headline — which is the trust moat: anyone can check a number instead of taking it on faith.

### Who it's for

Readers who want to understand *why* a result is what it is, not just see it — people checking a claim, researching an asset before a video ships, or deciding whether to trust the channel at all.

### What it draws on

| Part of the brain | How it's used |
|---|---|
| `dossiers/*.md` | The written explanation, cost stack, tax treatment, price data sources, and risks for each asset. |
| `costs/` | The cost models behind the low/central/high figures shown in each dossier. |
| `data/evidence/evidence.csv` | Every numeric claim on the page links to its `claim_id` row: sources, tiers, who checked it, who approved it. |
| `lab/` | Strategy Lab results, where a study draws on one, labelled as paper-portfolio research per `docs/methodology.md` section 9. |

### What has to exist before it can be built

- A dossier passing skeptic review for at least one asset (done for gold; see `dossiers/gold.md` and its reviews).
- The evidence log actually populated and passing `data/evidence/validate.py` for that asset's published claims — not just logged as draft.
- A settled decision on which claims are cleared to publish (`approved_by` filled in), since this is a publishing surface, not a research scratchpad.
- A stable page/URL structure per asset, so evidence-log links are durable.

### Compliance constraints

- No recommendations: describing what a study found is not the same as saying what to do with it. No "so buy..." framing anywhere on the page.
- No personalised output: the same page for every reader, regardless of who's viewing it.
- No signals: no "as of today" framing that reads as a timing cue. Historical findings only, per `docs/house-rules.md`.
- Carries the standard risk line for its format (newsletter/website footer line, per the mandatory risk lines in `docs/house-rules.md`).

---

## Asset Autopsy

The comparison layer: "Compare assets."

### What it does

Users compare any two or more assets against each other and against the S&P 500, over the standard fixed windows or a chosen purchase date, with costs applied and adjustable between the low, central and high scenarios (`docs/methodology.md` section 2.3). It shows the headline return and the Net Real Return side by side, so the cost drag is visible, not hidden.

Per `docs/methodology.md`'s "Published scale versus interactive comparison" (section 4): a user-chosen purchase date is an event window under the existing rules. It must be labelled as chosen dates for illustration and shown alongside at least one standard window, and it is never used as a published headline — it's an interactive result the user generated themselves, not something the company publishes.

### Who it's for

Anyone who wants to run their own "what if I'd bought X instead of Y" comparison, rather than wait for a published video to cover that exact pairing.

### What it draws on

| Part of the brain | How it's used |
|---|---|
| `dossiers/*.md` | Which assets are available to compare, and their cost stacks. |
| `costs/` | The low/central/high cost figures applied to each asset in the comparison, per the user's chosen scenario. |
| `data/evidence/evidence.csv` | Only claims that are cleared (approved, non-draft) feed a live comparison — an unapproved or Tier-C-only figure shouldn't silently power a user-facing result. |
| `lab/` | Not used directly — Strategy Lab is paper-portfolio research, not a live comparison tool, and the two must stay visibly separate. |

### What has to exist before it can be built

- At least two assets with dossiers, cost models and evidence-log entries good enough to be marked cleared for use in a live tool, not just published narrative.
- A benchmark data feed for the S&P 500 total-return series in GBP, per the decisions log's global-shares benchmark decision.
- A defined data pipeline for the user-chosen-date feature: a live or near-live price series per asset, not just the historical windows used in published content.
- The app's version of the mandatory risk line, wired to appear on every comparison result (see `docs/house-rules.md`, "App, on any comparison result").

### Compliance constraints

- No recommendations: the tool shows what happened, never "you should hold X."
- No personalised output: it computes from the inputs the user chooses (assets, dates, scenario), not from anything about who the user is (age, income, goals). Any future account/profile feature would need its own compliance review before use in Asset Autopsy.
- No signals: no alerts, no "buy now" styling, no notification that a comparison has moved in the user's favour.
- Carries the app comparison risk line on every result, every time, per `docs/house-rules.md` mandatory risk lines.

### Naming note

Asset Autopsy is deliberately the name of both this feature and the short-form video series. The series functions as a preview and on-ramp for the tool, so the shared name is intentional, not a collision to resolve.

---

## Strategy Lab

The strategy testing layer.

### What it does

Runs pre-registered paper portfolios that test investing strategies against historical data, under the rules in `docs/methodology.md` section 9: rules, assets, start date and success test written down before testing; no look-ahead; tuned on one period and judged only on a later one it never saw; full costs applied at the central scenario on every trade; and a kill rule — a strategy that fails its pre-registered test is retired and reported, not tweaked until it passes. Results are always labelled as research on historical data, never as signals or a suggestion to act.

### Who it's for

Readers curious whether a mechanical strategy (e.g. rebalancing rules, trend rules, dollar-cost averaging variants) would actually have worked once costs are included — and, just as importantly, seeing the strategies that failed and were retired.

### What it draws on

| Part of the brain | How it's used |
|---|---|
| `dossiers/*.md` | The assets a strategy trades, and their price history. |
| `costs/` | Full transaction costs (central scenario) applied to every simulated trade, per methodology section 9.5. |
| `data/evidence/evidence.csv` | The price data and cost figures a strategy relies on must themselves be evidenced, same as any other published number. |
| `lab/` | Where each strategy's pre-registration and results live — this product is the public-facing view onto that folder. |

### What has to exist before it can be built

- At least one strategy pre-registered and run through to a kept-or-killed verdict, with its pre-registration and results committed to `lab/` before any product view is built around it.
- A settled convention for how a killed strategy is displayed (it must be shown, not quietly dropped, per the kill rule).
- Skeptic review of the strategy's methodology and results, same bar as a dossier.

### Compliance constraints

- No recommendations: a strategy's historical result is never framed as "do this."
- No personalised output: results are shown as run, not adjusted per viewer.
- No signals: labelled as research on historical data on every view, never as a live or ongoing recommendation. Killed strategies stay visible, not hidden.
- Carries the paper portfolio risk line on every output, every time, per `docs/house-rules.md` mandatory risk lines.

---

## Asset Scorecard

Rates asset *types* on a fixed set of descriptive, historical factors — never a specific fund, ticker, property or item.

### What it does

Shows each asset class's value on the factors set out in `docs/scorecard-method.md` (pending Lucas's approval — see that document's own escalation before this product is built): cost drag, liquidity, historical drawdown, dispersion of historical outcomes, tax treatment and shelter eligibility, data quality, and structural/selection-bias exposure. Factors are shown side by side per asset type; whether they are ever combined into a single score is itself an open question in `docs/scorecard-method.md` section 4, not decided here. Every figure shown traces to a dossier and an evidence-log claim, the same as `Research`.

### Who it's for

A reader deciding which asset's full dossier or Autopsy comparison to look at next — a quick, honest snapshot of what an asset class actually is (costly, illiquid, volatile, well- or poorly-evidenced) before going deeper, not a signal to act on.

### What it draws on

| Part of the brain | How it's used |
|---|---|
| `docs/scorecard-method.md` | The approved factor definitions, methods and scales — the Scorecard implements exactly these, nothing more, once approved. |
| `dossiers/*.md` | Cost stack, time-to-sell, tax treatment (section 4) and item-vs-index classification (section 6) feed the factors directly. |
| `costs/` | Rolling-window calculations (in the style of `costs/benchmark/`) feed the historical-drawdown and dispersion factors where they exist for an asset. |
| `data/evidence/evidence.csv` | Only cleared (approved, non-draft) claims feed a live factor value; the tier mix of an asset's own rows is itself the data-quality factor's input. |

### What has to exist before it can be built

- Lucas's approval of `docs/scorecard-method.md`'s recommended factors, and answers to its three open escalation questions (combined vs side-by-side display, band cut-offs, how to show assets with no historical series).
- At least three or four assets with dossiers and evidence-log entries good enough to be marked cleared, so the Scorecard isn't a one-asset table.
- A UK financial promotions specialist review before launch (see the hard-constraint note above).

### Compliance constraints

- **Hard constraint (see note above):** no personalised recommendations, no forecasts, no rating of an individual security — asset *types* only, historical and descriptive factors only.
- No recommendations: a factor value is never framed as "so buy" or "avoid."
- No personalised output: the same Scorecard for every viewer.
- No signals: no "as of today" framing, no colour-coded urgency styling that implies a timing cue.
- Carries the standard risk line for its format, per `docs/house-rules.md` mandatory risk lines.

---

## Portfolio X-ray

Describes a user's own existing holdings — never rates, ranks or recommends them.

### What it does

Given a user's own portfolio (whatever assets and amounts they enter), shows its cost drag (the platform, fund and product costs they're actually paying, drawn from the relevant dossiers), concentration (the share held in each asset, sector or single item), currency exposure (the share priced in GBP versus other currencies), and historical outcome ranges (what a similarly-weighted mix has historically returned over the standard windows, per methodology section 4 — never a projection of what *this* portfolio will return going forward). Every figure is stated plainly, with no grading: a concentration figure is shown as a percentage, never labelled "high risk" or given a red/amber/green rating, since that would itself be an implicit judgment this product isn't allowed to make.

### Who it's for

A reader who wants to understand what they actually hold — its real cost, its real spread across assets and currencies, and how a similar historical mix has behaved — without being told to change anything about it.

### What it draws on

| Part of the brain | How it's used |
|---|---|
| `dossiers/*.md` | Cost stack and currency treatment for each asset the user holds. |
| `costs/` | The cost models applied to whatever the user says they hold. |
| `data/evidence/evidence.csv` | Any published figure used in the description (e.g. a historical outcome range) must itself be a cleared claim. |
| `costs/benchmark/`-style calculations | Historical outcome ranges for a given asset mix and window, reusing the same rolling-window method already built for the S&P 500. |

### What has to exist before it can be built

- A defined, safe way for a user to enter their holdings — this is the first product in this document to handle a user's personal financial data, and needs its own data-handling/privacy review before anything is built, not just a compliance-content review.
- Enough assets with dossiers, cost models and evidence-log entries cleared for use that a real portfolio (not just gold and the S&P 500) can actually be described.
- A UK financial promotions specialist review before launch (see the hard-constraint note above) — given this is the closest of the five products to describing an individual's actual financial position, this review should be treated as the highest-scrutiny of the five, not a formality.

### Compliance constraints

- **Hard constraint (see note above):** no personalised recommendations, no forecasts, no rating of an individual security — and, specific to this product, no rating, ranking or grading of the user's own holdings either (no "your concentration is too high," no red/amber/green, no "consider diversifying"). Description only.
- No recommendations: never suggests a trade, a rebalance, or a different allocation.
- No personalised output *beyond the description itself*: the tool reflects back what the user entered — it must not infer anything about the user (age, goals, risk appetite) beyond the holdings they typed in.
- No signals: no alerts, no "this has changed since you last checked" framing.
- Carries the standard risk line for its format, per `docs/house-rules.md` mandatory risk lines, plus an explicit "this is a description of your holdings, not advice" statement on every result, given how close this product sits to advice-adjacent territory.
