"""Edge routing functions for the debate graph.

MVP uses linear routing (always proceed to next round).
These functions are stubbed for future conditional routing
(e.g., early exit on consensus, quality gates).
"""

from decision_prism.models.state import DebateState


def route_after_intent(state: DebateState) -> str:
    """Always proceed to dispatch."""
    return "dispatch_experts"


def route_after_dispatch(state: DebateState) -> str:
    """Always proceed to research."""
    return "research"


def route_after_research(state: DebateState) -> str:
    """Always proceed to Round 1."""
    return "debate_round1"


def route_after_round1(state: DebateState) -> str:
    """Always proceed to Round 2.
    Future: Check consensus — early exit if agreement threshold met.
    """
    return "debate_round2"


def route_after_round2(state: DebateState) -> str:
    """Always proceed to Round 3.
    Future: Quality gate — if statements lack sufficient depth, repeat.
    """
    return "debate_round3"


def route_after_round3(state: DebateState) -> str:
    """Always proceed to synthesis."""
    return "synthesize_report"


def route_after_synthesis(state: DebateState) -> str:
    """Always proceed to analysis."""
    return "analysis"
