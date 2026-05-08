"""
Shared fixtures for the Lead Intelligence Engine test suite.
All LLM API calls must be mocked — never hit live endpoints in CI.
"""
import pytest


@pytest.fixture
def mock_lead_record():
    """Minimal lead record fixture for unit tests."""
    return {
        "id": "lead_001",
        "source": "linkedin_public",
        "company": "Acme Corp",
        "role": "L&D Manager",
        "consent": True,
        "pii_flag": False,
        "ae_ready": True,
        "enrichment_score": 82,
        "summary": "Active in EdTech procurement discussions.",
    }


@pytest.fixture
def mock_amber_record():
    """Lead record with consent ambiguity — must always route to amber."""
    return {
        "id": "lead_002",
        "source": "scraped_email",
        "company": "Beta Ltd",
        "role": "Training Manager",
        "consent": None,
        "pii_flag": False,
        "ae_ready": False,
    }


@pytest.fixture
def mock_red_record():
    """Lead record with PII flag — must route to red tier."""
    return {
        "id": "lead_003",
        "source": "internal_crm",
        "company": "Gamma Inc",
        "role": "HR Director",
        "consent": True,
        "pii_flag": True,
        "ae_ready": False,
    }


def generate_mock_leads(count: int, ae_ready: bool = True) -> list:
    """Generate a list of mock lead records for cache boundary tests."""
    return [
        {
            "id": f"lead_{i:03d}",
            "source": "linkedin_public",
            "company": f"Company {i}",
            "role": "L&D Manager",
            "consent": True,
            "pii_flag": False,
            "ae_ready": ae_ready,
            "enrichment_score": 70 + (i % 30),
            "summary": f"Lead {i} summary for cache boundary testing.",
        }
        for i in range(count)
    ]
