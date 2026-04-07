"""Agent base and run tests."""

import asyncio

from decision_prism.agents.base import BaseAgent


class MockLLM:
    async def chat(self, messages, temperature=None, max_tokens=None):
        return {"content": "Hello from LLM"}


def test_base_agent_run():
    class TestAgent(BaseAgent):
        def _build_system_prompt(self, context):
            return "You are a test agent."

    agent = TestAgent()
    result = asyncio.get_event_loop().run_until_complete(
        agent.run(
            messages=[{"role": "user", "content": "test"}],
            context={"query": "test"},
            llm=MockLLM(),
        )
    )
    assert result == "Hello from LLM"


def test_base_agent_format_messages():
    """Verify messages are passed through correctly."""

    class TestAgent(BaseAgent):
        def _build_system_prompt(self, context):
            return "test"

    agent = TestAgent()

    captured = {}

    class CaptureLLM:
        async def chat(self, messages, temperature=None, max_tokens=None):
            captured["messages"] = messages
            return {"content": "ok"}

    asyncio.get_event_loop().run_until_complete(
        agent.run(
            messages=[{"role": "user", "content": "hello"}],
            context={},
            llm=CaptureLLM(),
        )
    )
    assert captured["messages"][0]["role"] == "system"
    assert captured["messages"][-1]["content"] == "hello"


def test_base_agent_prompt_template():
    """Verify BaseAgent has prompt_template attribute."""
    assert hasattr(BaseAgent, "prompt_template")
    assert BaseAgent.prompt_template == ""


def test_base_agent_render_prompt():
    """Verify BaseAgent has render_prompt method."""
    assert callable(BaseAgent.render_prompt)
