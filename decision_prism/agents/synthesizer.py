"""Synthesizer Agent — produces structured report from debate rounds."""

from decision_prism.agents.base import BaseAgent
from decision_prism.llm.provider import LLMProvider


class SynthesizerAgent(BaseAgent):
    name = "synthesizer"

    async def run(
        self,
        messages: list[dict],
        context: dict,
        llm: LLMProvider,
    ) -> str:
        prompt = """\
You are a neutral synthesizer integrating a 3-round expert debate into a \
structured decision report.

Query: {query}

=== ROUND 1 — Initial Statements ===
{round_1}

=== ROUND 2 — Cross-Examination Challenges ===
{round_2}

=== ROUND 3 — Risk-Adjusted Revisions ===
{round_3}

=== RISK ASSESSMENT ===
{risk_assessment}

Synthesize the above into a structured report with:
1. Key Findings (consensus and dissent)
2. Probability-Weighted Conclusions
3. Causal Chain (driver → mechanism → result)
4. Stakeholder Impact (winners and losers)
5. Risk Factors
6. Recommended Action

Output as valid JSON following this schema:
{{
  "key_findings": ["...", "..."],
  "probability_conclusions": [{{
      "claim": "...", "probability": 0.0, "confidence": 0.0
  }}],
  "causal_chains": [{{"driver": "...", "mechanism": "...", "result": "..."}}],
  "stakeholder_impact": [{{
      "stakeholder": "...", "impact": "+/-/0", "details": "..."
  }}],
  "risk_factors": ["...", "..."],
  "recommended_action": "..."
}}
""".format(
            query=context.get("query", ""),
            round_1=context.get("round_1", ""),
            round_2=context.get("round_2", ""),
            round_3=context.get("round_3", ""),
            risk_assessment=context.get("risk_assessment", ""),
        )

        response = await llm.chat_json(
            messages=[{"role": "system", "content": prompt}, *messages],
        )
        return response["content"]
