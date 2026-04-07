"""Base agent interface with Jinja2 prompt rendering."""

from abc import ABC

from jinja2 import Environment, FileSystemLoader

from decision_prism.llm.provider import LLMProvider


class BaseAgent(ABC):
    name: str = "base"
    prompt_template: str = ""

    def render_prompt(self, template_name: str, **context: str) -> str:
        """Load and render a Jinja2 template from the prompts/ directory."""
        return self._load_template(template_name).render(**context)

    @staticmethod
    def _load_template(name: str):
        env = Environment(loader=FileSystemLoader("prompts"), trim_blocks=True, lstrip_blocks=True)
        return env.get_template(name)

    async def run(
        self,
        messages: list[dict],
        context: dict,
        llm: LLMProvider,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        prompt = self.prompt_template.format(**context)
        response = await llm.chat(
            messages=[{"role": "system", "content": prompt}, *messages],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response["content"]
