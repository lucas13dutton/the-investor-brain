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
    """A minimal, fully valid 'claim' row. Tests override just the field(s) they want broken."""
    row = {
        "claim_id": "TEST-0001",
        "row_type": "claim",
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
        "source_1_url": "https://example.gov.uk/page",
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

    def test_tier_c_only_row_type_sensitivity_does_not_use_this_rule(self):
        # A genuinely unsourced cost is row_type "sensitivity", not a "claim" with a marker —
        # it must carry NO source at all, so this rule (which only applies to "claim" rows)
        # never even runs for it. See TestSensitivityRowType below for its own rule.
        row = base_row(row_type="sensitivity", value="5", unit="%")
        for n in (1, 2):
            row[f"source_{n}_name"] = row[f"source_{n}_tier"] = row[f"source_{n}_quote"] = ""
            row[f"source_{n}_url"] = row[f"source_{n}_accessed"] = ""
        errors = validate.validate_row(row, today=TODAY)
        self.assertFalse(
            any("Tier C source(s)" in e for e in errors),
            f"a sensitivity row should never hit the claim-only Tier-C rule, got: {errors}",
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


class TestQuoteIntegrity(unittest.TestCase):
    def test_no_verbatim_phrase_fails(self):
        row = base_row(source_1_quote="No verbatim quoted line could be found for this figure.")
        errors = validate.validate_row(row, today=TODAY)
        self.assertTrue(
            any("describes an absent quote" in e for e in errors),
            f"expected a quote-integrity error, got: {errors}",
        )

    def test_no_quotable_phrase_fails(self):
        row = base_row(source_1_quote="No quotable primary-source line was obtained in this pass.")
        errors = validate.validate_row(row, today=TODAY)
        self.assertTrue(
            any("describes an absent quote" in e for e in errors),
            f"expected a quote-integrity error, got: {errors}",
        )

    def test_real_quote_passes(self):
        row = base_row(source_1_quote="The rate is 0.12% per year, billed monthly.")
        errors = validate.validate_row(row, today=TODAY)
        self.assertFalse(
            any("describes an absent quote" in e for e in errors),
            f"a real quote should pass, got: {errors}",
        )

    def test_quote_integrity_only_applies_to_claim_rows(self):
        row = base_row(row_type="structural", source_1_quote="No verbatim source cited; a structural fact.")
        errors = validate.validate_row(row, today=TODAY)
        self.assertEqual(errors, [], f"structural rows skip quote-integrity too, got: {errors}")


class TestUrlFormat(unittest.TestCase):
    def test_missing_url_fails(self):
        row = base_row(source_1_url="")
        errors = validate.validate_row(row, today=TODAY)
        self.assertTrue(
            any("is blank" in e and "source_1_url" in e for e in errors),
            f"expected a blank-URL error, got: {errors}",
        )

    def test_non_http_url_fails(self):
        row = base_row(source_1_url="gov.uk (full page path not captured)")
        errors = validate.validate_row(row, today=TODAY)
        self.assertTrue(
            any("does not start with 'http'" in e for e in errors),
            f"expected a non-http URL error, got: {errors}",
        )

    def test_https_url_passes(self):
        row = base_row(source_1_url="https://www.gov.uk/some-page")
        errors = validate.validate_row(row, today=TODAY)
        self.assertEqual(
            [e for e in errors if "source_1_url" in e], [],
            f"an https URL should pass, got: {errors}",
        )


class TestStructuralRowType(unittest.TestCase):
    def test_structural_row_needs_no_source_at_all(self):
        row = base_row(row_type="structural")
        for n in (1, 2):
            for field in ("name", "tier", "quote", "url", "accessed"):
                row[f"source_{n}_{field}"] = ""
        errors = validate.validate_row(row, today=TODAY)
        self.assertEqual(errors, [], f"a structural row with no source should pass, got: {errors}")


class TestSensitivityRowType(unittest.TestCase):
    def _blank_row(self, **overrides):
        defaults = {"row_type": "sensitivity", "value": "5", "unit": "%"}
        for n in (1, 2):
            for field in ("name", "tier", "quote", "url", "accessed"):
                defaults[f"source_{n}_{field}"] = ""
        defaults.update(overrides)
        return base_row(**defaults)

    def test_sensitivity_with_bound_and_no_source_passes(self):
        row = self._blank_row()
        errors = validate.validate_row(row, today=TODAY)
        self.assertEqual(errors, [], f"a well-formed sensitivity row should pass, got: {errors}")

    def test_sensitivity_missing_value_fails(self):
        row = self._blank_row(value="")
        errors = validate.validate_row(row, today=TODAY)
        self.assertTrue(
            any("must state its bound" in e for e in errors),
            f"expected a missing-bound error, got: {errors}",
        )

    def test_sensitivity_with_source_attribution_fails(self):
        row = self._blank_row(source_1_tier="C", source_1_quote="some quote", source_1_accessed="2026-09-19")
        errors = validate.validate_row(row, today=TODAY)
        self.assertTrue(
            any("no source attribution" in e for e in errors),
            f"expected a source-attribution error, got: {errors}",
        )


class TestWithdrawnRowType(unittest.TestCase):
    def test_withdrawn_with_no_replacement_named_passes(self):
        row = base_row(row_type="withdrawn", claim_text="An old figure, now unreliable.")
        errors = validate.validate_row(row, today=TODAY)
        self.assertEqual(errors, [], f"withdrawn with no named replacement should pass, got: {errors}")

    def test_withdrawn_with_valid_replacement_passes(self):
        rows = [
            base_row(claim_id="TEST-0002"),
            base_row(claim_id="TEST-0001", row_type="withdrawn",
                     calculation_ref="n/a — WITHDRAWN, replaced by TEST-0002"),
        ]
        failures = validate.validate_rows(rows, today=TODAY)
        self.assertEqual(failures, [], f"a valid named replacement should pass, got: {failures}")

    def test_withdrawn_with_dangling_replacement_fails(self):
        rows = [
            base_row(claim_id="TEST-0001", row_type="withdrawn",
                     calculation_ref="n/a — WITHDRAWN, replaced by TEST-9999"),
        ]
        failures = validate.validate_rows(rows, today=TODAY)
        self.assertEqual(len(failures), 1)
        self.assertTrue(
            any("does not exist" in e for e in failures[0][1]),
            f"expected a dangling-replacement error, got: {failures}",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
