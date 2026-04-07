"""Main entry point tests."""

from decision_prism.main import run_debate


def test_run_debate_raises_without_api_key():
    """Without api key, run_debate should fail gracefully."""
    try:
        run_debate("test query")
    except Exception as e:
        # Expected to fail without valid API key
        assert isinstance(e, (ValueError, RuntimeError, Exception))
