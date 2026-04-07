"""Tests for base agents."""

import pytest

from decision_prism.agents.expert import SMEExpertAgent
from decision_prism.agents.risk import RiskAgent
from decision_prism.agents.synthesizer import SynthesizerAgent


class TestAgentConstruction:
    def test_expert_agent_creation(self):
        agent = SMEExpertAgent(domain="macro_finance", stance="government_regulator")
        assert "Macro Finance" in agent.name
        assert agent.domain == "macro_finance"
        assert agent.stance == "government_regulator"

    def test_risk_agent_creation(self):
        agent = RiskAgent()
        assert agent.name == "risk_analyst"

    def test_synthesizer_agent_creation(self):
        agent = SynthesizerAgent()
        assert agent.name == "synthesizer"


class TestExpertRunWithMock:
    @pytest.mark.asyncio
    async def test_expert_run_returns_content(self, mock_llm):
        agent = SMEExpertAgent(domain="urban_planning", stance="government_regulator")
        result = await agent.run(
            messages=[{"role": "user", "content": "test query"}],
            context={"query": "test query", "research_summary": "mock research"},
            llm=mock_llm,
        )
        assert isinstance(result, str)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_risk_agent_run_returns_content(self, mock_llm):
        agent = RiskAgent()
        result = await agent.run(
            messages=[{"role": "user", "content": "test query"}],
            context={"query": "test query", "debate_summary": "mock summary"},
            llm=mock_llm,
        )
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_synthesizer_returns_json_string(self, mock_llm):
        agent = SynthesizerAgent()
        result = await agent.run(
            messages=[{"role": "user", "content": "test query"}],
            context={
                "query": "test query",
                "round_1": "round 1",
                "round_2": "round 2",
                "round_3": "round 3",
                "risk_assessment": "risk",
            },
            llm=mock_llm,
        )
        assert isinstance(result, str)
