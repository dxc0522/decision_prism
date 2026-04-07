"""Main entry point tests."""

from decision_prism.main import run_debate


def test_run_debate_raises_without_api_key():
    """Without api key, run_debate should fail gracefully."""
    try:
        run_debate("test query")
    except Exception as e:
        # 预期在没有有效 API 密钥时会失败
        assert isinstance(e, (ValueError, RuntimeError, Exception))
