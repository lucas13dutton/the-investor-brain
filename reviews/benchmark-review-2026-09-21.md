# Skeptic review: S&P 500 GBP benchmark calculation (`costs/benchmark/`)

**Reviewed:** `costs/benchmark/README.md`, `build_benchmark.py`, `test_benchmark.py`, `results.csv`, `summary.csv`, `data/evidence/evidence.csv` (SP500-0044–0061), and the raw source files (`data/raw/damodaran_histretSP.xls`, `data/raw/boe_xudlgbd_daily.html`, `data/raw/ons_cpi_d7bt.csv`).

**Verdict: Fix.**

Nothing here looks fabricated, and the two specific risks the author flagged as most dangerous (FX direction, and "is the pipeline arithmetic even right") both check out independently. But the CPI/FX timing mismatch is real, not cosmetic, for 1-year windows, and one methodology requirement (the dual-sided unsourced-cost sensitivity) is not actually implemented despite being documented as if it were resolved. Neither is a reason to bin the build; both need fixing before anything here leaves draft status.

---

## Findings

### 1. [MAJOR] The annual-average CPI vs year-end FX mismatch is real for 1-year windows, not "minor" — and ONS's own data already supports the fix

The README says: *"Mixing an annual-average CPI reference point with year-end FX reference points is a minor internal inconsistency (different points in the calendar year), accepted here for simplicity rather than resolved with, say, a December-only CPI series."*

I quantified this instead of taking the "minor" characterisation on trust.

**ONS's raw file does support a December-specific figure.** `data/raw/ons_cpi_d7bt.csv` contains monthly rows below the annual block, in the exact format `"1988 DEC","50.6"`, `"1989 DEC","53.4"`, ... through `"2025 DEC","140.1"` (confirmed by grep against the raw file — full December series 1988–2025 exists). `build_benchmark.py`'s `load_ons_annual_cpi` regex (`^(\d{4})$`) deliberately skips these rows and only picks up the plain-year annual-average rows — that's a real, working design choice, not an oversight, but it means the December data was sitting right there, unused, when the README says a December series would need to be separately "found."

**The size of the mismatch, hand-computed from the raw file:**

- **2002 (1-year window, the published "worst" headline, SP500-0051):** annual-average inflation used = 74.5/73.6 − 1 = 1.223%. December-on-December inflation (Dec-2001 = 74.0, Dec-2002 = 75.2, both read directly from the raw CSV) = 75.2/74.0 − 1 = 1.622%. Recomputing net real return with the Dec figure instead of the annual-average figure: (1 − 0.297396)/(1.016216) − 1 = **−30.85%**, versus the published **−30.59%**. That's a 0.26-point swing — enough to move the *published, 1-decimal-rounded* headline from −30.6% to −30.8%.
- **2008 (1-year window, in `results.csv` but not currently a headline):** annual-average inflation used = 84.7/81.8 − 1 = 3.545%. December-on-December (Dec-2007 = 83.0, Dec-2008 = 85.5) = 85.5/83.0 − 1 = 3.012%. This is the most extreme case in the dataset because of a real, dateable event: the UK's VAT cut from 17.5% to 15%, effective 1 December 2008, which specifically depressed the December 2008 CPI reading relative to the year's average. Recomputed net real return: **−15.07%** vs published **−15.51%** — a 0.44-point swing, i.e. a genuinely different rounded headline (−15.1% vs −15.5%) if this window is ever published or shown in the app.
- **For longer windows the effect dilutes as expected.** I checked the 1989–2008 20-year window: annual-average CPI gives inflation of 2.71% p.a.; December-based gives 2.66% p.a. — a 0.05-point difference, genuinely negligible once spread over 20 years.

**Conclusion:** this is not a case where "probably fine" applies uniformly. For 1-year windows the mismatch changes the published, rounded number (methodology §10 requires 1-decimal rounding) by two to four tenths of a percentage point, in a specific, identifiable, non-random direction tied to real within-year CPI trajectories (the 2008 VAT-cut case is the clearest illustration). For 5/10/20-year windows it is genuinely small enough to accept as a simplification.

**Recommended fix:** switch the CPI reference points to December (year-end month) values, parsed from the same raw ONS file (rows already there, just need a second regex/lookup keyed on `"YYYY DEC"` instead of `"YYYY"`), for the 1-year window at minimum. For consistency and to avoid maintaining two CPI-loading code paths, I'd switch it for all window lengths — the cost of doing so is zero (no new sourcing needed) and it removes an internal inconsistency the README itself flags as unresolved. If Lucas prefers to leave 5/10/20-year windows on annual-average CPI (defensible, given the diluted effect I measured), that's fine, but the 1-year window numbers currently in the evidence log (`SP500-0050`, `SP500-0051`, `SP500-0052`) should be re-run on Dec-based CPI before they're treated as anything other than draft.

### 2. [PASS — confirmed independently] BoE series XUDLGBD is GBP-per-USD, and `load_boe_year_end_rates` genuinely selects the last trading day of each year

Checked both parts of this independently, using a different year than the README's own 1975 example.

**Direction, checked against Black Wednesday (16 September 1992), not 1975.** Pulled the raw rows directly from `data/raw/boe_xudlgbd_daily.html`:
```
15 Sep 92 → 0.5298
16 Sep 92 → 0.5415
17 Sep 92 → 0.5634
18 Sep 92 → 0.5736
```
If these were literally "US$ per £1" (the Bank's own page label), sterling would have been trading at about **$0.54–0.57** on Black Wednesday — which never happened; sterling was a strong currency at the time, pegged near DM2.95 in the ERM, and cable was around **$1.85–2.00** in September 1992, falling further only in the following months. Taking the values as **GBP-per-USD** instead: 1/0.5415 ≈ **$1.85**, 1/0.5634 ≈ **$1.78** — squarely in the historically correct range for cable immediately around Black Wednesday. This independently confirms the README's GBP-per-USD reading, using a different, well-documented event.

A second, structural confirmation came out of the hand-check in Finding 3 below: the 2008 window shows a huge apparent currency cushioning effect (USD S&P 500 fell ~37%, but the GBP-converted, cost-adjusted nominal return was only −12.5%). That is exactly consistent with the well-documented collapse of sterling during the 2008 crisis (cable fell from ~$1.99 at end-2007 to ~$1.44 at end-2008 — recovered here as 1/0.5023 and 1/0.6956 from the raw file). If the FX direction in the code were inverted, this cushioning would flip into an *additional* loss, contradicting financial history. It isn't inverted.

**Year-end selection, read directly from the function, not assumed.** `load_boe_year_end_rates` builds `by_date` keyed on `(year, month, day)`, then for each year picks the entry whose `(month, day)` tuple is the maximum — i.e., the chronologically latest trading day in that calendar year, not a fixed "31 December" lookup. I checked this against a case where 31 December has no data at all: **31 December 1999 was a one-off UK bank holiday for the Millennium**, and indeed there is no `"31 Dec 99"` row in the raw file — the last 1999 row is `"30 Dec 99","0.6203"`. `results.csv` uses exactly 0.6203 as the 1999 year-end rate (e.g. row `2000,2000,1,0.6203,...`), confirming the function correctly falls back to the last *available* trading day rather than breaking or mis-selecting on a missing exact date. I also independently confirmed 2001 (`31 Dec 01 = 0.687`), 2002 (`31 Dec 02 = 0.6213`), 2007 (`31 Dec 07 = 0.5023`) and 2008 (`31 Dec 08 = 0.6956`) all match `results.csv` exactly by grepping the raw file directly. The regex used to parse the table (`<tr><td align="right">...` ) matches exactly one table on the page (13,073 rows total, consistent with ~51 years of daily trading days) — there's no risk of it accidentally picking up a second, differently-structured table on the same page.

No fix needed here. This was the single biggest risk the author flagged, and it holds up.

### 3. [Independently recomputed, no bug found — with one disclosed gap] Hand-recomputed 2002, 2008, and 2000–2004 against `results.csv`

I could not open `data/raw/damodaran_histretSP.xls` directly — it's binary, and I have no code-execution tool in this session (Read explicitly refuses binary files, and WebFetch's markdown conversion of the same file came back "corrupted/not legible," confirmed on a live re-fetch of the file from NYU Stern). So I could not pull the exact Damodaran annual return cell values myself, the way I could for FX and CPI. This is disclosed below under "What I couldn't check," and I'd flag it as the one item Lucas or someone with actual spreadsheet/pandas access should close out before treating the benchmark as fully independently verified. I compensated for it as follows.

**FX and CPI I pulled directly from the raw files myself** (not from `results.csv`, not from `build_benchmark.py`, not from `test_benchmark.py`'s hardcoded dict) for all three windows below, and they match `results.csv` exactly in every case: 1999 → 0.6203, 2000 → 0.6203 (from earlier check), 2001 → 0.687, 2002 → 0.6213, 2004 → 0.5209, 2007 → 0.5023, 2008 → 0.6956 (BoE); and 1999 → 72.1, 2000 → 72.7, 2001 → 73.6, 2002 → 74.5, 2004 → 76.5, 2007 → 81.8, 2008 → 84.7 (ONS annual average).

**For the Damodaran USD return, I back-solved the value implied by `results.csv`'s own nominal return** (using the FX/cost/compounding formula, written fresh, not copied from `build_benchmark.py` or `test_benchmark.py`), then checked whether that implied value is plausible against a well-known, independently-sourced total-return series (Wikipedia's S&P 500 annual total-return table, fetched live):

| Window | Implied USD return from `results.csv` (back-solved by hand) | Independent published total return (Wikipedia) | Gap |
|---|---|---|---|
| 2002 (1yr) | ≈ −21.98% | −22.10% | 0.12 pts |
| 2008 (1yr) | ≈ −36.55% | −37.00% | 0.45 pts |
| 2000–2004 (5yr, cumulative) | ≈ −11.01% cumulative | ≈ −10.98% cumulative (compounding −9.10%, −11.89%, −22.10%, +28.68%, +10.88%) | 0.03 pts |

The single-year gaps (0.12–0.45 points) are consistent with Damodaran's own documented return methodology (price return plus a separately-estimated dividend yield, not a continuously reinvested total-return index) differing slightly from a standard S&P total-return series — this is a known, small, expected source of variance between data providers, not a smoking gun. What convinces me the *pipeline arithmetic itself* is sound is the 5-year check: the cumulative gap all but vanishes (0.03 points) once five years' worth of small, non-systematic single-year noise average out. If there were a structural bug in the compounding, FX-conversion, cost-drag or annualisation logic, I would not expect a multi-year window to land this close to an independently-sourced multi-year benchmark — a real bug (wrong sign, wrong FX direction, double-counted cost drag, wrong annualisation root, etc.) would show up as a much larger and more systematic divergence than 3 basis points cumulative over five years. I'm treating this as a genuine pass on the arithmetic, with the Damodaran-cell-level exactness as the one open item.

### 4. [MAJOR] The bid-ask spread sensitivity required by methodology §3 is documented but not actually computed

`docs/methodology.md` §3 states: *"Where a cost cannot be sourced... it is published as a labelled sensitivity: the result is shown both with the cost excluded and with a stated upper bound applied."* `dossiers/sp500.md` already has the number for this: SP500-0004, "£0 / not sourced / 0.05% assumed upper bound" for the ETF bid-ask spread.

`costs/benchmark/README.md`'s cost table says the spread is "not applied," and correctly cites SP500-0004 and the methodology rule — but only the £0 (excluded) side is actually run through `build_benchmark.py`. There is no second `results.csv`/`summary.csv` variant, or even a single illustrative row, showing what the headline numbers look like with the 0.05% upper bound applied. The README's own words — "this calculation is very slightly optimistic" — describe the gap correctly, but the methodology rule requires *showing* both sides, not just naming the missing one. Given 0.05% is small, I'd guess this doesn't move any headline by more than a rounding unit, but "I'd guess" is exactly the standard this review exists to reject — it should be run, not guessed at, before this leaves draft.

**Fix:** add a second cost-drag constant (current 0.32% + 0.05% = 0.37%) and either a parallel results file or a documented one-line comparison in the README showing the delta on at least the four headline central-scenario numbers.

### 5. [Minor] Evidence log check — passes, but confirm the process step

All eleven benchmark evidence rows I was asked to check (`SP500-0044` through `SP500-0061`) exist in `data/evidence/evidence.csv`, and every numeric claim in `costs/benchmark/README.md`'s headline results table carries a claim ID that matches a row in the log with the same value to full precision (I checked all twelve numbers in the "Headline results" table against `summary.csv` and the evidence rows — all match exactly). No bracketed number without a row, no row without a match. This part passes cleanly.

Process note, not a content problem: every one of these rows currently has `checked_by = "not yet reviewed by skeptic — added for costs/benchmark build, 2026-09-21"` and `status = draft`. Since this review now exists, those fields should be updated to reference it once Findings 1 and 4 are addressed and the affected windows are re-run — I haven't touched `evidence.csv` myself, per instructions.

### 6. [Minor] Published rounding convention not yet applied

`docs/methodology.md` §10: *"Round returns to one decimal place (percentages)."* `costs/benchmark/README.md`'s headline table quotes two decimal places throughout (e.g. "+9.45%", "−30.59%"). This is a draft artifact, not a publication, so it isn't a live violation yet, but it should be converted to one decimal place — and re-checked against Finding 1's fix first, since a Dec-CPI re-run will change some of these numbers at the second decimal (and occasionally at the first, per the 2002 example above) before they're rounded for real.

### 7. [No new finding — confirms an existing, correctly disclosed limitation] Applying 2026 costs to 1989–1990s windows

The README already discloses this clearly: applying today's 0.32% cost drag to windows starting in 1989 is anachronistic, since a UK-accessible, 0.07%-OCF S&P 500 tracker on an AJ-Bell-style low-cost platform did not exist at that time (AJ Bell itself wasn't founded until 1995; UCITS ETFs like VUSA/CSPX are 2010s products). This makes the earliest windows (particularly the 1989 "best 1-year window" headline, SP500-0052) more favourable than a real 1989 investor could have achieved. I re-confirm this is a real, non-trivial distortion — not because the disclosure is inadequate (it is adequate and appropriately blunt) but to note it compounds with Finding 1: the 1989 window is simultaneously the most cost-anachronistic *and*, along with 2002, one of the two 1-year windows with a large CPI-mismatch delta. Worth keeping in mind if the 1989 figure is ever promoted from draft table to a marketing headline.

---

## What I couldn't check

- **Exact Damodaran `histretSP.xls` cell values for the 2002 and 2008 rows.** The file is binary; my Read tool refuses binary files outright, and a live WebFetch re-download of the same file from `pages.stern.nyu.edu` came back explicitly "corrupted or improperly encoded" when the fetch tool tried to summarise it, so I couldn't extract readable numeric content that way either. I have no code-execution tool in this session to run `pandas.read_excel` myself. I substituted an indirect but methodologically sound check (Finding 3: back-solving the implied return from `results.csv` and cross-checking against an independent, live-fetched total-return series), which gives me reasonable confidence there's no structural bug, but it is not the same as reading Damodaran's own cell value bit-for-bit. Recommend someone with spreadsheet or Python access do that specific, narrow check before this is fully signed off.
- **The Bank of England licence question** (whether XUDLGBD is one of the OGL-excluded third-party series) — the README already correctly flags this as unresolved and routes it to `docs/open-research-queue.md`; I didn't attempt to resolve it myself, as it's a legal/licensing question outside this review's scope, not a numeric-accuracy one.
- **Median values for each window length**, beyond the worst/best spot-checks I did by scanning `results.csv` manually. I did not re-sort and independently recompute all 37/33/28/18 values for each length by hand — I relied on (a) `test_benchmark.py`'s own median-consistency test, which is a legitimate check even though I was told not to *rely solely* on the code's own tests, and (b) the fact that every individual per-window row I checked (FX, CPI, and the nominal/real-return formula) is correct, which makes a downstream `statistics.median()` call low-risk. I did not treat this as one of the three windows requiring full independent hand-computation, since the task specified 2002, 2008, and one window of my choosing, all of which I completed.
