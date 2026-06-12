from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import PUBLIC_RATE_LIMIT, limiter
from app.domains.auth import service
from app.domains.auth.schemas import AuthTokenRequest, AuthTokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/token",
    response_model=AuthTokenResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit(PUBLIC_RATE_LIMIT)
async def create_token(
    request: Request,
    payload: AuthTokenRequest,
    db: AsyncSession = Depends(get_db),
) -> AuthTokenResponse:
    visitor, token = await service.create_visitor_token(db, payload)
    return AuthTokenResponse(token=token, visitor_id=visitor.id)
