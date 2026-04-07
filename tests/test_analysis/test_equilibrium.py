"""Nash equilibrium analysis tests."""

from decision_prism.analysis.equilibrium import (
    EquilibriumResult,
    StakeholderImpact,
    analyze_equilibrium,
)


def test_analyze_equilibrium_returns_empty():
    """MVP returns empty result."""
    result = analyze_equilibrium("any summary")
    assert isinstance(result, EquilibriumResult)
    assert result.impacts == []
    assert result.compensation_strategies == []


def test_stakeholder_impact_model():
    impact = StakeholderImpact(
        stakeholder="Homebuyers",
        impact="negative",
        details="Higher rates reduce affordability",
    )
    assert impact.stakeholder == "Homebuyers"
    assert impact.impact == "negative"


def test_equilibrium_result_model():
    result = EquilibriumResult(
        impacts=[StakeholderImpact(stakeholder="A", impact="positive", details="Good")],
        compensation_strategies=["subsidy"],
    )
    assert len(result.impacts) == 1
    assert len(result.compensation_strategies) == 1
