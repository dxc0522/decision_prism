"""Causal chain extraction.

MVP: prompt-based extraction validated against a Pydantic model.
"""

from pydantic import BaseModel


class CausalLink(BaseModel):
    driver: str
    mechanism: str
    result: str


class CausalGraph(BaseModel):
    chains: list[CausalLink]


def extract_causal_chains(
    debate_summary: str,
) -> list[CausalLink]:
    """Extract causal chains from debate text.

    MVP returns an empty list — the real extraction will be done
    via the synthesizer LLM and structured output. This function
    validates and wraps the output into Pydantic models.

    TODO: wire this through the LLM with a JSON schema response.
    """
    # For MVP: the synthesizer already produces the causal chains
    # as part of the structured report. This is a validation pass.
    return []
