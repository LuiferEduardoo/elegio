from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.category.models import Category
from app.domains.question.models import Question
from app.domains.test.models import Test


class TestNotFoundError(Exception):
    pass


class CategoryNotFoundError(Exception):
    pass


async def list_questions_by_test(
    db: AsyncSession, test_id: int, limit: int, offset: int
) -> tuple[list[Question], int]:
    test = await db.get(Test, test_id)
    if test is None or test.deleted_at is not None:
        raise TestNotFoundError(f"Test {test_id} not found")

    filters = (
        Question.deleted_at.is_(None),
        Question.test_id == test_id,
    )

    total = (
        await db.execute(select(func.count(Question.id)).where(*filters))
    ).scalar_one()

    result = await db.execute(
        select(Question)
        .options(selectinload(Question.category))
        .where(*filters)
        .order_by(Question.question_order.asc(), Question.id.asc())
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars().all()), total


async def list_questions_by_category(
    db: AsyncSession, category_id: int, limit: int, offset: int
) -> tuple[list[Question], int]:
    category = await db.get(Category, category_id)
    if category is None or category.deleted_at is not None:
        raise CategoryNotFoundError(f"Category {category_id} not found")

    filters = (
        Question.deleted_at.is_(None),
        Question.category_id == category_id,
    )

    total = (
        await db.execute(select(func.count(Question.id)).where(*filters))
    ).scalar_one()

    result = await db.execute(
        select(Question)
        .options(selectinload(Question.category))
        .where(*filters)
        .order_by(Question.question_order.asc(), Question.id.asc())
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars().all()), total
