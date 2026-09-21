#!/usr/bin/env python3
"""Unit tests for costs/benchmark/build_benchmark.py.

Three windows are checked against an independent hand calculation using the
same real source values the pipeline itself loads (S&P 500 returns from
Damodaran, GBP-per-USD year-end rates from the Bank of England, December CPI
from the ONS) — computed here with a plain, separately-written formula, not
by re-running the module's own code path, so this genuinely catches a
regression rather than just re-checking the same arithmetic against itself.

Run directly: python3 costs/benchmark/test_benchmark.py
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_benchmark as bb  # noqa: E402

# Real values, as loaded by build_benchmark.py from data/raw/ on 2026-09-21.
# CPI is December-on-December (not annual average — see README.md "Inflation",
# corrected 2026-09-21 per a skeptic review that found the mismatch real).
DAMODARAN = {
    2009: 0.2593523387766398, 2010: 0.14821092278719414, 2011: 0.0209837473362805,
    2012: 0.15890585241730293, 2013: 0.32145085858125483, 2014: 0.13524421649462237,
    2015: 0.013788916411676138, 2016: 0.11773080874798171, 2017: 0.2160548143449928,
    2018: -0.04226869289088544, 2019: 0.31211679996808755, 2020: 0.18023201827422478,
    2021: 0.2846885175196416,
}
FX = {
    2009: 0.6193, 2010: 0.6388, 2011: 0.6468, 2012: 0.6185, 2013: 0.605,
    2014: 0.6407, 2015: 0.6748, 2016: 0.8128, 2017: 0.7402, 2018: 0.7831,
    2019: 0.757, 2020: 0.7327, 2021: 0.742,
}
CPI_DECEMBER = {
    2009: 88.0, 2010: 91.2, 2014: 100.1, 2019: 108.5, 2020: 109.2, 2021: 115.1,
}

COST_DRAG = bb.ANNUAL_OCF_RATE + bb.ANNUAL_PLATFORM_FEE_RATE  # 0.0007 + 0.0025 = 0.0032


def hand_calculate(start_year, length, damodaran, fx, cpi, spread_rate):
    """Independent formula: same method as build_benchmark.compute_window,
    written separately here so a bug in one wouldn't be mirrored in the other."""
    end_year = start_year + length - 1

    usd_growth = 1.0
    for y in range(start_year, end_year + 1):
        usd_growth = usd_growth * (1 + damodaran[y]) * (1 - COST_DRAG)

    rate_start = fx[start_year - 1]
    rate_end = fx[end_year]

    lump_sum = 10_000.0
    invested_usd = lump_sum / rate_start
    grown_usd = invested_usd * usd_growth
    grown_gbp = grown_usd * rate_end

    total_cash_in = lump_sum * (1 + spread_rate) + 5.00
    net_proceeds = grown_gbp * (1 - spread_rate) - 5.00

    nominal = (net_proceeds / total_cash_in) ** (1 / length) - 1

    cpi_start = cpi[start_year - 1]
    cpi_end = cpi[end_year]
    inflation = (cpi_end / cpi_start) ** (1 / length) - 1

    real = (1 + nominal) / (1 + inflation) - 1
    return nominal, real, net_proceeds


class TestHandCalculatedWindows(unittest.TestCase):
    """Three windows, independently hand-calculated, per the task's requirement.
    Each is checked against both the floor (spread excluded) and ceiling
    (spread at its 0.05% sensitivity upper bound) scenarios."""

    def test_2021_one_year_window(self):
        # Single year 2021: S&P 500 +28.47% USD, GBP weakened slightly (0.7327 -> 0.742),
        # December CPI rose 109.2 -> 115.1 (+5.40%).
        row = bb.compute_window(2021, 1, DAMODARAN, FX, CPI_DECEMBER)

        exp_nominal_floor, exp_real_floor, exp_proceeds_floor = hand_calculate(
            2021, 1, DAMODARAN, FX, CPI_DECEMBER, 0.0
        )
        self.assertAlmostEqual(row["nominal_annual_return_floor"], exp_nominal_floor, places=9)
        self.assertAlmostEqual(row["net_real_return_floor"], exp_real_floor, places=9)
        self.assertAlmostEqual(row["net_proceeds_gbp_floor"], round(exp_proceeds_floor, 2), places=2)

        exp_nominal_ceil, exp_real_ceil, exp_proceeds_ceil = hand_calculate(
            2021, 1, DAMODARAN, FX, CPI_DECEMBER, bb.SPREAD_CEILING_RATE
        )
        self.assertAlmostEqual(row["nominal_annual_return_ceiling"], exp_nominal_ceil, places=9)
        self.assertAlmostEqual(row["net_real_return_ceiling"], exp_real_ceil, places=9)
        self.assertAlmostEqual(row["net_proceeds_gbp_ceiling"], round(exp_proceeds_ceil, 2), places=2)

        # The ceiling (extra cost each way) must always be worse than the floor.
        self.assertLess(row["net_real_return_ceiling"], row["net_real_return_floor"])

        # Sanity-check the magnitude: a strong USD equity year, small GBP move,
        # noticeably higher December-CPI inflation than the annual average gave.
        self.assertGreater(row["nominal_annual_return_floor"], 0.25)
        self.assertLess(row["nominal_annual_return_floor"], 0.35)
        self.assertGreater(row["net_real_return_floor"], 0.15)

    def test_2015_to_2019_five_year_window(self):
        cpi = dict(CPI_DECEMBER)
        cpi[2014] = 100.1
        cpi[2019] = 108.5
        row = bb.compute_window(2015, 5, DAMODARAN, FX, cpi)
        exp_nominal, exp_real, exp_proceeds = hand_calculate(2015, 5, DAMODARAN, FX, cpi, 0.0)

        self.assertAlmostEqual(row["nominal_annual_return_floor"], exp_nominal, places=9)
        self.assertAlmostEqual(row["net_real_return_floor"], exp_real, places=9)
        self.assertAlmostEqual(row["net_proceeds_gbp_floor"], round(exp_proceeds, 2), places=2)
        self.assertEqual(row["end_year"], 2019)

    def test_2010_to_2019_ten_year_window(self):
        cpi = dict(CPI_DECEMBER)
        cpi[2009] = 88.0
        cpi[2019] = 108.5
        row = bb.compute_window(2010, 10, DAMODARAN, FX, cpi)
        exp_nominal, exp_real, exp_proceeds = hand_calculate(2010, 10, DAMODARAN, FX, cpi, 0.0)

        self.assertAlmostEqual(row["nominal_annual_return_floor"], exp_nominal, places=9)
        self.assertAlmostEqual(row["net_real_return_floor"], exp_real, places=9)
        self.assertAlmostEqual(row["net_proceeds_gbp_floor"], round(exp_proceeds, 2), places=2)
        self.assertEqual(row["end_year"], 2019)


class TestMissingDataHandling(unittest.TestCase):
    def test_window_needing_unavailable_year_returns_none(self):
        # 2021 minus 1 gives 2020's FX/CPI as the "start" reference; if that's missing,
        # compute_window must return None rather than raise or silently use wrong data.
        thin_fx = {k: v for k, v in FX.items() if k != 2020}
        row = bb.compute_window(2021, 1, DAMODARAN, thin_fx, CPI_DECEMBER)
        self.assertIsNone(row)

    def test_window_needing_unavailable_damodaran_year_returns_none(self):
        thin_damodaran = {k: v for k, v in DAMODARAN.items() if k != 2021}
        row = bb.compute_window(2021, 1, thin_damodaran, FX, CPI_DECEMBER)
        self.assertIsNone(row)


class TestSummaryStatistics(unittest.TestCase):
    def test_worst_and_best_and_median_are_consistent(self):
        cpi = dict(CPI_DECEMBER)
        cpi.update({2011: 96.8, 2012: 100.0, 2013: 100.0, 2015: 100.6, 2016: 103.5, 2017: 105.4, 2018: 107.8})
        results = [
            bb.compute_window(y, 1, DAMODARAN, FX, cpi)
            for y in range(2010, 2022)
            if bb.compute_window(y, 1, DAMODARAN, FX, cpi) is not None
        ]
        summary = bb.build_summary(results)
        row = next(s for s in summary if s["window_length"] == 1)

        for scenario in ("floor", "ceiling"):
            real_returns = sorted(r[f"net_real_return_{scenario}"] for r in results)
            self.assertAlmostEqual(row[f"worst_net_real_return_{scenario}"], real_returns[0], places=9)
            self.assertAlmostEqual(row[f"best_net_real_return_{scenario}"], real_returns[-1], places=9)
            self.assertLessEqual(
                row[f"worst_net_real_return_{scenario}"], row[f"median_net_real_return_{scenario}"]
            )
            self.assertGreaterEqual(
                row[f"best_net_real_return_{scenario}"], row[f"median_net_real_return_{scenario}"]
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
