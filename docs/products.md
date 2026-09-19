# Products

**Status: draft specs. None of the three is built.** This document describes what each is intended to do, so that what gets built matches what the brain already promises in `docs/methodology.md` and `docs/house-rules.md`. Nothing here is a commitment to a build date.

These are three surfaces of the Asset Theory brand — see the "Naming" section in the root `README.md` for the full naming hierarchy.

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
