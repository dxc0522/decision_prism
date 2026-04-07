"""OpenRouter provider wrapping langchain-openai ChatOpenAI."""

from langchain_openai import ChatOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from decision_prism.llm.provider import LLMProvider


class OpenRouterProvider(LLMProvider):
    def __init__(
        self,
        api_key: str,
        model: str = "qwen/qwen3.6-plus:free",
        base_url: str = "https://openrouter.ai/api/v1",
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ):
        self._llm = ChatOpenAI(
            model=model,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature,
            max_tokens=max_tokens,
            extra_headers={
                "HTTP-Referer": "https://github.com/dxc0522/decision_prism",
                "X-Title": "Decision Prism",
            },
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def chat(
        self,
        messages: list[dict],
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> dict:
        """Chat with the model. Returns {"content": str}."""
        lc_messages = messages  # Already in OpenAI format
        response = await self._llm.ainvoke(lc_messages)
        return {"content": response.content}

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def chat_json(
        self,
        messages: list[dict],
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> dict:
        """Chat with JSON-friendly output."""
        llm_with_json = self._llm.bind(response_format={"type": "json_object"})
        response = await llm_with_json.ainvoke(messages)
        return {"content": response.content}
