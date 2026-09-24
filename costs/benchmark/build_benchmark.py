#!/usr/bin/env python3
"""Build the S&P 500 GBP benchmark: nominal, cost-adjusted and net real returns
for every available start year, at window lengths of 1, 5, 10 and 20 years.

Data sources (raw files in data/raw/, gitignored, downloaded by
fetch_raw_data.py — see README.md for URLs, access dates and licence notes):
  - Damodaran's annual S&P 500 total return AND dividend yield series
    (NYU Stern), 1928-2025.
  - Bank of England XUDLGBD daily GBP-per-USD spot rate, 1975-present.
  - ONS CPI (D7BT, all items index, 2015=100), December-on-December, 1988-2025.

Every window is computed for two tax scenarios (Sheltered and Taxable, per
methodology section 2.2) crossed with two cost-sensitivity scenarios (floor:
ETF bid-ask spread excluded; ceiling: spread included at its labelled 0.05%
upper bound, per methodology section 3) — four figures per window. See
README.md for the full method, every assumption, and why the Sheltered
scenario is the default (no ISA/SIPP-specific costs exist to model; a
Taxable holding pays CGT on disposal and dividend tax on reinvested income,
per dossiers/sp500.md section 4).

Usage: python3 costs/benchmark/build_benchmark.py
Outputs: costs/benchmark/results.csv, costs/benchmark/summary.csv
"""

import csv
import re
import sys
from pathlib import Path
from statistics import median

BENCHMARK_DIR = Path(__file__).resolve().parent
DATA_RAW = BENCHMARK_DIR.parent.parent / "data" / "raw"

DAMODARAN_XLS = DATA_RAW / "damodaran_histretSP.xls"
BOE_HTML = DATA_RAW / "boe_xudlgbd_daily.html"
ONS_CSV = DATA_RAW / "ons_cpi_d7bt.csv"

WINDOW_LENGTHS = [1, 5, 10, 20]

# Central cost scenario, from dossiers/sp500.md, Route A (ETF) — see README.md
# "Cost assumptions" for the exact claim IDs and figures behind each number.
ILLUSTRATIVE_LUMP_SUM_GBP = 10_000.0
BUY_COMMISSION_GBP = 5.00        # SP500-0006, AJ Bell, central
SELL_COMMISSION_GBP = 5.00       # SP500-0006, AJ Bell, central (same schedule)
ANNUAL_OCF_RATE = 0.0007         # SP500-0016/0017, VUSA/CSPX, central, 0.07% p.a.
ANNUAL_PLATFORM_FEE_RATE = 0.0025  # SP500-0013, AJ Bell, central, 0.25% p.a. of the
                                    # position's GBP value each year, capped below.
PLATFORM_FEE_CAP_GBP = 42.00       # SP500-0013, AJ Bell, "£3.50 per month" x 12.
                                    # Binds once the GBP position passes ~£16,800 —
                                    # a skeptic review (2026-09-24) found this is
                                    # reached by every long, well-performing window
                                    # (e.g. the 2005-2024 20yr window passes it by
                                    # 2013), so it is applied per year below, not
                                    # assumed away as it was in the previous build.

# SP500-0004: the ETF bid-ask spread, a labelled sensitivity with no real source.
# "Floor" = excluded (£0). "Ceiling" = the dossier's own stated 0.05% (5bps) upper
# bound, applied once on the way in and once on the way out, as a % of the
# traded value at that point — not an invented central figure either way.
SPREAD_CEILING_RATE = 0.0005

# Taxable scenario, basic-rate taxpayer, 2026/27 rates — dossiers/sp500.md section 4.
CGT_RATE = 0.18                    # SP500-0032, basic-rate band
CGT_ANNUAL_EXEMPT_GBP = 3_000.0    # SP500-0003, applied once at disposal
DIVIDEND_ALLOWANCE_GBP = 500.0     # SP500-0034, applied fresh each tax year
DIVIDEND_TAX_RATE = 0.1075         # SP500-0035, basic rate


def load_damodaran_returns_and_yields(xls_path):
    """Return two dicts, {year: total return} and {year: dividend yield}, both
    decimal, from the Damodaran workbook's own two sheets."""
    import pandas as pd

    returns_df = pd.read_excel(xls_path, sheet_name="Returns by year", header=19)
    returns_df = returns_df[["Year", "S&P 500 (includes dividends)"]].dropna()
    returns = {}
    for _, row in returns_df.iterrows():
        year_raw = row["Year"]
        if not isinstance(year_raw, (int, float)):
            continue  # skip summary rows like "1928-2025"
        returns[int(year_raw)] = float(row["S&P 500 (includes dividends)"])

    yields_df = pd.read_excel(xls_path, sheet_name="S&P 500 & Raw Data", header=1)
    yields_df = yields_df[["Year", "Dividend Yield"]].dropna()
    yields = {}
    for _, row in yields_df.iterrows():
        year_raw = row["Year"]
        if not isinstance(year_raw, (int, float)):
            continue
        yields[int(year_raw)] = float(row["Dividend Yield"])

    return returns, yields


def load_boe_year_end_rates(html_path):
    """Return {year: GBP-per-USD rate at that year's last available trading day} from the
    raw BoE database HTML page (a <tbody> of <tr><td>date</td><td>rate</td></tr> rows)."""
    html = html_path.read_text(encoding="utf-8", errors="replace")
    rows = re.findall(
        r'<tr><td align="right">([^<]+)</td><td align="right">([^<]+)</td></tr>', html
    )
    month_map = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
    }
    by_date = {}
    for date_str, rate_str in rows:
        # format: "02 Jan 75"
        day_s, mon_s, yr_s = date_str.strip().split()
        year_2digit = int(yr_s)
        year = 2000 + year_2digit if year_2digit < 50 else 1900 + year_2digit
        month = month_map[mon_s]
        day = int(day_s)
        by_date[(year, month, day)] = float(rate_str)

    # last available observation per calendar year
    year_end_rate = {}
    for (year, month, day), rate in by_date.items():
        key = (month, day)
        if year not in year_end_rate or key > year_end_rate[year][0]:
            year_end_rate[year] = (key, rate)
    return {year: rate for year, (key, rate) in year_end_rate.items()}


def load_ons_december_cpi(csv_path):
    """Return {year: December CPI index value} from the raw ONS CSV export.

    Uses December-on-December, not the annual average, to match the year-end
    convention already used for returns and FX — see README.md "Inflation"
    for why a skeptic review (2026-09-21) found the earlier annual-average
    choice a real, dateable problem (e.g. the Dec 2008 UK VAT cut distorts
    that December's reading relative to 2008's own annual average), not a
    negligible one, at least for short windows.
    """
    cpi = {}
    dec_row_re = re.compile(r"^(\d{4}) DEC$")
    with csv_path.open(newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) != 2:
                continue
            period_field, value_field = row
            m = dec_row_re.match(period_field)
            if m:
                cpi[int(m.group(1))] = float(value_field)
    return cpi


def _grow_one_year(value_usd, year, damodaran, fx):
    """Apply one year's total return, fund OCF (a pure %, never capped) and AJ Bell's
    platform fee (0.25% of the GBP-converted position, capped at £42/year — SP500-0013)
    to a USD-tracked position. Returns the new value_usd.

    The platform fee has to be evaluated in GBP, on that year's own FX rate, because the
    cap is a fixed currency amount, not a percentage — a skeptic review (2026-09-24)
    found the previous build applied 0.25% uncapped throughout, which is only true for
    the *starting* position: every window with enough time to compound past roughly
    £16,800 (in practice, every published 5/10/20yr best-case window) should have hit
    the cap and didn't. See reviews/benchmark-review-2026-09-24.md Finding 1.
    """
    value_usd = value_usd * (1 + damodaran[year]) * (1 - ANNUAL_OCF_RATE)
    gbp_value = value_usd * fx[year]
    platform_fee_gbp = min(ANNUAL_PLATFORM_FEE_RATE * gbp_value, PLATFORM_FEE_CAP_GBP)
    gbp_value -= platform_fee_gbp
    return gbp_value / fx[year]


def _sheltered_scenario(start_year, end_year, damodaran, fx, spread_rate):
    """No tax deducted — an ISA/SIPP holding. Returns (total_cash_in, net_proceeds)."""
    rate_start = fx[start_year - 1]
    value_usd = ILLUSTRATIVE_LUMP_SUM_GBP / rate_start
    for y in range(start_year, end_year + 1):
        value_usd = _grow_one_year(value_usd, y, damodaran, fx)
    grown_gbp = value_usd * fx[end_year]

    total_cash_in = ILLUSTRATIVE_LUMP_SUM_GBP * (1 + spread_rate) + BUY_COMMISSION_GBP
    net_proceeds = grown_gbp * (1 - spread_rate) - SELL_COMMISSION_GBP
    return total_cash_in, net_proceeds


def _taxable_scenario(start_year, end_year, damodaran, yields, fx, spread_rate):
    """A basic-rate taxpayer holding outside a wrapper, per dossiers/sp500.md
    section 4.1. CGT on disposal, dividend tax on the notional distribution
    each year (an accumulating fund reinvests dividends, but HMRC still
    taxes them as income when they arise — HMRC CG57707, already cited in
    dossiers/sp500.md), with the taxed amount added to the CGT cost basis to
    avoid double taxation on eventual disposal.

    Each year's total return is split into a dividend/income component
    (Damodaran's own published dividend yield for that year) and a residual
    price/capital-gain component (total return minus dividend yield) — a
    standard approximation, not an exact decomposition. See README.md "Tax
    scenarios" for the full reasoning and its limitations.

    Returns (total_cash_in, net_proceeds).
    """
    rate_start = fx[start_year - 1]
    invested_usd = ILLUSTRATIVE_LUMP_SUM_GBP / rate_start
    value_usd = invested_usd

    cumulative_dividend_tax_gbp = 0.0
    cumulative_cost_basis_addition_gbp = 0.0

    for y in range(start_year, end_year + 1):
        # No silent default here (a skeptic review, 2026-09-24, flagged the previous
        # yields.get(y, 0.0) as a latent silent-failure risk): compute_window's own
        # coverage check already guarantees y is in yields before this runs, so a
        # missing year should raise loudly, not quietly understate dividend tax.
        dividend_yield_y = yields[y]
        notional_dividend_usd = value_usd * dividend_yield_y

        # Grow the whole position (price + reinvested dividend), net of ongoing costs —
        # the fund itself reinvests automatically; only the tax treatment is separate.
        # Same OCF + capped-platform-fee mechanism as the sheltered scenario.
        value_usd = _grow_one_year(value_usd, y, damodaran, fx)

        # The notional distribution is taxed as income in the year it arises, converted
        # to GBP at that year's own year-end rate (a real, dated conversion, not the
        # window's endpoint rate) — dividend tax is a real annual event, not a one-off.
        dividend_gbp = notional_dividend_usd * fx[y]
        taxable_dividend = max(0.0, dividend_gbp - DIVIDEND_ALLOWANCE_GBP)
        cumulative_dividend_tax_gbp += taxable_dividend * DIVIDEND_TAX_RATE
        # HMRC CG57707: the notional distribution is allowable expenditure (added to cost
        # basis) where it is subject to Income Tax — i.e. the taxed portion, not the
        # allowance-covered portion.
        cumulative_cost_basis_addition_gbp += taxable_dividend

    rate_end = fx[end_year]
    grown_gbp = value_usd * rate_end

    total_cash_in = ILLUSTRATIVE_LUMP_SUM_GBP * (1 + spread_rate) + BUY_COMMISSION_GBP
    gross_proceeds = grown_gbp * (1 - spread_rate) - SELL_COMMISSION_GBP

    adjusted_cost_basis = total_cash_in + cumulative_cost_basis_addition_gbp
    chargeable_gain = max(
        0.0, (gross_proceeds - adjusted_cost_basis) - CGT_ANNUAL_EXEMPT_GBP
    )
    cgt_due = chargeable_gain * CGT_RATE

    net_proceeds = gross_proceeds - cgt_due - cumulative_dividend_tax_gbp
    return total_cash_in, net_proceeds


def compute_window(start_year, length, damodaran, yields, fx, cpi):
    """Compute one (start_year, length) window. Returns a dict, or None if data is missing."""
    end_year = start_year + length - 1
    years_needed = list(range(start_year, end_year + 1))

    if any(y not in damodaran for y in years_needed):
        return None
    if any(y not in yields for y in years_needed):
        return None
    if (start_year - 1) not in fx or any(y not in fx for y in years_needed):
        return None
    if (start_year - 1) not in cpi or end_year not in cpi:
        return None

    rate_start = fx[start_year - 1]
    rate_end = fx[end_year]

    cpi_start = cpi[start_year - 1]
    cpi_end = cpi[end_year]
    avg_annual_inflation = (cpi_end / cpi_start) ** (1 / length) - 1

    result = {
        "start_year": start_year,
        "end_year": end_year,
        "window_length": length,
        "fx_rate_start": rate_start,
        "fx_rate_end": rate_end,
        "avg_annual_inflation": avg_annual_inflation,
    }

    for spread_label, spread_rate in (("floor", 0.0), ("ceiling", SPREAD_CEILING_RATE)):
        sheltered_cash_in, sheltered_proceeds = _sheltered_scenario(
            start_year, end_year, damodaran, fx, spread_rate
        )
        sheltered_nominal = (sheltered_proceeds / sheltered_cash_in) ** (1 / length) - 1
        sheltered_real = (1 + sheltered_nominal) / (1 + avg_annual_inflation) - 1

        taxable_cash_in, taxable_proceeds = _taxable_scenario(
            start_year, end_year, damodaran, yields, fx, spread_rate
        )
        taxable_nominal = (taxable_proceeds / taxable_cash_in) ** (1 / length) - 1
        taxable_real = (1 + taxable_nominal) / (1 + avg_annual_inflation) - 1

        result[f"sheltered_total_cash_in_gbp_{spread_label}"] = round(sheltered_cash_in, 2)
        result[f"sheltered_net_proceeds_gbp_{spread_label}"] = round(sheltered_proceeds, 2)
        result[f"sheltered_nominal_annual_return_{spread_label}"] = sheltered_nominal
        result[f"sheltered_net_real_return_{spread_label}"] = sheltered_real

        result[f"taxable_total_cash_in_gbp_{spread_label}"] = round(taxable_cash_in, 2)
        result[f"taxable_net_proceeds_gbp_{spread_label}"] = round(taxable_proceeds, 2)
        result[f"taxable_nominal_annual_return_{spread_label}"] = taxable_nominal
        result[f"taxable_net_real_return_{spread_label}"] = taxable_real

    return result


def build_results(damodaran, yields, fx, cpi):
    results = []
    min_year = min(damodaran)
    max_year = max(damodaran)
    for length in WINDOW_LENGTHS:
        for start_year in range(min_year, max_year - length + 2):
            row = compute_window(start_year, length, damodaran, yields, fx, cpi)
            if row is not None:
                results.append(row)
    return results


SCENARIOS = [
    ("sheltered", "floor"), ("sheltered", "ceiling"),
    ("taxable", "floor"), ("taxable", "ceiling"),
]


def build_summary(results):
    summary = []
    by_length = {}
    for r in results:
        by_length.setdefault(r["window_length"], []).append(r)

    for length in WINDOW_LENGTHS:
        rows = by_length.get(length, [])
        if not rows:
            continue
        summary_row = {"window_length": length, "n_windows": len(rows)}
        for tax, spread in SCENARIOS:
            key = f"{tax}_net_real_return_{spread}"
            prefix = f"{tax}_{spread}"
            rows_sorted = sorted(rows, key=lambda r: r[key])
            worst = rows_sorted[0]
            best = rows_sorted[-1]
            med = median(r[key] for r in rows)
            summary_row[f"median_net_real_return_{prefix}"] = med
            summary_row[f"worst_net_real_return_{prefix}"] = worst[key]
            summary_row[f"worst_start_year_{prefix}"] = worst["start_year"]
            summary_row[f"worst_end_year_{prefix}"] = worst["end_year"]
            summary_row[f"best_net_real_return_{prefix}"] = best[key]
            summary_row[f"best_start_year_{prefix}"] = best["start_year"]
            summary_row[f"best_end_year_{prefix}"] = best["end_year"]
        summary.append(summary_row)
    return summary


def write_results_csv(results, path):
    fieldnames = [
        "start_year", "end_year", "window_length", "fx_rate_start", "fx_rate_end",
        "avg_annual_inflation",
    ]
    for tax, spread in SCENARIOS:
        prefix = f"{tax}_{spread}"
        fieldnames += [
            f"{tax}_total_cash_in_gbp_{spread}", f"{tax}_net_proceeds_gbp_{spread}",
            f"{tax}_nominal_annual_return_{spread}", f"{tax}_net_real_return_{spread}",
        ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in sorted(results, key=lambda r: (r["window_length"], r["start_year"])):
            writer.writerow(r)


def write_summary_csv(summary, path):
    fieldnames = ["window_length", "n_windows"]
    for tax, spread in SCENARIOS:
        prefix = f"{tax}_{spread}"
        fieldnames += [
            f"median_net_real_return_{prefix}",
            f"worst_net_real_return_{prefix}", f"worst_start_year_{prefix}", f"worst_end_year_{prefix}",
            f"best_net_real_return_{prefix}", f"best_start_year_{prefix}", f"best_end_year_{prefix}",
        ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in summary:
            writer.writerow(row)


def main():
    for path in (DAMODARAN_XLS, BOE_HTML, ONS_CSV):
        if not path.exists():
            print(f"ERROR: missing raw data file {path} — run fetch_raw_data.py first", file=sys.stderr)
            return 1

    damodaran, yields = load_damodaran_returns_and_yields(DAMODARAN_XLS)
    fx = load_boe_year_end_rates(BOE_HTML)
    cpi = load_ons_december_cpi(ONS_CSV)

    results = build_results(damodaran, yields, fx, cpi)
    summary = build_summary(results)

    write_results_csv(results, BENCHMARK_DIR / "results.csv")
    write_summary_csv(summary, BENCHMARK_DIR / "summary.csv")

    print(f"Wrote {len(results)} window(s) to results.csv")
    print(f"Wrote {len(summary)} summary row(s) to summary.csv")
    for row in summary:
        print(f"  {row['window_length']:2d}yr ({row['n_windows']} windows):")
        for tax, spread in SCENARIOS:
            prefix = f"{tax}_{spread}"
            print(
                f"    {tax:9s}/{spread:8s}: median {row[f'median_net_real_return_{prefix}']:+.2%}, "
                f"worst {row[f'worst_net_real_return_{prefix}']:+.2%} "
                f"({row[f'worst_start_year_{prefix}']}-{row[f'worst_end_year_{prefix}']}), "
                f"best {row[f'best_net_real_return_{prefix}']:+.2%} "
                f"({row[f'best_start_year_{prefix}']}-{row[f'best_end_year_{prefix}']})"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
