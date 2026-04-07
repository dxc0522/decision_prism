"""Data models for debate workflow."""

from enum import StrEnum

from pydantic import BaseModel


class RoundType(StrEnum):
    STATEMENT = "statement"
    CROSS_EXAM = "cross_exam"
    REVISION = "revision"


class DebateEntry(BaseModel):
    expert_name: str
    domain: str
    stance: str
    content: str
    probability_estimates: list[float] | None = None
    causal_factors: list[str] | None = None


class RoundResult(BaseModel):
    round_type: RoundType
    entries: list[DebateEntry]


class ChallengeEntry(BaseModel):
    challenger: str
    target_expert: str
    challenge: str
    response: str
