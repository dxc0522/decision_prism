"""Nash equilibrium — stakeholder impact analysis.

MVP: structured extraction of winners/losers and Pareto improvement suggestions.
"""

from pydantic import BaseModel


class StakeholderImpact(BaseModel):
    stakeholder: str
    impact: str  # "positive", "negative", "neutral"
    details: str


class EquilibriumResult(BaseModel):
    impacts: list[StakeholderImpact]
    compensation_strategies: list[str]


def analyze_equilibrium(debate_summary: str) -> EquilibriumResult:
    """Analyze stakeholder impacts and suggest Pareto improvements.

    MVP returns empty — the real analysis comes from the synthesizer.
    TODO: wire through LLM with structured JSON output.
    """
    return EquilibriumResult(impacts=[], compensation_strategies=[])
