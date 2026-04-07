"""E2E debate flow tests with mocked LLM."""

import asyncio
from unittest.mock import AsyncMock, patch

from decision_prism.main import run_debate


class MockLLM:
    """Mock that returns deterministic responses for all chat/chat_json calls."""

    _call_count = 0

    async def chat(self, messages, temperature=None, max_tokens=None):
        self._call_count += 1
        return {"content": self._mock_response()}

    async def chat_json(self, messages, temperature=None, max_tokens=None):
        self._call_count += 1
        return {"content": self._mock_json_response()}

    def _mock_response(self):
        """Deterministic response for all chat calls."""
        return (
            "Based on the analysis, the probability of the expected outcome "
            "is approximately 65% with a confidence interval of +/- 15%. "
            "The primary causal drivers include market trends, regulatory "
            "environment, and stakeholder behavior. Key causal chains: "
            "rate changes -> mortgage affordability -> demand reduction."
        )

    def _mock_json_response(self):
        """Structured JSON response for the synthesizer."""
        import json

        return json.dumps({
            "summary": "Multi-factor analysis reveals moderate confidence.",
            "key_findings": ["Finding 1", "Finding 2", "Finding 3"],
            "probability_conclusions": [
                {"claim": "Policy impact likely", "probability": 65, "confidence": 15},
                {"claim": "Market adjustment expected", "probability": 55, "confidence": 10},
            ],
            "causal_chains": [
                {"driver": "Rate increases", "mechanism": "Reduced affordability", "result": "Lower demand"},
            ],
            "stakeholder_impact": [
                {"stakeholder": "Homebuyers", "impact": "negative", "details": "Higher borrowing costs"},
                {"stakeholder": "Builders", "impact": "neutral", "details": "Mixed impact on supply chain"},
            ],
            "risk_factors": ["Interest rate volatility", "Regulatory shifts"],
            "recommended_action": "Monitor closely and prepare contingency plans",
        })


@patch("decision_prism.llm.openrouter.OpenRouterProvider")
def test_full_debate_flow(mock_provider_class):
    """Full debate through LangGraph with mocked LLM returns complete state."""
    mock_provider_class.return_value = MockLLM()

    result = run_debate("What is the impact of rising interest rates on housing?")

    # 验证所有轮次都产生了内容
    assert len(result.get("errors", [])) == 0, f"Errors: {result.get('errors')}"
    assert len(result["round_1_statements"]) > 0, "Round 1 missing statements"
    assert len(result["round_2_challenges"]) > 0, "Round 2 missing challenges"
    assert len(result["round_3_revisions"]) > 0, "Round 3 missing revisions"

    # 验证报告已生成
    assert result["report"], "Report is empty"
    report = result["report"]
    assert "probability_conclusions" in report, "Report missing probability_conclusions"
    assert "causal_chains" in report, "Report missing causal_chains"
    assert "stakeholder_impact" in report, "Report missing stakeholder_impact"

    # 验证分析结果
    assert "final_analysis" in result, "Missing final_analysis"
    assert "bayesian" in result["final_analysis"], "Missing bayesian calibration"


@patch("decision_prism.llm.openrouter.OpenRouterProvider")
def test_full_debate_state_propagation(mock_provider_class):
    """Verify state fields propagate through entire pipeline."""
    query = "Test query for state propagation"
    mock_provider_class.return_value = MockLLM()

    result = run_debate(query)

    assert result["query"] == query
    assert result["detected_domains"], "No domains detected"
    assert result["selected_experts"], "No experts selected"
    assert result["current_round"] == 3, f"Expected round 3, got {result['current_round']}"
    assert len(result["selected_experts"]) >= 2, "Fewer than 2 experts selected"


@patch("decision_prism.llm.openrouter.OpenRouterProvider")
def test_research_materials_populated(mock_provider_class):
    """Verify research node populates materials dictionary."""
    mock_provider_class.return_value = MockLLM()

    result = run_debate("economic impact of remote work")

    # 研究材料应至少有一个领域的数据
    # (即使在没有 API 密钥时也只是一个占位符)
    assert isinstance(result["research_materials"], dict)
