"""纳什均衡 — 利益相关者影响分析。

MVP：结构化提取赢家/输家以及帕累托改进建议。
"""

from pydantic import BaseModel


class StakeholderImpact(BaseModel):
    stakeholder: str
    impact: str  # "positive", "negative", "neutral"
    details: str


class EquilibriumResult(BaseModel):
    impacts: list[StakeholderImpact]
    compensation_strategies: list[str]


def analyze_equilibrium(debate_summary: str) -> EquilibriumResult:
    """分析利益相关者影响并提出帕累托改进建议。

    MVP 返回空 — 真实分析来自综合代理。
    待办：通过 LLM 连接并使用结构化 JSON 输出。
    """
    return EquilibriumResult(impacts=[], compensation_strategies=[])
