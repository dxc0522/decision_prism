"""Shared test fixtures."""

import pytest

from decision_prism.models.domain import dispatch_agents
from decision_prism.models.state import DebateState


@pytest.fixture
def sample_query():
    return "What is the impact of rising interest rates on urban housing development?"


@pytest.fixture
def sample_experts(sample_query):
    return dispatch_agents(sample_query, top_n=3)


@pytest.fixture
def mock_llm_response():
    return {
        "content": "Mock expert analysis. "
        "Strong evidence supports the conclusion. "
        "Probability: 75%."
    }


@pytest.fixture
def mock_llm():
    """Simple mock LLM provider that returns deterministic strings."""

    class MockLLM:
        async def chat(self, messages, temperature=None, max_tokens=None):
            return {"content": "Mock analysis. Probability: 70%."}

        async def chat_json(self, messages, temperature=None, max_tokens=None):
            json_str = (
                '{"key_findings":["mock"],'
                '"probability_conclusions":[{"claim":"mock",'
                '"probability":0.7,"confidence":0.3}],'
                '"causal_chains":[],"stakeholder_impact":[],'
                '"risk_factors":["risk"],"recommended_action":"act"}'
            )
            return {"content": json_str}

    return MockLLM()


@pytest.fixture
def minimal_state(sample_query):
    """Minimal DebateState for testing individual nodes."""
    agents = dispatch_agents(sample_query)
    return DebateState(
        query=sample_query,
        detected_domains=[a["domain"] for a in agents],
        selected_experts=agents,
        debate_roles=["government_regulator", "enterprise_market", "individual_user"],
        round_1_statements=[],
        round_2_challenges=[],
        round_3_revisions=[],
        risk_assessments=[],
        research_materials={},
        synthesis_summary="",
        report={},
        current_round=0,
        max_rounds=3,
        errors=[],
        final_analysis={},
    )
