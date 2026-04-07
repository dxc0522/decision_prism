from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    openrouter_api_key: str = ""
    tavily_api_key: str = ""
    firecrawl_api_key: str = ""

    # LLM defaults
    llm_model: str = "qwen/qwen3.6-plus:free"
    llm_base_url: str = "https://openrouter.ai/api/v1"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 4096

    # Debate config
    debate_max_rounds: int = 3
    debate_expert_count: int = 3
    mc_simulations: int = 10000
    mc_seed: int | None = 42


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
