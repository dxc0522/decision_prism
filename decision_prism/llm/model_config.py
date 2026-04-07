"""Model configuration for LLM providers."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ModelConfig:
    provider: str = "openrouter"
    base_url: str | None = None
    api_key_env: str = "OPENROUTER_API_KEY"
    model: str = "qwen/qwen3.6-plus:free"
    temperature: float = 0.7
    max_tokens: int = 4096
    top_p: float = 1.0
    extra_params: dict[str, Any] = field(default_factory=dict)
