"""LangGraph state schema for debate workflow."""

import operator
from typing import Annotated, Any, TypedDict


class DebateState(TypedDict):
    query: str
    detected_domains: list[str]
    selected_experts: list[dict]
    debate_roles: list[str]
    round_1_statements: list[dict]
    round_2_challenges: list[dict]
    round_3_revisions: list[dict]
    risk_assessments: list[str]
    research_materials: dict[str, list[str]]
    synthesis_summary: str
    report: dict[str, Any]
    current_round: int
    max_rounds: int
    errors: Annotated[list[str], operator.add]
    final_analysis: dict[str, Any]
