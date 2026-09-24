# Skeptic review: S&P 500 GBP benchmark calculation (`costs/benchmark/`), third pass

**Reviewed:** `costs/benchmark/README.md`, `fetch_raw_data.py`, `build_benchmark.py`, `results.csv`, `summary.csv`, `dossiers/sp500.md` (cost-stack and tax sections), and all three raw sources — refetched independently in this pass, not read from the repo's gitignored `data/raw/` copies.

**Verdict: Fix.**

The two fixes this build claims to have made since the 2026-09-21 review (December-on-December CPI; the dual-sided spread sensitivity) are both real and correctly implemented — not just claimed in prose. The full pipeline is exactly reproducible from scratch: independently re-fetching all three raw sources and re-running `build_benchmark.py` unmodified reproduced `results.csv` and `summary.csv` **byte-for-byte**, and hand-recomputing the three requested windows from a freshly written formula (not copied from the script) matched the committed figures to 16 significant figures. But this pass found one new, quantified, headline-affecting bug the prior review didn't check for: the AJ Bell platform-fee cap is real in the dossier and in the code's own comments, but is never actually applied, and it silently understates every published **best-case** 5/10/20-year headline once a position compounds past ~£16,800.

---

## Findings

### 1. [MAJOR — new, not caught by the 2026-09-21 review] The AJ Bell platform-fee cap is documented as non-binding but is never actually implemented, and it does bind for every long, well-performing window

`build_benchmark.py` sets `ANNUAL_PLATFORM_FEE_RATE = 0.0025` with the comment *"cap not reached at this lump sum"* — true, but only checked against the **starting** £10,000 position. AJ Bell's own cap, per `dossiers/sp500.md` (SP500-0013), is **£3.50/month = £42/year**, which a flat 0.25% fee exceeds once the position passes **£16,800**. The code has no cap logic anywhere — it applies `(1 - ANNUAL_COST_DRAG)` (0.32% flat) every year regardless of position size, for every window length and every tax/spread combination.

For a lump sum that starts at £10,000 and is only ever tested over 1-year windows this genuinely doesn't matter. But three of the four published **window lengths that have time to compound** cross the cap threshold, and I modelled the actual year-by-year GBP-converted position (using the platform's own real FX rate each year, not the window's two endpoints) to quantify it precisely, sheltered/floor:

| Published window | Published headline (uncapped) | Correctly capped | Delta | Rounded headline changes? |
|---|---|---|---|---|
| 20yr best, 2005–2024 | +9.17% (→ **+9.2%**) | +9.2683% | +0.097pp | Yes — **+9.2% → +9.3%** |
| 10yr best, 1991–2000 | +17.08% (→ **+17.1%**) | +17.1915% | +0.113pp | Yes — **+17.1% → +17.2%** |
| 5yr best, 1995–1999 | +24.70% (→ **+24.7%**) | +24.7692% | +0.067pp | Yes — **+24.7% → +24.8%** |
| 1yr best, 1989 | +39.13% (→ **+39.1%**) | +39.1314% | +0.0002pp | No |

Worked example, 20yr window (2005–2024): the GBP-equivalent position first crosses £16,800 in **2013** (£21,182); by the final year, **2024**, it reaches **£106,653**, where the model charges an uncapped fee of **£266.63** against a true capped fee of **£42** — a 6.3× overcharge in that single year alone, and the cap binds for 12 of the 20 years (2013–2024).

The direction is consistent and one-sided: because the model always overcharges (never undercharges) once the cap should bind, **every published "best" figure for 5/10/20-year windows is currently too pessimistic**, in all four scenario combinations (sheltered/taxable × floor/ceiling) — I only computed sheltered/floor above, but the same flat, uncapped `ANNUAL_COST_DRAG` multiplier is used identically in `_taxable_scenario`, so the taxable-scenario best-case rows will show the same directional bias. Worst-case and short windows are essentially unaffected (the 2002 1-year worst-case delta I checked was +0.0001pp — the position never grows large enough for the cap to matter when it's falling, not compounding).

**Recommended fix:** replace the flat `ANNUAL_PLATFORM_FEE_RATE` multiplier with a genuine per-year GBP-position check (`min(0.25% × GBP-converted running value, £42)`), which requires tracking an annual FX-converted position rather than only the window's two endpoints — a real architectural change to `compute_window`/`_sheltered_scenario`/`_taxable_scenario`, not a one-line constant tweak. Re-run and re-round every headline afterward; do not assume only the four rows I checked move, since the corrected mechanism needs to run at every window length, both tax scenarios and both spread scenarios to be sure.

### 2. [PASS — confirmed fixed, and independently re-verified from raw data, not just read in code] CPI now uses December-on-December, matching the FX/returns year-end convention

`load_ons_december_cpi` matches only rows of the exact form `"YYYY DEC"` (regex `^(\d{4}) DEC$`), which is a genuine switch away from the annual-average series the 2026-09-21 review flagged. I didn't just read the function — I refetched `ons_cpi_d7bt.csv` live from `ons.gov.uk` myself and parsed it independently, getting Dec-2001 = 74.0, Dec-2002 = 75.2, Dec-2007 = 83.0, Dec-2008 = 85.5, matching both `build_benchmark.py`'s own loader and the prior review's manually-read values exactly.

### 3. [PASS — independently re-verified with a different method than the 2026-09-21 review] FX is year-end and GBP-per-USD

The 2026-09-21 review checked this against Black Wednesday (1992) and the 2008 crisis. I checked it against four different, unrelated years, computed from my own live refetch of the BoE HTML page (not the repo's cached copy): 2015 → implied cable $1.48/£, 2016 (post-Brexit) → $1.23/£, 2019 → $1.32/£, 2020 → $1.36/£. All four match well-documented real-world GBP/USD history, including the correct **direction** of the post-Brexit-referendum move (XUDLGBD jumps from 0.6748 to 0.8128 across 2015→2016 — more pounds per dollar, i.e. sterling weakening, which is exactly what happened). `load_boe_year_end_rates` genuinely selects the chronologically latest trading day per calendar year (max `(month, day)`), not a fixed 31 December lookup — confirmed by reading the function, consistent with the prior review's 1999-Millennium-holiday check.

### 4. [PASS — independently re-verified with fresh code and fresh data, closing the prior review's one open gap] 2002, 2008 and 2000–2009 hand-recomputed and matched exactly

The 2026-09-21 review could not open the binary Damodaran `.xls` file at all (no code-execution tool that session) and had to back-solve an implied return and sanity-check it against Wikipedia — a reasonable substitute, but not a direct check. This session has Python and network access, so I did the direct check: refetched all three raw sources live, wrote a fresh sheltered/floor formula from scratch (not copied from `build_benchmark.py` or `test_benchmark.py`), and got:

| Window | My hand calculation | `results.csv` (sheltered_net_real_return_floor) | Match |
|---|---|---|---|
| 2002 (1yr) | −0.3086081786442316 | −0.3086081786442316 | Exact, 16 sig figs |
| 2008 (1yr) | −0.1506887303740544 | −0.1506887303740544 | Exact, 16 sig figs |
| 2000–2009 (10yr) | −0.03177602354381004 | −0.03177602354381004 | Exact, 16 sig figs |

I also went further than asked: I refetched all three raw files fresh, dropped them into an unmodified copy of `build_benchmark.py`, and reran the whole pipeline end to end. The output `results.csv` (116 data rows) and `summary.csv` (4 rows) are **byte-for-byte identical** to what's committed in the repo, and the console summary matches every number in the README's own "Headline results" table exactly. This is about as strong a confirmation as this kind of check can get: the pipeline is genuinely reproducible from its stated raw sources, with nothing hand-edited afterward.

### 5. [PASS] Cost scenario matches `dossiers/sp500.md`'s central column, and each cost is applied in the structurally correct place

Checked every constant in `build_benchmark.py` against its cited claim ID in `dossiers/sp500.md`:

| Constant | Code value | Dossier source | Match |
|---|---|---|---|
| Buy/sell commission | £5.00 | SP500-0006, AJ Bell "£5.00" (central) | ✓ |
| Platform fee rate | 0.25% p.a. | SP500-0013, AJ Bell "0.25% (max £3.50/month)" | ✓ (rate matches; cap doesn't — see Finding 1) |
| Fund OCF | 0.07% p.a. | SP500-0016/0017, VUSA/CSPX | ✓ |
| CGT rate | 18% | SP500-0032, basic-rate band | ✓ |
| CGT exempt amount | £3,000 | SP500-0003 | ✓ |
| Dividend allowance | £500 | SP500-0034 | ✓ |
| Dividend tax rate | 10.75% | SP500-0035, basic rate | ✓ |

All seven pull the **central**-column figure specifically (not InvestEngine's "low" or Hargreaves Lansdown's "high"), consistent with the README's stated "Route A (ETF), AJ Bell" choice. Placement is also correct: buy/sell commissions are one-off, added to cash-in / subtracted from proceeds exactly once; OCF and platform fee compound annually inside `usd_growth`; CGT applies once, only in the taxable scenario, at disposal; dividend tax applies annually, only in the taxable scenario, on Damodaran's own published yield; the sheltered scenario correctly has zero tax logic at all (ISA/SIPP). The one real defect in this area is Finding 1 (the fee rate is right, its cap isn't implemented).

### 6. [PASS, with one interpretive note worth a documentation line] No published window falls below the 90% coverage rule

`compute_window` returns `None` — excluding the window from `results.csv` entirely — unless Damodaran has every year in the window, BoE FX has the start-year-minus-one rate and every year in the window, and ONS CPI has both the start-year-minus-one and end-year December values. There is no partial-fill path anywhere in `build_results`. This means every one of the 116 published windows has **100%**, not merely ≥90%, of its required annual data points — I don't need to hunt for a specific near-miss case, since the code structurally cannot publish one.

One documentation gap, not a numeric defect: `docs/methodology.md`'s 90% rule is written for monthly series ("gaps longer than three months... not filled in"), which doesn't map cleanly onto this benchmark's once-a-year data. Worth a one-line clarification in the README that this build's actual rule is "any missing annual data point excludes the whole window," which is stricter than, and therefore compliant with, the general 90% floor — but is a different mechanism than the methodology text describes, and a future reader shouldn't have to infer that.

### 7. [Minor, latent — not currently causing wrong output] `_taxable_scenario` silently defaults a missing dividend yield to 0% instead of excluding the window

`yields.get(y, 0.0)` means that if Damodaran's "S&P 500 & Raw Data" sheet were ever missing a year that the "Returns by year" sheet has, the taxable scenario would quietly assume 0% dividend yield (understating dividend tax) rather than excluding the window the way every other missing-data case in this file does. I checked: there is currently no such gap anywhere in the usable 1989–2025 range (confirmed directly against my own live refetch of both sheets), so this has not produced any wrong number today. But it's the only place in the file that fails silently rather than loudly, which is inconsistent with the all-or-nothing pattern everywhere else. Recommend changing it to exclude the window (matching `compute_window`'s existing pattern) rather than defaulting, so a future data change can't introduce a silent understatement.

---

## What I couldn't check

- **Median values for all 116 windows by hand.** Like the prior review, I spot-checked the worst/best rows for each window length (all of which I independently reproduced via the full pipeline re-run in Finding 4) rather than hand-recomputing all 37+33+28+18 medians myself. Given the full byte-for-byte pipeline reproduction in Finding 4, I have high confidence in this, but it is a relied-on inference, not a direct hand check.
- **Whether the same platform-fee-cap bug (Finding 1) moves any taxable-scenario or ceiling-spread headline by enough to change its rounded value.** I only ran the corrected model for sheltered/floor. The mechanism is identical in `_taxable_scenario`, so I expect the same direction and similar magnitude, but I did not rerun all four scenario combinations for all affected windows — that should happen as part of the actual fix, not be guessed at here.
- **The Bank of England licence question.** Out of scope for this review, and already correctly tracked elsewhere (`docs/open-research-queue.md`, `SP500-0074`).
