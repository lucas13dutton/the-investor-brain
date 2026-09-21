#!/usr/bin/env python3
"""Build the S&P 500 GBP benchmark: nominal, cost-adjusted and net real returns
for every available start year, at window lengths of 1, 5, 10 and 20 years.

Data sources (raw files in data/raw/, gitignored, downloaded by
fetch_raw_data.py — see README.md for URLs, access dates and licence notes):
  - Damodaran's annual S&P 500 total return series (NYU Stern), 1928-2025.
  - Bank of England XUDLGBD daily GBP-per-USD spot rate, 1975-present.
  - ONS CPI (D7BT, all items index, 2015=100), annual, 1988-2025.

See README.md in this folder for the full method and every assumption,
including how FX timing is handled and why the usable range starts in 1989.

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


def load_ons_annual_cpi(csv_path):
    """Return {year: CPI index value (annual average)} from the raw ONS CSV export."""
    cpi = {}
    year_row_re = re.compile(r"^(\d{4})$")
    with csv_path.open(newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) != 2:
                continue
            year_field, value_field = row
            if year_row_re.match(year_field):
                cpi[int(year_field)] = float(value_field)
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

    # 1. Cost-adjusted USD growth factor, compounded year by year.
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

    total_cash_in = ILLUSTRATIVE_LUMP_SUM_GBP + BUY_COMMISSION_GBP
    net_proceeds = grown_gbp - SELL_COMMISSION_GBP

    nominal_annual_return = (net_proceeds / total_cash_in) ** (1 / length) - 1

    # 3. Deflate by average annual CPI inflation over the same window.
    cpi_start = cpi[start_year - 1]
    cpi_end = cpi[end_year]
    avg_annual_inflation = (cpi_end / cpi_start) ** (1 / length) - 1

    net_real_return = (1 + nominal_annual_return) / (1 + avg_annual_inflation) - 1

    return {
        "start_year": start_year,
        "end_year": end_year,
        "window_length": length,
        "fx_rate_start": rate_start,
        "fx_rate_end": rate_end,
        "total_cash_in_gbp": round(total_cash_in, 2),
        "net_proceeds_gbp": round(net_proceeds, 2),
        "nominal_annual_return": nominal_annual_return,
        "avg_annual_inflation": avg_annual_inflation,
        "net_real_return": net_real_return,
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
        rows_sorted = sorted(rows, key=lambda r: r["net_real_return"])
        worst = rows_sorted[0]
        best = rows_sorted[-1]
        med = median(r["net_real_return"] for r in rows)
        summary.append({
            "window_length": length,
            "n_windows": len(rows),
            "median_net_real_return": med,
            "worst_net_real_return": worst["net_real_return"],
            "worst_start_year": worst["start_year"],
            "worst_end_year": worst["end_year"],
            "best_net_real_return": best["net_real_return"],
            "best_start_year": best["start_year"],
            "best_end_year": best["end_year"],
        })
    return summary


def write_results_csv(results, path):
    fieldnames = [
        "start_year", "end_year", "window_length", "fx_rate_start", "fx_rate_end",
        "total_cash_in_gbp", "net_proceeds_gbp", "nominal_annual_return",
        "avg_annual_inflation", "net_real_return",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in sorted(results, key=lambda r: (r["window_length"], r["start_year"])):
            writer.writerow(r)


def write_summary_csv(summary, path):
    fieldnames = [
        "window_length", "n_windows", "median_net_real_return",
        "worst_net_real_return", "worst_start_year", "worst_end_year",
        "best_net_real_return", "best_start_year", "best_end_year",
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
    cpi = load_ons_annual_cpi(ONS_CSV)

    results = build_results(damodaran, fx, cpi)
    summary = build_summary(results)

    write_results_csv(results, BENCHMARK_DIR / "results.csv")
    write_summary_csv(summary, BENCHMARK_DIR / "summary.csv")

    print(f"Wrote {len(results)} window(s) to results.csv")
    print(f"Wrote {len(summary)} summary row(s) to summary.csv")
    for row in summary:
        print(
            f"  {row['window_length']:2d}yr ({row['n_windows']} windows): "
            f"median {row['median_net_real_return']:+.2%}, "
            f"worst {row['worst_net_real_return']:+.2%} "
            f"({row['worst_start_year']}-{row['worst_end_year']}), "
            f"best {row['best_net_real_return']:+.2%} "
            f"({row['best_start_year']}-{row['best_end_year']})"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
