from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CandidateInGovernmentPlan(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    presidential_candidate: str
    vice_presidential_candidate: str
    political_group: str
    political_spectrum: str | None
    photo_president: str | None
    photo_vice_president: str | None
    photo_of_political_group: str | None


class GovernmentPlanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    candidate: CandidateInGovernmentPlan
    created_at: datetime


class GovernmentPlanList(BaseModel):
    items: list[GovernmentPlanRead]
    total: int
    limit: int
    offset: int
