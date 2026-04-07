"""Risk Agent — identifies black-swan and high-impact scenarios."""

from decision_prism.agents.base import BaseAgent
from decision_prism.llm.provider import LLMProvider


class RiskAgent(BaseAgent):
    name = "risk_analyst"

    async def run(
        self,
        messages: list[dict],
        context: dict,
        llm: LLMProvider,
    ) -> str:
        prompt = """\
You are a black-swan risk analyst specializing in strategic decision evaluation. \
Your task is to identify low-probability, high-impact scenarios that could invalidate \
the current consensus conclusions.

Query: {query}

Previous debate conclusions:
{debate_summary}

Analyze for:
1. Black-swan events that could derail the consensus
2. Hidden dependencies or cascading failure modes
3. Tail risks that are being underestimated
4. Second/third-order effects the experts missed

Provide your probability estimates and reasoning.
""".format(
            query=context.get("query", ""),
            debate_summary=context.get("debate_summary", ""),
        )

        response = await llm.chat(
            messages=[{"role": "system", "content": prompt}, *messages],
        )
        return response["content"]
