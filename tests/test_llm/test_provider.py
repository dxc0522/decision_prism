"""LLM provider tests."""

from decision_prism.llm.provider import LLMProvider, Message


def test_message_system():
    msg = Message.system("You are an expert")
    assert msg["role"] == "system"
    assert msg["content"] == "You are an expert"


def test_message_user():
    msg = Message.user("What is 2+2?")
    assert msg["role"] == "user"
    assert msg["content"] == "What is 2+2?"


def test_message_assistant():
    msg = Message.assistant("The answer is 4")
    assert msg["role"] == "assistant"
    assert msg["content"] == "The answer is 4"


def test_llm_provider_is_abstract():
    """Cannot instantiate LLMProvider directly."""
    try:
        LLMProvider()
        assert False, "Should have raised TypeError"
    except TypeError:
        pass


def test_concrete_provider_implementation():
    """Verify OpenRouterProvider implements LLMProvider."""
    from decision_prism.llm.openrouter import OpenRouterProvider

    provider = OpenRouterProvider(api_key="test")
    assert isinstance(provider, LLMProvider)
