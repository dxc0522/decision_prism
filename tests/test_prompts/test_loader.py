"""Prompt loader tests."""

from decision_prism.prompts import get_env, render_prompt


def test_get_env_returns_environment():
    env = get_env()
    assert env is not None


def test_render_debate_round1():
    result = render_prompt(
        "debate_round1.md",
        query="What is the impact of AI?",
        domain="tech_ethics",
        stance="cautious",
    )
    assert "AI" in result
    assert "tech_ethics" in result


def test_render_debate_round2():
    result = render_prompt(
        "debate_round2.md",
        expert_name="Dr. Smith",
        domain="macro_finance",
        stance="cautious",
        other_expert="Prof. Jones",
        their_statement="Prices will rise.",
    )
    assert "macro_finance" in result
    assert "Prof. Jones" in result


def test_render_debate_round3():
    result = render_prompt(
        "debate_round3.md",
        expert_name="Risk Analyst",
        risk_items="Flood risk is elevated.",
    )
    assert "Flood risk is elevated" in result
