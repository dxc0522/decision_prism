"""Debate model tests."""

from decision_prism.models.debate import ChallengeEntry, DebateEntry, RoundResult, RoundType


def test_round_type_enum():
    assert RoundType.STATEMENT == "statement"
    assert RoundType.CROSS_EXAM == "cross_exam"
    assert RoundType.REVISION == "revision"


def test_debate_entry():
    entry = DebateEntry(
        expert_name="Test Expert",
        domain="macro_finance",
        stance="optimistic",
        content="Market will grow.",
    )
    assert entry.expert_name == "Test Expert"
    assert entry.probability_estimates is None
    assert entry.causal_factors is None


def test_debate_entry_with_optional_fields():
    entry = DebateEntry(
        expert_name="Expert",
        domain="tech_ethics",
        stance="cautious",
        content="Concerns about AI.",
        probability_estimates=[0.6, 0.8],
        causal_factors=["regulation", "market pressure"],
    )
    assert len(entry.probability_estimates) == 2
    assert len(entry.causal_factors) == 2


def test_round_result():
    entry = DebateEntry(
        expert_name="E",
        domain="d",
        stance="s",
        content="c",
    )
    result = RoundResult(round_type=RoundType.STATEMENT, entries=[entry])
    assert result.round_type == RoundType.STATEMENT
    assert len(result.entries) == 1


def test_challenge_entry():
    challenge = ChallengeEntry(
        challenger="A",
        target_expert="B",
        challenge="Disagree with your analysis.",
        response="Standing by my position.",
    )
    assert challenge.challenger == "A"
    assert challenge.target_expert == "B"
