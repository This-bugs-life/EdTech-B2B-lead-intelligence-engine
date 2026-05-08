"""
Unit tests for the Weekly Linting Protocol scanner.

Linting rules under test:
  - Contradiction detection (e.g., green tier + pii_flag=True)
  - Orphaned page detection (no backlink)
  - Stale record detection (>30 days since last_updated)
  - Vault immutability: linter must report only, never delete

Target coverage: 75%+
"""
import pytest
from datetime import datetime, timedelta

# Replace stub below with: from engine.linter import run_lint_scan


def run_lint_scan(vault: dict) -> dict:
    """Stub — replace with real import once engine/linter.py exists."""
    issues = []
    for lead_id, record in vault.items():
        if record.get("tier") == "green" and record.get("pii_flag"):
            issues.append({"lead_id": lead_id, "type": "contradiction", "detail": "green + pii_flag"})
        if not record.get("backlink"):
            issues.append({"lead_id": lead_id, "type": "orphaned", "detail": "no backlink"})
        last_updated = record.get("last_updated")
        if last_updated:
            age = datetime.utcnow() - last_updated
            if age > timedelta(days=30):
                issues.append({"lead_id": lead_id, "type": "stale", "detail": f"{age.days} days old"})
    return {"issues": issues, "total": len(issues), "vault_size": len(vault)}


def create_vault_with_orphan():
    return {"lead_001": {"tier": "green", "pii_flag": False}}  # no backlink key


# ---------------------------------------------------------------------------
# Linting rule tests
# ---------------------------------------------------------------------------
def test_contradictory_tier_flags_detected():
    """Green tier + pii_flag=True must be flagged as contradiction."""
    vault = {"lead_001": {"tier": "green", "pii_flag": True, "backlink": "index"}}
    report = run_lint_scan(vault)
    assert any(i["type"] == "contradiction" for i in report["issues"])


def test_orphaned_pages_detected():
    """Records with no backlink must be flagged as orphaned."""
    vault = create_vault_with_orphan()
    report = run_lint_scan(vault)
    assert any(i["type"] == "orphaned" for i in report["issues"])


def test_stale_records_detected():
    """Records not updated in >30 days must be flagged as stale."""
    vault = {
        "lead_001": {
            "tier": "green",
            "pii_flag": False,
            "backlink": "index",
            "last_updated": datetime.utcnow() - timedelta(days=45),
        }
    }
    report = run_lint_scan(vault)
    assert any(i["type"] == "stale" for i in report["issues"])


def test_clean_vault_has_no_issues():
    """A well-formed vault with no violations must produce zero issues."""
    vault = {
        "lead_001": {
            "tier": "green",
            "pii_flag": False,
            "backlink": "index",
            "last_updated": datetime.utcnow() - timedelta(days=5),
        }
    }
    report = run_lint_scan(vault)
    assert report["total"] == 0


def test_lint_report_is_structured():
    """Lint output must always be a dict with 'issues' and 'total' keys."""
    report = run_lint_scan({})
    assert "issues" in report
    assert "total" in report
    assert isinstance(report["issues"], list)


def test_linter_does_not_delete_vault_entries():
    """Linter must report issues only — never mutate or delete vault records."""
    vault = {"lead_001": {"tier": "green", "pii_flag": True, "backlink": "index"}}
    original_size = len(vault)
    run_lint_scan(vault)
    assert len(vault) == original_size, "Linter mutated the vault — prohibited."
