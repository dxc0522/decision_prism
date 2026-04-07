"""Tests for graph nodes."""

from decision_prism.graph.nodes import (
    analysis_node,
    dispatch_experts_node,
    intent_parsing_node,
    research_node,
)


class TestNodes:
    def test_intent_parsing_node_returns_domains(self, minimal_state):
        result = intent_parsing_node(minimal_state)
        assert "detected_domains" in result
        assert "selected_experts" in result
        assert "debate_roles" in result
        assert len(result["detected_domains"]) > 0
        assert len(result["selected_experts"]) > 0

    def test_dispatch_experts_node_returns_empty_dict(self, minimal_state):
        result = dispatch_experts_node(minimal_state)
        assert result == {}

    def test_research_node_handles_missing_api_key(self, minimal_state):
        """Research node should gracefully handle missing Tavily API key."""
        result = research_node(minimal_state)
        assert "research_materials" in result
        assert isinstance(result["research_materials"], dict)

    def test_analysis_node_empty_report(self, minimal_state):
        """Analysis node should work with empty report."""
        result = analysis_node(minimal_state)
        assert "final_analysis" in result
        assert isinstance(result["final_analysis"], dict)

    def test_analysis_node_with_report_data(self, minimal_state):
        """Analysis node should compute Bayesian calibration from report data."""
        state = dict(minimal_state)  # Copy
        state["report"] = {
            "probability_conclusions": [
                {"claim": "Housing prices will drop", "probability": 60, "confidence": 15},
            ],
            "causal_chains": [{"driver": "rates", "mechanism": "demand", "result": "prices"}],
            "stakeholder_impact": [
                {"stakeholder": "buyers", "impact": "positive", "details": "..."}
            ],
        }
        state["research_materials"] = {
            "macro_finance": ["Interest rates impact housing market"],
        }
        result = analysis_node(state)
        assert "final_analysis" in result
        assert "bayesian" in result["final_analysis"]
        assert "sentiment" in result["final_analysis"]
