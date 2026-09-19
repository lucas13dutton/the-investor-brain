#!/usr/bin/env python3
"""Unit tests for data/evidence/validate.py.

Each test builds one or more deliberately broken rows and asserts the
specific rule fires with a matching error, plus one control test proving a
fully valid row passes clean. Run directly:

    python3 data/evidence/test_validate.py
"""

import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate  # noqa: E402


def base_row(**overrides):
    """A minimal, fully valid row. Tests override just the field(s) they want broken."""
    row = {
        "claim_id": "TEST-0001",
        "claim_text": "A test claim with a real number.",
        "asset": "test",
        "window": "n/a",
        "cost_scenario": "n/a",
        "tax_scenario": "n/a",
        "value": "1",
        "unit": "%",
        "source_1_name": "Some Official Body — some page",
        "source_1_tier": "A",
        "source_1_quote": "The exact quoted clause.",
        "source_1_url": "example.gov.uk/page",
        "source_1_accessed": "2026-09-19",
        "source_2_name": "",
        "source_2_tier": "",
        "source_2_quote": "",
        "source_2_url": "",
        "source_2_accessed": "",
        "calculation_ref": "n/a — directly sourced",
        "checked_by": "skeptic agent, reviews/test-review.md",
        "approved_by": "",
        "status": "draft",
        "created": "2026-09-19",
        "last_verified": "2026-09-19",
    }
    row.update(overrides)
    return row


TODAY = date(2026, 9, 19)


class TestValidRowPasses(unittest.TestCase):
    def test_control_row_has_no_errors(self):
        errors = validate.validate_row(base_row(), today=TODAY)
        self.assertEqual(errors, [], f"a fully valid row should have no errors, got: {errors}")

    def test_control_row_set_has_no_failures(self):
        rows = [base_row(claim_id="TEST-0001"), base_row(claim_id="TEST-0002")]
        failures = validate.validate_rows(rows, today=TODAY)
        self.assertEqual(failures, [], f"a valid row set should have no failures, got: {failures}")


class TestDuplicateClaimId(unittest.TestCase):
    def test_duplicate_claim_id_fails(self):
        rows = [
            base_row(claim_id="TEST-0001"),
            base_row(claim_id="TEST-0001"),  # deliberate duplicate
        ]
        failures = validate.validate_rows(rows, today=TODAY)
        self.assertEqual(len(failures), 2, "both rows sharing the duplicate id should fail")
        for claim_id, errors in failures:
            self.assertTrue(
                any("duplicated" in e for e in errors),
                f"expected a duplicate-id error for {claim_id}, got: {errors}",
            )


class TestMissingSource(unittest.TestCase):
    def test_no_complete_source_fails(self):
        row = base_row(source_1_tier="", source_1_quote="", source_1_accessed="")
        errors = validate.validate_row(row, today=TODAY)
        self.assertTrue(
            any("no source has a tier" in e for e in errors),
            f"expected a missing-source error, got: {errors}",
        )

    def test_partial_source_missing_quote_fails(self):
        # Tier and accessed date given, but no quote — still incomplete.
        row = base_row(source_1_quote="")
        errors = validate.validate_row(row, today=TODAY)
        self.assertTrue(
            any("no source has a tier" in e for e in errors),
            f"expected a missing-source error for a source with no quote, got: {errors}",
        )

    def test_complete_source_2_alone_is_sufficient(self):
        # source_1 incomplete, but source_2 fully filled in — should pass this rule.
        row = base_row(
            source_1_tier="", source_1_quote="", source_1_accessed="",
            source_2_name="A second source",
            source_2_tier="B",
            source_2_quote="A quoted clause.",
            source_2_url="example.com",
            source_2_accessed="2026-09-19",
        )
        errors = validate.validate_row(row, today=TODAY)
        self.assertFalse(
            any("no source has a tier" in e for e in errors),
            f"a complete source_2 alone should satisfy this rule, got: {errors}",
        )


class TestTierCOnlyWithoutMarker(unittest.TestCase):
    def test_tier_c_only_no_marker_fails(self):
        row = base_row(source_1_tier="C")
        errors = validate.validate_row(row, today=TODAY)
        self.assertTrue(
            any("Tier C source(s)" in e for e in errors),
            f"expected a Tier-C-only error, got: {errors}",
        )

    def test_tier_c_only_with_sensitivity_marker_passes(self):
        row = base_row(
            source_1_tier="C",
            claim_text="A test claim, treated as a labelled SENSITIVITY per methodology section 3.",
        )
        errors = validate.validate_row(row, today=TODAY)
        self.assertFalse(
            any("Tier C source(s)" in e for e in errors),
            f"a SENSITIVITY marker should clear this rule, got: {errors}",
        )

    def test_tier_c_only_with_exception_marker_passes(self):
        row = base_row(
            source_1_tier="C",
            calculation_ref="n/a — EXCEPTION APPROVED by Lucas, 2026-09-19",
        )
        errors = validate.validate_row(row, today=TODAY)
        self.assertFalse(
            any("Tier C source(s)" in e for e in errors),
            f"an EXCEPTION APPROVED marker should clear this rule, got: {errors}",
        )

    def test_mixed_tier_a_and_c_does_not_trigger_rule(self):
        row = base_row(
            source_1_tier="A",
            source_2_name="A Tier C source",
            source_2_tier="C",
            source_2_quote="Some quote.",
            source_2_url="example.com",
            source_2_accessed="2026-09-19",
        )
        errors = validate.validate_row(row, today=TODAY)
        self.assertFalse(
            any("Tier C source(s)" in e for e in errors),
            f"a row with at least one non-Tier-C source should not trigger this rule, got: {errors}",
        )


class TestLiveWithoutApproval(unittest.TestCase):
    def test_live_without_approved_by_fails(self):
        row = base_row(status="live", approved_by="")
        errors = validate.validate_row(row, today=TODAY)
        self.assertTrue(
            any("approved_by is blank" in e for e in errors),
            f"expected a live-without-approval error, got: {errors}",
        )

    def test_live_with_approved_by_passes(self):
        row = base_row(status="live", approved_by="Lucas, 2026-09-19")
        errors = validate.validate_row(row, today=TODAY)
        self.assertFalse(
            any("approved_by is blank" in e for e in errors),
            f"a live row with approved_by set should pass this rule, got: {errors}",
        )

    def test_draft_without_approved_by_passes(self):
        row = base_row(status="draft", approved_by="")
        errors = validate.validate_row(row, today=TODAY)
        self.assertFalse(
            any("approved_by is blank" in e for e in errors),
            f"a draft row should not need approved_by, got: {errors}",
        )


class TestLastVerifiedAge(unittest.TestCase):
    def test_last_verified_over_12_months_fails(self):
        stale_date = (TODAY - timedelta(days=400)).isoformat()
        row = base_row(last_verified=stale_date)
        errors = validate.validate_row(row, today=TODAY)
        self.assertTrue(
            any("more than 365 days" in e for e in errors),
            f"expected a stale last_verified error, got: {errors}",
        )

    def test_last_verified_missing_fails(self):
        row = base_row(last_verified="")
        errors = validate.validate_row(row, today=TODAY)
        self.assertTrue(
            any("missing or not a valid" in e for e in errors),
            f"expected a missing last_verified error, got: {errors}",
        )

    def test_last_verified_within_12_months_passes(self):
        recent_date = (TODAY - timedelta(days=200)).isoformat()
        row = base_row(last_verified=recent_date)
        errors = validate.validate_row(row, today=TODAY)
        self.assertEqual(
            [e for e in errors if "365 days" in e or "missing or not a valid" in e],
            [],
            f"a recent last_verified date should pass, got: {errors}",
        )

    def test_last_verified_exactly_365_days_passes(self):
        boundary_date = (TODAY - timedelta(days=365)).isoformat()
        row = base_row(last_verified=boundary_date)
        errors = validate.validate_row(row, today=TODAY)
        self.assertEqual(
            [e for e in errors if "365 days" in e],
            [],
            f"exactly 365 days old should not yet be 'more than' 365 days, got: {errors}",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
