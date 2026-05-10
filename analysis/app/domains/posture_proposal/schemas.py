from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class CoderType(str, Enum):
    LLM = "llm"
    HUMAN = "human"


class QualificationLLM(BaseModel):
    ambiguities: str = Field(
        description="Aspects of the axis the text leaves vague or unaddressed"
    )
    reasoning: str = Field(description="2-3 sentences explaining the placement")
    confidence: Literal["high", "medium", "low"]
    score: float = Field(ge=-1.0, le=1.0)


class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    weight: float


class ProposalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    summary: str | None
    full_text: str | None
    category: CategoryRead


class PostureResult(BaseModel):
    id: int
    axis_value: float
    confidence: ConfidenceLevel
