"""Final report Pydantic model."""

from pydantic import BaseModel


class StakeholderImpact(BaseModel):
    stakeholder: str
    impact: str  # 正面, 负面, 中性
    details: str


class CausalChain(BaseModel):
    driver: str
    mechanism: str
    result: str


class ProbabilityConclusion(BaseModel):
    claim: str
    probability: float  # 概率值，范围 0-100
    confidence: float  # 置信区间，+/- 范围


class BayesianCalibration(BaseModel):
    mean: float
    std: float
    p5: float
    p50: float
    p95: float


class FinalReport(BaseModel):
    summary: str
    key_findings: list[str]
    probability_conclusions: list[ProbabilityConclusion]
    causal_chains: list[CausalChain]
    stakeholder_impact: list[StakeholderImpact]
    risk_factors: list[str]
    recommended_action: str