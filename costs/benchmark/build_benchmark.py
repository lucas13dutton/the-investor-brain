#!/usr/bin/env python3
"""Build the S&P 500 GBP benchmark: nominal, cost-adjusted and net real returns
for every available start year, at window lengths of 1, 5, 10 and 20 years.

Data sources (raw files in data/raw/, gitignored, downloaded by
fetch_raw_data.py — see README.md for URLs, access dates and licence notes):
  - Damodaran's annual S&P 500 total return series (NYU Stern), 1928-2025.
  - Bank of England XUDLGBD daily GBP-per-USD spot rate, 1975-present.
  - ONS CPI (D7BT, all items index, 2015=100), December-on-December, 1988-2025.

Every window is computed twice: a "floor" scenario (the ETF bid-ask spread
excluded, since no source for it was ever found) and a "ceiling" scenario
(the spread included at its labelled 0.05% sensitivity upper bound, applied
each way) — per methodology section 3's unsourced-cost sensitivity rule,
which requires showing both, not just the excluded version. See README.md.

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
ANNUAL_PLATFORM_FEE_RATE = 0.0025  # SP500-0013, AJ Bell, central, 0.25% p.a. (cap not reached at this lump sum)
ANNUAL_COST_DRAG = ANNUAL_OCF_RATE + ANNUAL_PLATFORM_FEE_RATE  # 0.0032

# SP500-0004: the ETF bid-ask spread, a labelled sensitivity with no real source.
# "Floor" = excluded (£0). "Ceiling" = the dossier's own stated 0.05% (5bps) upper
# bound, applied once on the way in and once on the way out, as a % of the
# traded value at that point — not an invented central figure either way.
SPREAD_CEILING_RATE = 0.0005


def load_damodaran_returns(xls_path):
    """Return {year: annual USD total return (decimal)} from the Damodaran workbook."""
    import pandas as pd

    df = pd.read_excel(xls_path, sheet_name="Returns by year", header=19)
    df = df[["Year", "S&P 500 (includes dividends)"]].dropna()
    returns = {}
    for _, row in df.iterrows():
        year_raw = row["Year"]
        if not isinstance(year_raw, (int, float)):
            continue  # skip summary rows like "1928-2025"
        year = int(year_raw)
        returns[year] = float(row["S&P 500 (includes dividends)"])
    return returns


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


def compute_window(start_year, length, damodaran, fx, cpi):
    """Compute one (start_year, length) window. Returns a dict, or None if data is missing."""
    end_year = start_year + length - 1
    years_needed = range(start_year, end_year + 1)

    if any(y not in damodaran for y in years_needed):
        return None
    if (start_year - 1) not in fx or end_year not in fx:
        return None
    if (start_year - 1) not in cpi or end_year not in cpi:
        return None

    # 1. Cost-adjusted USD growth factor, compounded year by year (spread not yet applied).
    usd_growth = 1.0
    for y in years_needed:
        usd_growth *= (1 + damodaran[y]) * (1 - ANNUAL_COST_DRAG)

    # 2. FX conversion: buy at end-of-(start_year-1) rate, sell at end-of-end_year rate.
    #    Rate is GBP per USD (see README "FX timing and direction").
    rate_start = fx[start_year - 1]
    rate_end = fx[end_year]

    invested_gbp = ILLUSTRATIVE_LUMP_SUM_GBP
    invested_usd = invested_gbp / rate_start
    grown_usd = invested_usd * usd_growth
    grown_gbp = grown_usd * rate_end

    # 3. Deflate by December-on-December CPI inflation over the same window.
    cpi_start = cpi[start_year - 1]
    cpi_end = cpi[end_year]
    avg_annual_inflation = (cpi_end / cpi_start) ** (1 / length) - 1

    def scenario(spread_rate):
        total_cash_in = ILLUSTRATIVE_LUMP_SUM_GBP * (1 + spread_rate) + BUY_COMMISSION_GBP
        net_proceeds = grown_gbp * (1 - spread_rate) - SELL_COMMISSION_GBP
        nominal = (net_proceeds / total_cash_in) ** (1 / length) - 1
        real = (1 + nominal) / (1 + avg_annual_inflation) - 1
        return round(total_cash_in, 2), round(net_proceeds, 2), nominal, real

    floor_cash_in, floor_proceeds, floor_nominal, floor_real = scenario(0.0)
    ceiling_cash_in, ceiling_proceeds, ceiling_nominal, ceiling_real = scenario(SPREAD_CEILING_RATE)

    return {
        "start_year": start_year,
        "end_year": end_year,
        "window_length": length,
        "fx_rate_start": rate_start,
        "fx_rate_end": rate_end,
        "avg_annual_inflation": avg_annual_inflation,
        "total_cash_in_gbp_floor": floor_cash_in,
        "net_proceeds_gbp_floor": floor_proceeds,
        "nominal_annual_return_floor": floor_nominal,
        "net_real_return_floor": floor_real,
        "total_cash_in_gbp_ceiling": ceiling_cash_in,
        "net_proceeds_gbp_ceiling": ceiling_proceeds,
        "nominal_annual_return_ceiling": ceiling_nominal,
        "net_real_return_ceiling": ceiling_real,
    }


def build_results(damodaran, fx, cpi):
    results = []
    min_year = min(damodaran)
    max_year = max(damodaran)
    for length in WINDOW_LENGTHS:
        for start_year in range(min_year, max_year - length + 2):
            row = compute_window(start_year, length, damodaran, fx, cpi)
            if row is not None:
                results.append(row)
    return results


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
        for scenario in ("floor", "ceiling"):
            key = f"net_real_return_{scenario}"
            rows_sorted = sorted(rows, key=lambda r: r[key])
            worst = rows_sorted[0]
            best = rows_sorted[-1]
            med = median(r[key] for r in rows)
            summary_row[f"median_net_real_return_{scenario}"] = med
            summary_row[f"worst_net_real_return_{scenario}"] = worst[key]
            summary_row[f"worst_start_year_{scenario}"] = worst["start_year"]
            summary_row[f"worst_end_year_{scenario}"] = worst["end_year"]
            summary_row[f"best_net_real_return_{scenario}"] = best[key]
            summary_row[f"best_start_year_{scenario}"] = best["start_year"]
            summary_row[f"best_end_year_{scenario}"] = best["end_year"]
        summary.append(summary_row)
    return summary


def write_results_csv(results, path):
    fieldnames = [
        "start_year", "end_year", "window_length", "fx_rate_start", "fx_rate_end",
        "avg_annual_inflation",
        "total_cash_in_gbp_floor", "net_proceeds_gbp_floor",
        "nominal_annual_return_floor", "net_real_return_floor",
        "total_cash_in_gbp_ceiling", "net_proceeds_gbp_ceiling",
        "nominal_annual_return_ceiling", "net_real_return_ceiling",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in sorted(results, key=lambda r: (r["window_length"], r["start_year"])):
            writer.writerow(r)


def write_summary_csv(summary, path):
    fieldnames = ["window_length", "n_windows"]
    for scenario in ("floor", "ceiling"):
        fieldnames += [
            f"median_net_real_return_{scenario}",
            f"worst_net_real_return_{scenario}", f"worst_start_year_{scenario}", f"worst_end_year_{scenario}",
            f"best_net_real_return_{scenario}", f"best_start_year_{scenario}", f"best_end_year_{scenario}",
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

    damodaran = load_damodaran_returns(DAMODARAN_XLS)
    fx = load_boe_year_end_rates(BOE_HTML)
    cpi = load_ons_december_cpi(ONS_CSV)

    results = build_results(damodaran, fx, cpi)
    summary = build_summary(results)

    write_results_csv(results, BENCHMARK_DIR / "results.csv")
    write_summary_csv(summary, BENCHMARK_DIR / "summary.csv")

    print(f"Wrote {len(results)} window(s) to results.csv")
    print(f"Wrote {len(summary)} summary row(s) to summary.csv")
    for row in summary:
        print(f"  {row['window_length']:2d}yr ({row['n_windows']} windows):")
        for scenario in ("floor", "ceiling"):
            print(
                f"    {scenario:8s}: median {row[f'median_net_real_return_{scenario}']:+.2%}, "
                f"worst {row[f'worst_net_real_return_{scenario}']:+.2%} "
                f"({row[f'worst_start_year_{scenario}']}-{row[f'worst_end_year_{scenario}']}), "
                f"best {row[f'best_net_real_return_{scenario}']:+.2%} "
                f"({row[f'best_start_year_{scenario}']}-{row[f'best_end_year_{scenario}']})"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
