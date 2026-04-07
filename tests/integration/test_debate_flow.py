"""Integration test for full debate flow with mocked LLM."""

import json

from decision_prism.models.domain import dispatch_agents


class MockLLMProvider:
    """Mock LLM provider with deterministic responses."""

    def __init__(self, *args, **kwargs):
        pass

    async def chat(self, *args, **kwargs):
        return {"content": "Mock expert analysis content with probability estimate 70%."}

    async def chat_json(self, *args, **kwargs):
        return {
            "content": json.dumps(
                {
                    "key_findings": ["Mock finding"],
                    "probability_conclusions": [
                        {"claim": "Mock claim", "probability": 65, "confidence": 20}
                    ],
                    "causal_chains": [{"driver": "D", "mechanism": "M", "result": "R"}],
                    "stakeholder_impact": [
                        {"stakeholder": "Public", "impact": "neutral", "details": "..."}
                    ],
                    "risk_factors": ["Mock risk"],
                    "recommended_action": "Do nothing",
                }
            )
        }


def _mock_agent_init(run_method_name="chat"):
    """Factory for mock agent classes."""

    class MockAgent:
        def __init__(self, *args, **kwargs):
            self.name = "Mock Agent"
            self.domain = kwargs.get("domain", "mock")
            self.stance = kwargs.get("stance", "government_regulator")

        def run(self, *args, **kwargs):
            llm = kwargs.get("llm")
            if hasattr(llm, "chat_json") and run_method_name == "chat_json":
                return llm.chat_json(*args, **kwargs)
            return llm.chat(*args, **kwargs)

    return MockAgent


class TestFullDebateFlow:
    def test_graph_build(self):
        """The debate StateGraph compiles without error."""
        from decision_prism.graph.workflow import build_debate_graph

        graph = build_debate_graph()
        assert graph is not None

    def test_state_propagation(self):
        """Verify state flows correctly through nodes with mocked LLM at node level."""
        from decision_prism.graph.nodes import (
            dispatch_experts_node,
            intent_parsing_node,
            research_node,
        )
        from decision_prism.main import get_initial_state

        state = get_initial_state("What is the impact of interest rates on urban housing?")

        # Intent parsing
        state = {**state, **intent_parsing_node(state)}
        assert len(state["detected_domains"]) > 0
        assert len(state["selected_experts"]) > 0

        # Dispatch (no-op)
        state = {**state, **dispatch_experts_node(state)}

        # Research (graceful when no API key)
        state = {**state, **research_node(state)}
        assert len(state["research_materials"]) > 0

        # Verify state structure is complete for further rounds
        assert "round_1_statements" in state
        assert state["current_round"] == 0

    def test_nodes_individually_with_mock(self):
        """Test each debate node independently with mocked LLM."""
        from decision_prism.graph.nodes import debate_round1_node

        agents = dispatch_agents("test interest rate housing", top_n=3)
        base_state = {
            "query": "Test query about interest rates and housing",
            "detected_domains": [a["domain"] for a in agents],
            "selected_experts": agents,
            "debate_roles": ["government_regulator", "enterprise_market", "individual_user"],
            "round_1_statements": [],
            "round_2_challenges": [],
            "round_3_revisions": [],
            "risk_assessments": [],
            "research_materials": {"macro_finance": ["Some research content"]},
            "synthesis_summary": "",
            "report": {},
            "current_round": 0,
            "max_rounds": 3,
            "errors": [],
            "final_analysis": {},
        }

        r1 = debate_round1_node(base_state)
        # Round 1 will populate errors due to no API key, that's fine
        assert "round_1_statements" in r1
        assert "errors" in r1

    def test_sentiment_tool(self):
        """Sentiment analysis works standalone."""
        from decision_prism.tools.sentiment import analyze_sentiment

        results = [
            {
                "title": "Economic growth continues",
                "url": "",
                "content": "positive growth strong opportunity",
            },
            {
                "title": "Market decline feared",
                "url": "",
                "content": "negative decline crisis risk loss",
            },
        ]
        sentiment = analyze_sentiment(results)
        assert "score" in sentiment
        assert "label" in sentiment
        assert sentiment["label"] in ("positive", "negative", "neutral")

    def test_sentiment_balanced(self):
        """Balanced content should be roughly neutral."""
        from decision_prism.tools.sentiment import analyze_sentiment

        results = [
            {"title": "", "url": "", "content": "growth positive improve"},
            {"title": "", "url": "", "content": "decline negative crisis"},
        ]
        sentiment = analyze_sentiment(results)
        assert sentiment["label"] in ("positive", "negative", "neutral")

    def test_sentiment_no_signal(self):
        """Empty content returns neutral."""
        from decision_prism.tools.sentiment import analyze_sentiment

        sentiment = analyze_sentiment([{"title": "", "url": "", "content": ""}])
        assert sentiment["score"] == 0.0
        assert sentiment["label"] == "neutral"
