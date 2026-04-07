"""Causal chain extraction tests."""

from decision_prism.analysis.causal import CausalGraph, CausalLink, extract_causal_chains


def test_extract_causal_chains_returns_empty():
    """MVP returns empty list."""
    chains = extract_causal_chains("any debate text")
    assert chains == []


def test_causal_link_model():
    link = CausalLink(
        driver="Rates rise", mechanism="Higher mortgage costs", result="Housing slows"
    )
    assert link.driver == "Rates rise"
    assert link.mechanism == "Higher mortgage costs"
    assert link.result == "Housing slows"


def test_causal_graph_model():
    links = [
        CausalLink(driver="A", mechanism="B", result="C"),
        CausalLink(driver="X", mechanism="Y", result="Z"),
    ]
    graph = CausalGraph(chains=links)
    assert len(graph.chains) == 2
