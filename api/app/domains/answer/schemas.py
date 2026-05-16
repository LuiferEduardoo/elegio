from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domains.test_attempt.models import TestStatus


class CategoryAverage(BaseModel):
    category_id: int
    category_name: str
    weight: float
    average: float = Field(
        description="Mean of response_option.value for answers in this category"
    )


class CandidateAffinity(BaseModel):
    candidate_id: int
    presidential_candidate: str
    vice_presidential_candidate: str
    political_group: str
    political_spectrum: str | None = None
    photo_president: str | None = None
    photo_vice_president: str | None = None
    photo_of_political_group: str | None = None
    affinity: float = Field(
        ge=0.0, le=1.0, description="Normalized similarity (1 = identical, 0 = opposite)"
    )
    distance: float = Field(ge=0.0, description="Weighted Manhattan distance")
    categories_compared: int = Field(
        ge=0, description="Categories that were both answered and have postures"
    )


class AffinityResponse(BaseModel):
    test_attempt_uuid: str
    user_averages: list[CategoryAverage]
    candidates: list[CandidateAffinity]


class AnswerCreate(BaseModel):
    question_id: int = Field(gt=0)
    response_option_id: int | None = Field(default=None, gt=0)
    boolean_answer: bool | None = None
    open_text_answer: str | None = None
    response_time: int | None = Field(default=None, ge=0)


class AnswerCreateWithAttempt(AnswerCreate):
    test_attempt_uuid: str | None = None


class AnswerUpdate(BaseModel):
    response_option_id: int | None = Field(default=None, gt=0)
    boolean_answer: bool | None = None
    open_text_answer: str | None = None
    response_time: int | None = Field(default=None, ge=0)


class AnswerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    test_attempt_id: int
    question_id: int
    response_option_id: int | None
    boolean_answer: bool | None
    open_text_answer: str | None
    response_time: int | None
    created_at: datetime


class AnswerCreateResponse(BaseModel):
    answer: AnswerRead
    test_completed: bool
    test_attempt_status: TestStatus


class AnswerList(BaseModel):
    items: list[AnswerRead]
    total: int
    limit: int
    offset: int
