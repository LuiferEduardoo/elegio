from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.domains.question.models import QuestionType


class CategoryInQuestion(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    weight: float


class QuestionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    test_id: int
    candidate_id: int | None
    title: str
    description: str | None
    type_question: QuestionType
    video_url: str | None
    question_order: int
    is_active: bool
    category: CategoryInQuestion | None
    created_at: datetime


class QuestionList(BaseModel):
    items: list[QuestionRead]
    total: int
    limit: int
    offset: int
