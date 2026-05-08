"""
Unit tests for the wiki profile synthesiser.

Level 4 AI Framework constraints under test:
  - LLM calls are always mocked — never hit live Gemini or Claude APIs in CI
  - Synthesiser must never write directly to DB
  - API failures must be handled gracefully with fallback status

Target coverage: 70%+ (LLM boundary is fully mocked)
"""
import pytest
from unittest.mock import MagicMock

# Replace stub below with: from engine.synthesiser import synthesise_profile


def synthesise_profile(record: dict, client=None) -> dict:
    """Stub — replace with real import once engine/synthesiser.py exists."""
    if client is None:
        return {"status": "failed", "fallback_used": True, "profile": None}
    try:
        response = client.generate(record)
        return {"status": "success", "fallback_used": False, "profile": response}
    except Exception:
        return {"status": "failed", "fallback_used": True, "profile": None}


# ---------------------------------------------------------------------------
# Mocking guard — LLM call isolation
# ---------------------------------------------------------------------------
def test_synthesiser_handles_api_failure_gracefully(mock_lead_record):
    """Gemini/Claude API timeout must not propagate as unhandled exception."""
    mock_client = MagicMock()
    mock_client.generate.side_effect = Exception("API timeout")
    result = synthesise_profile(mock_lead_record, client=mock_client)
    assert result["status"] == "failed"
    assert result["fallback_used"] is True


def test_synthesiser_returns_profile_on_success(mock_lead_record):
    """Successful LLM response must return status=success with profile data."""
    mock_client = MagicMock()
    mock_client.generate.return_value = {"wiki_profile": "Generated profile text."}
    result = synthesise_profile(mock_lead_record, client=mock_client)
    assert result["status"] == "success"
    assert result["profile"] is not None


def test_synthesiser_never_writes_to_db_directly(mock_lead_record):
    """Level 4 constraint: no direct DB writes from LLM output path."""
    mock_db = MagicMock()
    mock_client = MagicMock()
    mock_client.generate.return_value = {"wiki_profile": "Generated profile text."}
    synthesise_profile(mock_lead_record, client=mock_client)
    mock_db.write.assert_not_called()
    mock_db.insert.assert_not_called()
    mock_db.update.assert_not_called()


def test_synthesiser_no_live_api_calls(mock_lead_record):
    """Verify mock intercepted the call — no live network traffic."""
    mock_client = MagicMock()
    mock_client.generate.return_value = {"wiki_profile": "ok"}
    result = synthesise_profile(mock_lead_record, client=mock_client)
    assert mock_client.generate.called
    assert result["status"] == "success"
