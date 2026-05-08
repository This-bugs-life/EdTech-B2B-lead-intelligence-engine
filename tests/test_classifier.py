"""
Unit tests for the data classification router.

Privacy-critical: wrong tier routing = potential data breach.
Target coverage: 95%+

Decision D-03: Amber is the default classification on ambiguity.
"""
import pytest

# Replace stub below with: from engine.classifier import classify_record


def classify_record(record: dict) -> str:
    """Stub — replace with real import once engine/classifier.py exists."""
    if record.get("pii_flag") and record.get("source") == "internal_crm":
        return "red"
    if record.get("consent") is None or record.get("source") == "scraped_email":
        return "amber"
    if record.get("pii_flag"):
        return "amber"
    if record.get("source") not in ("linkedin_public",):
        return "amber"
    return "green"


# ---------------------------------------------------------------------------
# Tier routing — parametrized matrix
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "record,expected_tier",
    [
        ({"source": "linkedin_public", "consent": True,  "pii_flag": False}, "green"),
        ({"source": "scraped_email",   "consent": None,  "pii_flag": False}, "amber"),
        ({"source": "linkedin_public", "consent": True,  "pii_flag": True},  "amber"),
        ({"source": "internal_crm",    "consent": True,  "pii_flag": True},  "red"),
    ],
)
def test_tier_routing(record, expected_tier):
    assert classify_record(record) == expected_tier


def test_amber_is_default_on_ambiguity():
    """D-03: must never silently promote ambiguous records to green."""
    ambiguous = {"source": "unknown", "consent": None, "pii_flag": False}
    assert classify_record(ambiguous) == "amber"


def test_unknown_source_defaults_to_amber():
    """Any unrecognised source must not pass to green."""
    record = {"source": "mystery_platform", "consent": True, "pii_flag": False}
    result = classify_record(record)
    assert result in ("amber", "red"), (
        f"Unknown source routed to '{result}' — must be amber or red, never green."
    )


def test_explicit_false_consent_routes_to_amber():
    record = {"source": "linkedin_public", "consent": False, "pii_flag": False}
    assert classify_record(record) != "green"


def test_red_requires_manual_cli_gate(mock_red_record):
    """Red-tier records must be classified as red, not promoted."""
    assert classify_record(mock_red_record) == "red"
