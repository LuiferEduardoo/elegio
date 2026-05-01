from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.question.models import Question
from app.domains.response_option.models import ResponseOption


class QuestionNotFoundError(Exception):
    pass


async def list_response_options_by_question(
    db: AsyncSession, question_id: int, limit: int, offset: int
) -> tuple[list[ResponseOption], int]:
    question = await db.get(Question, question_id)
    if question is None or question.deleted_at is not None:
        raise QuestionNotFoundError(f"Question {question_id} not found")

    filters = (
        ResponseOption.deleted_at.is_(None),
        ResponseOption.question_id == question_id,
    )

    total = (
        await db.execute(select(func.count(ResponseOption.id)).where(*filters))
    ).scalar_one()

    result = await db.execute(
        select(ResponseOption)
        .where(*filters)
        .order_by(ResponseOption.id.asc())
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars().all()), total
