"""因果链提取。

MVP：基于提示词的提取，并通过 Pydantic 模型验证。
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
    """从辩论文本中提取因果链。

    MVP 返回空列表 — 实际提取将通过综合代理 LLM 和结构化输出完成。
    此函数验证并将输出包装为 Pydantic 模型。

    待办：通过 LLM 连接并使用 JSON 模式响应。
    """
    # 对于 MVP：综合代理已产生因果链
    # 作为结构化报告的一部分。这是一个验证通道。
    return []
