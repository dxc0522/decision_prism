"""Main entry point — run_debate bootstrap function."""

import logging

from decision_prism.config import get_settings
from decision_prism.graph.workflow import build_debate_graph
from decision_prism.models.state import DebateState

logger = logging.getLogger(__name__)


def get_initial_state(query: str) -> DebateState:
    """Create initial state for the debate graph."""
    settings = get_settings()
    return DebateState(
        query=query,
        detected_domains=[],
        selected_experts=[],
        debate_roles=[],
        round_1_statements=[],
        round_2_challenges=[],
        round_3_revisions=[],
        risk_assessments=[],
        research_materials={},
        synthesis_summary="",
        report={},
        current_round=0,
        max_rounds=settings.debate_max_rounds,
        errors=[],
        final_analysis={},
    )


def run_debate(query: str) -> dict:
    """Run a full debate and return the final state."""
    graph = build_debate_graph()
    initial_state = get_initial_state(query)

    result = graph.invoke(initial_state)
    return result
