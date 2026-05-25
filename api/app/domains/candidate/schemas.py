from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CategoryAverage(BaseModel):
    category_id: int
    category_name: str
    weight: float
    negative_pole_name: str
    negative_pole_description: str
    positive_pole_name: str
    positive_pole_description: str
    average: float = Field(
        description="Mean of posture.axis_value across the candidate's proposals in this category"
    )
    adjusted_average: float = Field(
        description=(
            "Average after applying the candidate's rhetorical weight for this category: "
            "sign(avg) * |avg|^(1/weight). Defaults to `average` when no weight is set."
        )
    )
    rhetorical_weight: float | None = Field(
        default=None,
        description="Rhetorical weight (0.0-5.0) used to compute adjusted_average; null if not set",
    )
    editorial_justification: str | None = Field(
        default=None,
        description="Editorial rationale for the rhetorical weight, if any",
    )
    proposals_count: int = Field(
        ge=0, description="Number of rated proposals contributing to the average"
    )


class CandidateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    presidential_candidate: str
    vice_presidential_candidate: str
    political_group: str
    photo_of_political_group: str | None
    photo_president: str | None
    photo_vice_president: str | None
    troubles_questions: str | None
    political_spectrum: str | None
    created_at: datetime
    category_averages: list[CategoryAverage] = []


class CandidateList(BaseModel):
    items: list[CandidateRead]
    total: int
    limit: int
    offset: int
