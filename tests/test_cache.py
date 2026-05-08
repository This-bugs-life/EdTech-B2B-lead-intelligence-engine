"""
Unit tests for the Hot MD Cache generator.

Cache contract (from architecture):
  - Maximum 1,000 words
  - AE-ready leads only
  - 30-day rolling window (staleness enforced upstream)
  - Floor: 10 leads where available

Target coverage: 85%+
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from conftest import generate_mock_leads

# Replace stub below with: from engine.cache import build_hot_cache


def build_hot_cache(leads: list) -> str:
    """Stub — replace with real import once engine/cache.py exists."""
    ae_leads = [l for l in leads if l.get("ae_ready")]
    if not ae_leads:
        return ""
    lines = []
    for lead in ae_leads:
        line = (
            f"## {lead['company']} | {lead['role']}\n"
            f"Score: {lead.get('enrichment_score', 'N/A')} | "
            f"{lead.get('summary', '')}\n"
        )
        lines.append(line)
    cache = "\n".join(lines)
    words = cache.split()
    if len(words) > 1000:
        cache = " ".join(words[:1000])
    return cache


# ---------------------------------------------------------------------------
# Boundary tests
# ---------------------------------------------------------------------------
def test_cache_word_ceiling():
    """Cache must never exceed 1,000 words regardless of lead count."""
    leads = generate_mock_leads(200, ae_ready=True)
    cache = build_hot_cache(leads)
    word_count = len(cache.split())
    assert word_count <= 1000, f"Cache exceeded ceiling: {word_count} words"


def test_cache_ae_ready_filter():
    """Non-AE-ready leads must never appear in the cache."""
    leads = generate_mock_leads(5, ae_ready=False)
    cache = build_hot_cache(leads)
    assert cache == ""


def test_cache_mixed_ae_ready():
    """Only AE-ready leads from a mixed set should be in cache."""
    ready = generate_mock_leads(3, ae_ready=True)
    not_ready = generate_mock_leads(3, ae_ready=False)
    for i, l in enumerate(not_ready):
        l["company"] = f"ExcludedCorp {i}"
    cache = build_hot_cache(ready + not_ready)
    for lead in not_ready:
        assert lead["company"] not in cache, (
            f"Non-AE-ready lead '{lead['company']}' leaked into cache."
        )


def test_cache_empty_input():
    """Empty lead list must return empty string, not raise."""
    cache = build_hot_cache([])
    assert cache == ""


def test_cache_is_string():
    """Cache output must always be a string."""
    leads = generate_mock_leads(5, ae_ready=True)
    cache = build_hot_cache(leads)
    assert isinstance(cache, str)
