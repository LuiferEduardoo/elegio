from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domains.response_option import service
from app.domains.response_option.schemas import ResponseOptionList, ResponseOptionRead

router = APIRouter(prefix="/response-options", tags=["response-options"])


@router.get("/question/{question_id}", response_model=ResponseOptionList)
async def list_response_options_by_question(
    question_id: int = Path(gt=0),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> ResponseOptionList:
    try:
        options, total = await service.list_response_options_by_question(
            db, question_id, limit, offset
        )
    except service.QuestionNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))

    return ResponseOptionList(
        items=[ResponseOptionRead.model_validate(o) for o in options],
        total=total,
        limit=limit,
        offset=offset,
    )
