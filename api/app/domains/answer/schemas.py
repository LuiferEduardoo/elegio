from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domains.test_attempt.models import TestStatus


class AnswerCreate(BaseModel):
    question_id: int = Field(gt=0)
    response_option_id: int | None = Field(default=None, gt=0)
    boolean_answer: bool | None = None
    open_text_answer: str | None = None
    response_time: int | None = Field(default=None, ge=0)


class AnswerCreateWithAttempt(AnswerCreate):
    test_attempt_uuid: str


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
