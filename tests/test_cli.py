"""CLI tests."""

from typer.testing import CliRunner

from decision_prism.cli import app

runner = CliRunner()


def test_info_command():
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert "Decision Prism Configuration" in result.stdout
    assert "Model:" in result.stdout


def test_debate_command_missing_query():
    """Debate without query arg should fail with usage info."""

    result = runner.invoke(app, ["debate"])
    assert result.exit_code != 0


def test_debate_command_with_mocked_llm():
    """Debate command with mocked LLM should output results without errors."""
    import json
    from unittest.mock import patch

    class MockLLM:
        async def chat(self, messages, temperature=None, max_tokens=None):
            return {"content": "Mock analysis. Evidence strongly supports the claim."}

        async def chat_json(self, messages, temperature=None, max_tokens=None):
            return {
                "content": json.dumps({
                    "summary": "Mock summary",
                    "key_findings": ["Finding A"],
                    "probability_conclusions": [
                        {
                            "claim": "Mock claim",
                            "probability": 70,
                            "confidence": 15,
                        }
                    ],
                    "causal_chains": [
                        {
                            "driver": "Driver A",
                            "mechanism": "Via mechanism",
                            "result": "Result Z",
                        }
                    ],
                    "stakeholder_impact": [
                        {
                            "stakeholder": "Stakeholder A",
                            "impact": "neutral",
                            "details": "Some impact",
                        }
                    ],
                    "risk_factors": ["Risk factor"],
                    "recommended_action": "Proceed with caution",
                })
            }

    with patch(
        "decision_prism.llm.openrouter.OpenRouterProvider",
        return_value=MockLLM(),
    ):
        result = runner.invoke(
            app, ["debate", "What is the impact of AI on healthcare?"]
        )

    assert result.exit_code == 0
    assert "Expert Panel" in result.stdout
    assert "Decision Report" in result.stdout
    assert "Debate complete!" in result.stdout
