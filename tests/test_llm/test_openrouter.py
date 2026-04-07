"""OpenRouterProvider tests."""

from decision_prism.llm.openrouter import OpenRouterProvider


def test_openrouter_construction():
    provider = OpenRouterProvider(api_key="test_key")
    assert provider._llm.model_name == "qwen/qwen3.6-plus:free"


def test_openrouter_custom_model():
    provider = OpenRouterProvider(
        api_key="test_key",
        model="anthropic/claude-3-opus",
        base_url="https://example.com/v1",
        temperature=0.5,
        max_tokens=2048,
    )
    assert provider._llm.model_name == "anthropic/claude-3-opus"


def test_openrouter_default_headers():
    """Verify HTTP-Referer and X-Title headers are set via default_headers."""
    provider = OpenRouterProvider(api_key="test_key")
    headers = provider._llm.default_headers
    assert headers.get("HTTP-Referer") == "https://github.com/dxc0522/decision_prism"
    assert headers.get("X-Title") == "Decision Prism"
