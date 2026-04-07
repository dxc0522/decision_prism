"""SME Expert Agent — domain expert that adopts a stance in debate."""

from decision_prism.agents.base import BaseAgent
from decision_prism.llm.provider import LLMProvider


class SMEExpertAgent(BaseAgent):
    def __init__(self, domain: str, stance: str):
        self.domain = domain
        self.stance = stance
        self.name = f"{domain.replace('_', ' ').title()} Expert ({stance})"

    async def run(
        self,
        messages: list[dict],
        context: dict,
        llm: LLMProvider,
    ) -> str:
        """Run expert analysis with role-adopted system prompt."""
        prompt = """\
You are a {domain} expert with deep domain knowledge. You are participating in \
a structured debate from the perspective of a {stance}.

Your role and priorities as a {stance}:
- Focus on arguments, evidence, and reasoning relevant to that standpoint.
- Provide probability estimates (0-100%) for your key claims.
- Identify the primary causal factors driving your conclusions.
- Support your positions with evidence from the provided research materials.

Query: {query}
""".format(domain=self.domain, stance=self.stance, query=context.get("query", ""))

        research_summary = context.get("research_summary", "")
        if research_summary:
            prompt += f"\n\nResearch materials:\n{research_summary}\n"

        response = await llm.chat(
            messages=[{"role": "system", "content": prompt}, *messages],
        )
        return response["content"]
