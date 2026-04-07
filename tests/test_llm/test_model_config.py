"""Model config tests."""

from decision_prism.llm.model_config import ModelConfig


def test_model_config_defaults():
    config = ModelConfig()
    assert "qwen" in config.model.lower() or config.model
    assert config.temperature == 0.7
    assert config.max_tokens == 4096


def test_model_config_custom():
    config = ModelConfig(model="gpt-4", temperature=0.5, max_tokens=2048)
    assert config.model == "gpt-4"
    assert config.temperature == 0.5
    assert config.max_tokens == 2048
