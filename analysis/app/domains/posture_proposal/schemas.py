# app/domains/posture/schemas.py
from typing import Literal
from pydantic import BaseModel, Field


class QualificationLLM(BaseModel):
    ambiguities: str = Field(
        description="Aspects of the axis the text leaves vague or unaddressed"
    )
    reasoning: str = Field(
        description="2-3 sentences explaining the placement"
    )
    confidence: Literal["high", "medium", "low"]
    score: float = Field(ge=-1.0, le=1.0)