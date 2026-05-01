from datetime import datetime

from pydantic import BaseModel, ConfigDict


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


class CandidateList(BaseModel):
    items: list[CandidateRead]
    total: int
    limit: int
    offset: int
