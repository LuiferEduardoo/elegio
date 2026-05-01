from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.question import service
from app.domains.question.schemas import QuestionList, QuestionRead

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/by-test/{test_id}", response_model=QuestionList)
async def list_questions_by_test(
    test_id: int = Path(gt=0),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> QuestionList:
    try:
        questions, total = await service.list_questions_by_test(
            db, test_id, limit, offset
        )
    except service.TestNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))

    return QuestionList(
        items=[QuestionRead.model_validate(q) for q in questions],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/by-category/{category_id}", response_model=QuestionList)
async def list_questions_by_category(
    category_id: int = Path(gt=0),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> QuestionList:
    try:
        questions, total = await service.list_questions_by_category(
            db, category_id, limit, offset
        )
    except service.CategoryNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))

    return QuestionList(
        items=[QuestionRead.model_validate(q) for q in questions],
        total=total,
        limit=limit,
        offset=offset,
    )
