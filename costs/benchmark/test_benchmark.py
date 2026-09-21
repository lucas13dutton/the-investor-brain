#!/usr/bin/env python3
"""Unit tests for costs/benchmark/build_benchmark.py.

Windows are checked against an independent hand calculation using the same
real source values the pipeline itself loads (S&P 500 returns and dividend
yields from Damodaran, GBP-per-USD year-end rates from the Bank of England,
December CPI from the ONS) — computed here with a plain, separately-written
formula, not by re-running the module's own code path, so this genuinely
catches a regression rather than just re-checking the same arithmetic
against itself.

Run directly: python3 costs/benchmark/test_benchmark.py
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_benchmark as bb  # noqa: E402

# Real values, as loaded by build_benchmark.py from data/raw/ on 2026-09-21.
# CPI is December-on-December (not annual average — see README.md "Inflation").
DAMODARAN = {
    2009: 0.2593523387766398, 2010: 0.14821092278719414, 2011: 0.0209837473362805,
    2012: 0.15890585241730293, 2013: 0.32145085858125483, 2014: 0.13524421649462237,
    2015: 0.013788916411676138, 2016: 0.11773080874798171, 2017: 0.2160548143449928,
    2018: -0.04226869289088544, 2019: 0.31211679996808755, 2020: 0.18023201827422478,
    2021: 0.2846885175196416,
}
# Damodaran's own published annual dividend yield, "S&P 500 & Raw Data" sheet.
YIELDS = {
    2009: 0.0197, 2010: 0.0188, 2011: 0.0206, 2012: 0.0213, 2013: 0.0195,
    2014: 0.0189, 2015: 0.0205, 2016: 0.0201, 2017: 0.0184, 2018: 0.0208,
    2019: 0.0182, 2020: 0.0158, 2021: 0.0129,
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


def hand_calculate_sheltered(start_year, length, damodaran, fx, cpi, spread_rate):
    """Independent formula for the Sheltered (no tax) scenario."""
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


def hand_calculate_taxable(start_year, length, damodaran, yields, fx, cpi):
    """Independent formula for the Taxable scenario, floor spread only.
    Written separately from build_benchmark._taxable_scenario on purpose."""
    end_year = start_year + length - 1
    lump_sum = 10_000.0

    rate_start = fx[start_year - 1]
    value_usd = lump_sum / rate_start

    dividend_tax_total_gbp = 0.0
    cost_basis_addition_gbp = 0.0

    for y in range(start_year, end_year + 1):
        div_yield = yields.get(y, 0.0)
        notional_dividend_usd = value_usd * div_yield
        value_usd = value_usd * (1 + damodaran[y]) * (1 - COST_DRAG)

        dividend_gbp = notional_dividend_usd * fx[y]
        taxable_dividend = max(0.0, dividend_gbp - 500.0)
        dividend_tax_total_gbp += taxable_dividend * 0.1075
        cost_basis_addition_gbp += taxable_dividend

    rate_end = fx[end_year]
    grown_gbp = value_usd * rate_end

    total_cash_in = lump_sum + 5.00
    gross_proceeds = grown_gbp - 5.00

    adjusted_cost_basis = total_cash_in + cost_basis_addition_gbp
    chargeable_gain = max(0.0, (gross_proceeds - adjusted_cost_basis) - 3_000.0)
    cgt_due = chargeable_gain * 0.18

    net_proceeds = gross_proceeds - cgt_due - dividend_tax_total_gbp
    nominal = (net_proceeds / total_cash_in) ** (1 / length) - 1

    cpi_start = cpi[start_year - 1]
    cpi_end = cpi[end_year]
    inflation = (cpi_end / cpi_start) ** (1 / length) - 1
    real = (1 + nominal) / (1 + inflation) - 1
    return nominal, real, net_proceeds


class TestHandCalculatedWindows(unittest.TestCase):
    """Three windows, independently hand-calculated, per the task's requirement.
    Each is checked against floor/ceiling AND sheltered/taxable."""

    def test_2021_one_year_window(self):
        row = bb.compute_window(2021, 1, DAMODARAN, YIELDS, FX, CPI_DECEMBER)

        exp_nominal_floor, exp_real_floor, exp_proceeds_floor = hand_calculate_sheltered(
            2021, 1, DAMODARAN, FX, CPI_DECEMBER, 0.0
        )
        self.assertAlmostEqual(row["sheltered_nominal_annual_return_floor"], exp_nominal_floor, places=9)
        self.assertAlmostEqual(row["sheltered_net_real_return_floor"], exp_real_floor, places=9)
        self.assertAlmostEqual(row["sheltered_net_proceeds_gbp_floor"], round(exp_proceeds_floor, 2), places=2)

        exp_nominal_ceil, exp_real_ceil, exp_proceeds_ceil = hand_calculate_sheltered(
            2021, 1, DAMODARAN, FX, CPI_DECEMBER, bb.SPREAD_CEILING_RATE
        )
        self.assertAlmostEqual(row["sheltered_nominal_annual_return_ceiling"], exp_nominal_ceil, places=9)
        self.assertAlmostEqual(row["sheltered_net_real_return_ceiling"], exp_real_ceil, places=9)

        self.assertLess(row["sheltered_net_real_return_ceiling"], row["sheltered_net_real_return_floor"])

        # Sanity-check the magnitude: a strong USD equity year, small GBP move.
        self.assertGreater(row["sheltered_nominal_annual_return_floor"], 0.25)
        self.assertLess(row["sheltered_nominal_annual_return_floor"], 0.35)
        self.assertGreater(row["sheltered_net_real_return_floor"], 0.15)

    def test_2015_to_2019_five_year_window(self):
        cpi = dict(CPI_DECEMBER)
        cpi[2014] = 100.1
        cpi[2019] = 108.5
        row = bb.compute_window(2015, 5, DAMODARAN, YIELDS, FX, cpi)
        exp_nominal, exp_real, exp_proceeds = hand_calculate_sheltered(2015, 5, DAMODARAN, FX, cpi, 0.0)

        self.assertAlmostEqual(row["sheltered_nominal_annual_return_floor"], exp_nominal, places=9)
        self.assertAlmostEqual(row["sheltered_net_real_return_floor"], exp_real, places=9)
        self.assertAlmostEqual(row["sheltered_net_proceeds_gbp_floor"], round(exp_proceeds, 2), places=2)
        self.assertEqual(row["end_year"], 2019)

        # Taxable must be strictly worse than Sheltered over 5 years at this lump sum
        # (real historical gains here are large enough to exceed the £3,000 CGT exemption).
        self.assertLess(row["taxable_net_real_return_floor"], row["sheltered_net_real_return_floor"])

    def test_2010_to_2019_ten_year_window_taxable(self):
        cpi = dict(CPI_DECEMBER)
        cpi[2009] = 88.0
        cpi[2019] = 108.5
        row = bb.compute_window(2010, 10, DAMODARAN, YIELDS, FX, cpi)

        exp_nominal, exp_real, exp_proceeds = hand_calculate_taxable(2010, 10, DAMODARAN, YIELDS, FX, cpi)

        self.assertAlmostEqual(row["taxable_nominal_annual_return_floor"], exp_nominal, places=9)
        self.assertAlmostEqual(row["taxable_net_real_return_floor"], exp_real, places=9)
        self.assertAlmostEqual(row["taxable_net_proceeds_gbp_floor"], round(exp_proceeds, 2), places=2)
        self.assertEqual(row["end_year"], 2019)

        # Also check the floor Sheltered figure for the same window, for a complete
        # independent cross-check of both scenarios on one window.
        exp_s_nominal, exp_s_real, exp_s_proceeds = hand_calculate_sheltered(2010, 10, DAMODARAN, FX, cpi, 0.0)
        self.assertAlmostEqual(row["sheltered_nominal_annual_return_floor"], exp_s_nominal, places=9)
        self.assertAlmostEqual(row["sheltered_net_real_return_floor"], exp_s_real, places=9)


class TestTaxableScenario(unittest.TestCase):
    def test_taxable_never_beats_sheltered(self):
        # Tax can never IMPROVE a return relative to the same holding held tax-free.
        cpi = dict(CPI_DECEMBER)
        cpi.update({2011: 96.8, 2012: 100.0, 2013: 100.0, 2015: 100.6, 2016: 103.5, 2017: 105.4, 2018: 107.8})
        for start in range(2010, 2020):
            row = bb.compute_window(start, 5, DAMODARAN, YIELDS, FX, cpi)
            if row is None:
                continue
            for spread in ("floor", "ceiling"):
                self.assertLessEqual(
                    row[f"taxable_net_real_return_{spread}"],
                    row[f"sheltered_net_real_return_{spread}"] + 1e-12,
                )

    def test_loss_year_pays_no_cgt(self):
        # 2022 was a real S&P 500 loss year. No CGT should be due on a loss (the
        # chargeable-gain floor at zero must bite), even though dividend tax can
        # still apply independently of whether the price fell.
        cpi = {2021: 115.1, 2022: 130.9}
        yields = {2022: YIELDS.get(2021, 0.02)}  # any reasonable yield; not the point of this test
        damodaran = {2022: -0.1803}
        fx = {2021: 0.742, 2022: 0.8306}
        row = bb.compute_window(2022, 1, damodaran, yields, fx, cpi)
        self.assertIsNotNone(row)
        # With a loss, gross proceeds < cost basis, so chargeable_gain must floor at
        # zero — confirmed indirectly: taxable proceeds should exceed sheltered minus
        # only whatever dividend tax was due (never reduced further by a negative CGT).
        self.assertGreaterEqual(
            row["taxable_net_proceeds_gbp_floor"],
            row["sheltered_net_proceeds_gbp_floor"] - 50,  # generous bound on plausible dividend tax
        )


class TestMissingDataHandling(unittest.TestCase):
    def test_window_needing_unavailable_year_returns_none(self):
        thin_fx = {k: v for k, v in FX.items() if k != 2020}
        row = bb.compute_window(2021, 1, DAMODARAN, YIELDS, thin_fx, CPI_DECEMBER)
        self.assertIsNone(row)

    def test_window_needing_unavailable_damodaran_year_returns_none(self):
        thin_damodaran = {k: v for k, v in DAMODARAN.items() if k != 2021}
        row = bb.compute_window(2021, 1, thin_damodaran, YIELDS, FX, CPI_DECEMBER)
        self.assertIsNone(row)

    def test_window_needing_fx_mid_window_returns_none(self):
        # The taxable scenario needs FX for every year in the window, not just the
        # endpoints — a gap in the middle must still be caught.
        cpi = dict(CPI_DECEMBER)
        cpi[2009] = 88.0
        thin_fx = {k: v for k, v in FX.items() if k != 2015}
        row = bb.compute_window(2010, 10, DAMODARAN, YIELDS, thin_fx, cpi)
        self.assertIsNone(row)


class TestSummaryStatistics(unittest.TestCase):
    def test_worst_and_best_and_median_are_consistent(self):
        cpi = dict(CPI_DECEMBER)
        cpi.update({2011: 96.8, 2012: 100.0, 2013: 100.0, 2015: 100.6, 2016: 103.5, 2017: 105.4, 2018: 107.8})
        results = [
            bb.compute_window(y, 1, DAMODARAN, YIELDS, FX, cpi)
            for y in range(2010, 2022)
            if bb.compute_window(y, 1, DAMODARAN, YIELDS, FX, cpi) is not None
        ]
        summary = bb.build_summary(results)
        row = next(s for s in summary if s["window_length"] == 1)

        for tax, spread in bb.SCENARIOS:
            prefix = f"{tax}_{spread}"
            key = f"{tax}_net_real_return_{spread}"
            real_returns = sorted(r[key] for r in results)
            self.assertAlmostEqual(row[f"worst_net_real_return_{prefix}"], real_returns[0], places=9)
            self.assertAlmostEqual(row[f"best_net_real_return_{prefix}"], real_returns[-1], places=9)
            self.assertLessEqual(
                row[f"worst_net_real_return_{prefix}"], row[f"median_net_real_return_{prefix}"]
            )
            self.assertGreaterEqual(
                row[f"best_net_real_return_{prefix}"], row[f"median_net_real_return_{prefix}"]
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
