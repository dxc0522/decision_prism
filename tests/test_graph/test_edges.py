"""Graph edge routing tests."""

from decision_prism.graph.edges import (
    route_after_dispatch,
    route_after_intent,
    route_after_research,
    route_after_round1,
    route_after_round2,
    route_after_round3,
    route_after_synthesis,
)


def _dummy_state():
    return {
        "query": "test",
        "detected_domains": [],
        "selected_experts": [],
        "debate_roles": [],
        "round_1_statements": [],
        "round_2_challenges": [],
        "round_3_revisions": [],
        "risk_assessments": [],
        "research_materials": {},
        "synthesis_summary": "",
        "report": {},
        "current_round": 0,
        "max_rounds": 3,
        "errors": [],
        "final_analysis": {},
    }


def test_route_after_intent():
    assert route_after_intent(_dummy_state()) == "dispatch_experts"


def test_route_after_dispatch():
    assert route_after_dispatch(_dummy_state()) == "research"


def test_route_after_research():
    assert route_after_research(_dummy_state()) == "debate_round1"


def test_route_after_round1():
    assert route_after_round1(_dummy_state()) == "debate_round2"


def test_route_after_round2():
    assert route_after_round2(_dummy_state()) == "debate_round3"


def test_route_after_round3():
    assert route_after_round3(_dummy_state()) == "synthesize_report"


def test_route_after_synthesis():
    assert route_after_synthesis(_dummy_state()) == "analysis"
