"""Abstract LLM provider interface."""

from abc import ABC, abstractmethod


class Message(dict):
    """Simple message type."""

    @staticmethod
    def system(content: str) -> dict:
        return {"role": "system", "content": content}

    @staticmethod
    def user(content: str) -> dict:
        return {"role": "user", "content": content}

    @staticmethod
    def assistant(content: str) -> dict:
        return {"role": "assistant", "content": content}


class LLMProvider(ABC):
    @abstractmethod
    async def chat(
        self,
        messages: list[dict],
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> dict:
        """Chat with the LLM. Returns {"content": str}."""
        ...

    @abstractmethod
    async def chat_json(
        self,
        messages: list[dict],
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> dict:
        """Chat with JSON output mode. Returns {"content": str}."""
        ...
