# S&P 500 GBP benchmark calculation

**Status:** third build, after one skeptic review. Not published — every figure below is `status: draft` in the evidence log. See `reviews/benchmark-review-2026-09-21.md` for the full review; this README reflects the fixes made in response to it (December-on-December CPI, and the dual-sided spread sensitivity below) — the FX direction and year-end selection were both independently checked and confirmed correct, no change needed there. This build also adds a second tax scenario (see "Tax scenarios" below): every result is now computed once as **Sheltered** (an ISA/SIPP holding, no UK tax) and once as **Taxable** (a basic-rate UK taxpayer holding outside a wrapper), per `docs/methodology.md` section 2.2.

This computes the S&P 500 global-shares benchmark's nominal, cost-adjusted and net real return, in GBP, for a UK investor, per `docs/methodology.md`'s "public-data benchmark chain" decision (Damodaran + Bank of England + ONS, Decisions log 19 Sep 2026). It reproduces the calculation for every available rolling window at four lengths (1, 5, 10, 20 years), per methodology section 4, for both the Sheltered and Taxable scenarios (methodology section 2.2).

---

## Files

| File | What it is |
|---|---|
| `fetch_raw_data.py` | Downloads the three raw source files into `data/raw/` (gitignored). Re-running it refreshes the data. |
| `build_benchmark.py` | Loads the raw files, computes every window in both tax scenarios, writes `results.csv` and `summary.csv`. |
| `results.csv` | Every window: start year, end year, window length, FX rates used, average inflation, then `sheltered_*` and `taxable_*` cash flows, nominal return and net real return (each with `_floor`/`_ceiling` spread variants). |
| `summary.csv` | For each window length: number of windows, then median/worst/best net real return (and the years it covers) for each of the four `sheltered`/`taxable` × `floor`/`ceiling` combinations. |
| `test_benchmark.py` | Unit tests, including three independently hand-calculated windows covering both tax scenarios. |

Run in order: `python3 fetch_raw_data.py`, then `python3 build_benchmark.py`, then `python3 test_benchmark.py` to check it.

---

## Data sources

| Source | What | Coverage | Evidence log |
|---|---|---|---|
| Aswath Damodaran (NYU Stern) | Annual S&P 500 total return, dividends included | 1928–2025 | `SP500-0044` (data), `SP500-0045` (licence) |
| Bank of England, series XUDLGBD | Daily GBP-per-USD spot exchange rate | 1975–present | `SP500-0046` (data), `SP500-0047` (licence) |
| ONS, series D7BT | UK CPI index (2015=100), December-on-December | 1988–2025 | `SP500-0048` (data), `SP500-0049` (licence) |

### Licence status

Damodaran's and ONS's data are both clearly and permissively licensed (Damodaran's own usage-rules text explicitly invites reuse; ONS is Open Government Licence). **The Bank of England's position is genuinely unresolved and is flagged here, not assumed:** the Bank's own legal page states most of its Database is OGL-licensed, but explicitly excludes "selected exchange rate data and series" that it reproduces under licence from third parties — without naming which series. Whether XUDLGBD specifically is one of the excluded ones could not be determined from the page itself. This build uses the data for internal, non-commercial research and calculation only, not external republication of the raw series. **Before anything derived from this FX data is published externally, this needs a direct question to the Bank of England (the same treatment already applied to LBMA/IBA gold pricing and S&P DJI's own index data elsewhere in this company's work) — see `docs/open-research-queue.md`.**

---

## The calculation, start to finish

For a window starting in year `Y` and running `N` years (to year `Y+N-1`):

1. **USD growth.** Compound each year's Damodaran S&P 500 total return, `Y` to `Y+N-1`, applying the central annual cost drag to each year (see "Cost assumptions" below): `usd_growth = Π (1 + return_t) × (1 - annual_cost_drag)`.
2. **Currency conversion.** Convert an illustrative £10,000 lump sum to USD at the **year-end rate for `Y-1`** (i.e. the rate just before the window starts), grow it in USD, then convert the result back to GBP at the **year-end rate for `Y+N-1`** (the window's last year). See "FX timing and direction" below for why endpoints, not a rate applied every year, give the same answer.
3. **One-off costs.** Total cash in = £10,000 + a buying commission. Net proceeds = the grown, converted amount, minus a selling commission.
4. **Tax.** In the **Sheltered** scenario, steps 1–3 are the whole story — no tax is deducted. In the **Taxable** scenario, UK Capital Gains Tax and dividend tax are applied instead — see "Tax scenarios" below for the full method.
5. **Nominal annual return** = `(net proceeds / total cash in) ^ (1/N) − 1`, per `docs/methodology.md` section 1.2.
6. **Net real return** = deflate the nominal return by the average annual CPI inflation over the same window (`(CPI_{Y+N-1} / CPI_{Y-1}) ^ (1/N) − 1`, using December-on-December CPI — see "Inflation" below), per methodology section 1.2 step 4.

Steps 1–6 are run **four times** per window — Sheltered and Taxable, each once excluding the ETF bid-ask spread cost and once including it at its labelled sensitivity upper bound — see "Cost assumptions" below.

This is done for **every start year the data supports**, per methodology's rolling-window rule (section 4, item 2) — not a hand-picked date.

---

## FX timing and direction

**Direction.** The Bank of England's own browse page labels series ECW/XUDLGBD as "Spot exchange rate, Sterling into US$" — but the actual fetched values (e.g. `0.4281` on 2 January 1975) only make sense as **GBP per 1 USD**, not the reverse: £1 was worth roughly $2.34 in January 1975, and `1/2.34 ≈ 0.427` matches the fetched value almost exactly, while a literal "Sterling into US$" reading (i.e. USD per £1) would put the value near 2.3, not 0.43. This build treats the series as **GBP per USD** on that empirical basis, not the page's own label, and converts accordingly: `GBP = USD × rate`, `USD = GBP / rate`. If this is wrong, every return in `results.csv` would be roughly inverted in its currency-return component, so this is the single most important assumption to double-check independently before anything here is relied on.

**Year-end, not daily.** The methodology asked for "annual average or year-end" rates. This build uses **year-end** (the last available trading-day observation on or before 31 December each year), for two reasons: it's simpler to reason about and check by hand than an average of ~260 daily observations, and it matches how the rest of this company's work already treats annual snapshots (e.g. the standard "month end" publication date). An annual-average approach is left as a documented alternative, not implemented here — it would give slightly different results, especially in years with a sharp FX move.

**Two endpoints, not one rate per year.** Converting once at the start and once at the end of an N-year window gives the mathematically identical cumulative result to converting at every year's own boundary and compounding the ratios (the intermediate rates cancel out: `Π (rate_{t-1}/rate_t) = rate_start/rate_end`). This build takes the simpler two-endpoint route since only the window's overall return is needed, not year-by-year GBP values within it.

---

## Cost assumptions (central scenario, from `dossiers/sp500.md`)

| Cost | Value | Claim ID | Applied as |
|---|---|---|---|
| Illustrative lump sum | £10,000 | — (illustrative, not itself an evidenced fact) | The invested amount. Chosen because it's below AJ Bell's platform-fee cap (see below), so the fee applies at its full stated rate rather than being capped — simpler to explain. A different lump sum would give the same *percentage* return, since every cost here except the flat commissions scales with, or is negligible relative to, the amount invested. |
| Buying commission | £5.00, one-off | `SP500-0006` | Added to "total cash in" at the start. |
| Selling commission | £5.00, one-off | `SP500-0006` (same schedule) | Subtracted from proceeds at the end. |
| Stamp duty / SDRT | 0% | `SP500-0002` | Not applied (genuinely zero for UK-listed ETFs). |
| Fund OCF | 0.07% p.a. | `SP500-0016` / `SP500-0017` (VUSA/CSPX) | Included in the annual cost drag. |
| Platform fee | 0.25% p.a., capped at £3.50/month | `SP500-0013` (AJ Bell) | Included in the annual cost drag. At £10,000, 0.25% = £25/year, below the £42/year cap — the cap never binds in this calculation. |
| **Total annual cost drag** | **0.32% p.a.** | sum of the two rows above | Applied to every year's USD return before FX conversion: `(1 + return) × (1 - 0.0032)`. |
| ETF bid-ask spread | **£0 (floor) / 0.05% each way (ceiling)** | `SP500-0004` (a labelled sensitivity, not a settled central figure) | The dossier's own central-scenario value for this cost is "not sourced — no central figure is invented." Per methodology section 3's unsourced-cost sensitivity rule, this build shows **both** sides explicitly, applied once on buying and once on selling: `results.csv` and `summary.csv` carry a `_floor` set of columns (spread excluded) and a `_ceiling` set (spread included at 5bps each way), for every window. A skeptic review (2026-09-21) found the first build only computed the floor version, which didn't actually satisfy the rule — fixed here. |

This uses **Route A (ETF)** from `dossiers/sp500.md`, specifically AJ Bell as the platform and VUSA/CSPX as the fund — one internally consistent combination, not a blend across platforms. Route B (open-ended fund) would give a slightly different, also-defensible answer.

**The same costs are applied to every historical year, including the 1920s–1980s.** Real trading commissions, platform fees and fund charges were almost certainly higher in earlier decades than today's rates. Applying 2026's costs uniformly across a century of history means **this calculation is more favourable to the earliest historical windows than a UK investor in, say, 1935 would actually have experienced.** This is a genuine, disclosed limitation, not a hidden one.

---

## Inflation

Average annual CPI inflation over a window is computed as `(CPI_end / CPI_start) ^ (1/N) − 1`, using ONS's **December** index value (not the annual average) for the calendar year before the window starts and the window's final calendar year — matching the year-end convention already used for FX and, implicitly, for when a year's return is deemed to have completed.

**This was originally built on the annual average instead, and a skeptic review (2026-09-21) found that a real, not negligible, problem for shorter windows** — not a minor rounding difference. Hand-recomputing the 2002 window (a 1-year window) with December CPI instead of the annual average moved the net real return from −30.59% to −30.85%, a 0.26 percentage-point swing large enough to change the published headline. The 2008 window moved by 0.44 points, driven by a genuine, dateable event: the UK's December 2008 VAT cut pulled that December's CPI reading down relative to 2008's own annual average, exaggerating the gap between the two conventions in exactly the way you'd worry about. The effect shrinks to roughly 0.05 points for a 20-year window, but since the same code computes all four window lengths, the December convention is now used uniformly rather than mixing conventions by window length.

---

## Usable date range

The Damodaran series covers 1928–2025 and the BoE series covers 1975–present, but **ONS's CPI series only goes back to 1988**, which is the binding constraint: the earliest usable window needs CPI (and FX) for the year *before* it starts, so the earliest possible start year is **1989**. The latest usable year is 2025 (the last fully complete year across all three sources). This gives:

| Window length | Usable start years | Number of windows |
|---|---|---|
| 1 year | 1989–2025 | 37 |
| 5 years | 1989–2021 | 33 |
| 10 years | 1989–2016 | 28 |
| 20 years | 1989–2006 | 18 |

A longer USD-only or GBP-only history exists further back (Damodaran to 1928, BoE to 1975), but this company's methodology requires every figure to be in real, GBP terms — so the pre-1989 years aren't usable for this specific benchmark until a longer UK CPI series is found or substituted.

---

## Tax scenarios

`docs/methodology.md` section 2.2 defines two scenarios; this build computes both, for every window.

**Sheltered** is an ISA or SIPP holding. No UK tax applies to gains or income inside either wrapper, so this is just steps 1–3 above, with nothing further deducted. Per the methodology's Decisions log (17 Sep 2026), **Taxable is the default scenario for published headlines, with Sheltered shown alongside** — this build now computes both for every window, so that decision can be honoured once anything here is published; nothing here is published yet, everything is still `status: draft`.

**Taxable** is the same holding, same platform, same fund, held outside any wrapper, for a **basic-rate UK taxpayer only** (higher- and additional-rate taxpayers, and anyone whose gains/income interact with other income in the same tax year, are out of scope — see limitations below). Two UK taxes apply, both already evidence-logged in `dossiers/sp500.md` section 4:

1. **Dividend tax on the notional distribution, every year it arises.** An accumulating ETF reinvests its dividends automatically rather than paying them out, but HMRC does not treat that as tax-free: HMRC's Capital Gains Manual, CG57707, states the notional distribution "is treated as allowable expenditure where it is subject to Income Tax in the hands of the unit holder" — i.e. it's taxed as income in the year it arises, exactly as if it had been paid out and reinvested by hand. This build approximates each year's dividend using **Damodaran's own published annual dividend yield** for the S&P 500 (from the same workbook as the total-return series, so no separate source was needed), applied to that year's opening USD position — a standard yield/price-return split, not an exact per-security decomposition. The notional dividend is converted to GBP at **that year's own year-end FX rate** (not the window's start or end rate — dividend tax is a real, dated annual event, not a one-off), then taxed at **10.75%** (`SP500-0035`, basic rate) on the amount above the **£500 annual dividend allowance** (`SP500-0034`), reapplied fresh every tax year.
2. **Capital Gains Tax at disposal, once, at the end of the window.** The whole gain (final GBP proceeds minus the original cost) is taxed at **18%** (`SP500-0032`, basic-rate band) above the **£3,000 annual CGT exempt amount** (`SP500-0003`), applied once at the single disposal event this calculation models (a lump sum bought once and sold once, not repeated annual disposals). Per CG57707, the portion of each year's notional dividend that was actually taxed as income is added to the CGT cost basis before this calculation, so the same money is never taxed twice — once as income, then again as a capital gain on disposal.

**A genuinely correct edge case, not a bug:** several windows above (e.g. the 1-year window starting 2002, and multiple 5- and 10-year worst windows) show **identical** Sheltered and Taxable results. This happens when a window's notional dividend income stays under the £500 allowance in every year *and* the window ends at a loss (so CGT floors at zero, per the exempt-amount rule) — at this build's £10,000 illustrative lump sum, dividend income alone rarely exceeds £500/year even after some compounding, so the tax drag in most windows is driven almost entirely by CGT on the accumulated capital gain at disposal, not by the annual dividend tax. This was checked by hand for the 2002 window: that year's dividend yield (≈1.40%) on the position's opening value converts to roughly £127 — under the £500 allowance — and 2002 was itself a loss year, so both taxes are genuinely zero, not omitted.

**Known limitations, not modelled:**
- Higher-rate (35.75%, `SP500-0036`) and additional-rate (39.35%, `SP500-0037`) taxpayers — basic rate only.
- Interaction with the holder's other income, gains, or allowances used elsewhere in the same tax year (this scenario assumes the full £500 dividend allowance and £3,000 CGT exempt amount are available every year, which won't be true for every real investor).
- Multiple smaller disposals, or Bed & ISA / Bed & SIPP transfers, which change the CGT timing entirely — this models one lump sum, bought once and sold once.
- Any change to these rates or thresholds between the 2026/27 figures used here and the year an investor actually held the position (the rates are today's, applied uniformly across history, same limitation already disclosed for costs above).

---

## Headline results (central cost scenario, GBP, net of UK CPI)

**Sheltered scenario (ISA/SIPP, no UK tax), floor spread** (ETF bid-ask spread excluded):

| Window | Windows | Median | Worst | Best |
|---|---|---|---|---|
| 1 year | 37 | +9.65% `SP500-0050` | −30.86% (2002) `SP500-0051` | +39.13% (1989) `SP500-0052` |
| 5 years | 33 | +10.67% `SP500-0053` | −7.19% (2000–2004) `SP500-0054` | +24.70% (1995–1999) `SP500-0055` |
| 10 years | 28 | +8.35% `SP500-0056` | −3.18% (2000–2009) `SP500-0057` | +17.08% (1991–2000) `SP500-0058` |
| 20 years | 18 | +6.25% `SP500-0059` | +4.52% (1999–2018) `SP500-0060` | +9.17% (2005–2024) `SP500-0061` |

**Taxable scenario (basic-rate UK taxpayer), floor spread:**

| Window | Windows | Median | Worst | Best |
|---|---|---|---|---|
| 1 year | 37 | +9.65% `SP500-0062` | −30.86% (2002) `SP500-0063` | +36.26% (1989) `SP500-0064` |
| 5 years | 33 | +9.33% `SP500-0065` | −7.19% (2000–2004) `SP500-0066` | +21.84% (1995–1999) `SP500-0067` |
| 10 years | 28 | +7.30% `SP500-0068` | −3.18% (2000–2009) `SP500-0069` | +15.31% (1991–2000) `SP500-0070` |
| 20 years | 18 | +5.51% `SP500-0071` | +3.88% (1999–2018) `SP500-0072` | +8.26% (2005–2024) `SP500-0073` |

**Ceiling scenario** (ETF bid-ask spread included, 0.05% each way), both tax scenarios: every figure is very slightly worse than its floor equivalent — e.g. the Sheltered 1-year worst window moves from −30.86% to −30.93%. The gap is small because the spread is a one-off cost, not an annual drag, so it matters less the longer the window. See `results.csv`/`summary.csv` for the `_ceiling` columns; not separately logged in the evidence log, since each `SP500-00xx` claim ID above already states both figures.

The 1-, 5- and 10-year worst windows all correctly land on the dot-com crash and its aftermath (2002; 2000–2004; 2000–2009) — a plausible real-world check, not just an internally-consistent one, independently confirmed by the skeptic review. Every 20-year window in the sample, even the worst, even in the ceiling scenario, and even after basic-rate UK tax, is real-return-positive.

The median and worst windows are identical between Sheltered and Taxable at several window lengths — this is a real result of this build's £10,000 illustrative lump sum, not a bug; see "Tax scenarios" below for why. The Taxable "best" windows diverge more clearly from Sheltered, since a large capital gain is exactly what triggers CGT.

---

## What this does not do yet

- The Taxable scenario only models a basic-rate taxpayer, one lump-sum purchase and one disposal, with no interaction with the holder's other income or gains — see "Tax scenarios" above for the full list of what's excluded.
- The skeptic review that checked this build could not open the binary Damodaran `.xls` file directly (no code-execution tool in that session) — it cross-checked the compounded multi-year result against an independently-fetched total-return series instead (a close match), rather than verifying each individual year's cell value bit-for-bit. Worth a follow-up if anyone wants that last mile of certainty. The new dividend-yield column (used for the Taxable scenario) has not yet had its own independent skeptic check.
- Doesn't use an annual-average FX alternative to compare against the year-end convention used (the FX convention itself was independently confirmed correct, just not compared against the alternative).
- The Bank of England licence question is unresolved (see "Licence status") and is tracked in `docs/open-research-queue.md`.
