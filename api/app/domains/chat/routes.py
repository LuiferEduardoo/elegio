from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse

from app.core.database import get_db
from app.core.rate_limit import PRIVATE_RATE_LIMIT, limiter
from app.core.security import get_token_payload
from app.domains.chat import service
from app.domains.chat.schemas import (
    ChatCreate,
    ChatList,
    ChatMessageCreate,
    ChatMessageList,
    ChatMessageRead,
    ChatRead,
)

router = APIRouter(prefix="/chats", tags=["chats"])


def _get_visitor_id(token_payload: dict[str, Any]) -> int:
    visitor_id = token_payload.get("visitor_id")
    if not visitor_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token missing visitor_id")
    return visitor_id


@router.post("", response_model=ChatRead, status_code=status.HTTP_201_CREATED)
@limiter.limit(PRIVATE_RATE_LIMIT)
async def create_chat(
    request: Request,
    payload: ChatCreate,
    token_payload: dict[str, Any] = Depends(get_token_payload),
    db: AsyncSession = Depends(get_db),
) -> ChatRead:
    visitor_id = _get_visitor_id(token_payload)
    chat = await service.create_chat(db, visitor_id, payload.title)
    return ChatRead.model_validate(chat)


@router.get("", response_model=ChatList)
@limiter.limit(PRIVATE_RATE_LIMIT)
async def list_chats(
    request: Request,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    token_payload: dict[str, Any] = Depends(get_token_payload),
    db: AsyncSession = Depends(get_db),
) -> ChatList:
    visitor_id = _get_visitor_id(token_payload)
    chats, total = await service.list_chats(db, visitor_id, limit, offset)
    return ChatList(
        items=[ChatRead.model_validate(c) for c in chats],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{chat_id}/messages", response_model=ChatMessageList)
@limiter.limit(PRIVATE_RATE_LIMIT)
async def list_chat_messages(
    request: Request,
    chat_id: int = Path(gt=0),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    token_payload: dict[str, Any] = Depends(get_token_payload),
    db: AsyncSession = Depends(get_db),
) -> ChatMessageList:
    visitor_id = _get_visitor_id(token_payload)
    try:
        messages, total = await service.list_messages(
            db, chat_id, visitor_id, limit, offset
        )
    except service.ChatNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))

    return ChatMessageList(
        items=[ChatMessageRead.model_validate(m) for m in messages],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.post("/{chat_id}/messages")
@limiter.limit(PRIVATE_RATE_LIMIT)
async def send_chat_message(
    request: Request,
    payload: ChatMessageCreate,
    chat_id: int = Path(gt=0),
    token_payload: dict[str, Any] = Depends(get_token_payload),
    db: AsyncSession = Depends(get_db),
) -> EventSourceResponse:
    """Send a message and stream the assistant reply over SSE.

    Event stream: ``sources`` → ``token``* → [``title``] → ``done``
    (or ``error``).
    """
    visitor_id = _get_visitor_id(token_payload)
    try:
        chat = await service.get_chat_for_visitor(db, chat_id, visitor_id)
    except service.ChatNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))
    if not chat.is_active:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Chat is not active")

    return EventSourceResponse(
        service.stream_chat_response(db, chat, payload.content)
    )
