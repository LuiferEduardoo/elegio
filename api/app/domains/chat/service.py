"""Elegio chatbot service: RAG over Qdrant + Gemini via LangChain, with
summarizing conversational memory and an SSE streaming response.

Memory model: the prompt always carries ``chat.summary`` (a rolling summary of
old messages) plus the messages newer than ``chat.last_summarized_message_id``
verbatim. Before each turn, if the verbatim history exceeds
``HISTORY_TOKEN_BUDGET`` (approximated at ``APPROX_CHARS_PER_TOKEN``), the
oldest messages — all but the last ``KEEP_RECENT_MESSAGES`` — are folded into
the summary with one LLM call. The budget is deliberately far below the model
context window (~1M tokens for gemini-2.5-flash): it bounds latency and cost
per turn, not just correctness.
"""

import json
import logging
import time
from collections.abc import AsyncIterator

from langchain_core.messages import (
    AIMessage,
    AIMessageChunk,
    BaseMessage,
    HumanMessage,
)
from langchain_google_genai import ChatGoogleGenerativeAI
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.domains.chat.models import Chat, ChatMessage, ChatMessageRole
from app.domains.chat.prompts import CHAT_PROMPT, SUMMARY_PROMPT, TITLE_PROMPT
from app.domains.chat.retriever import COLLECTION_LABELS, ElegioRetriever
from app.domains.chat.schemas import ChatMessageRead

logger = logging.getLogger(__name__)

DEFAULT_CHAT_TITLE = "Nueva conversación"

HISTORY_TOKEN_BUDGET = 8_000
KEEP_RECENT_MESSAGES = 8
APPROX_CHARS_PER_TOKEN = 4


class ChatNotFoundError(Exception):
    pass


class ChatNotActiveError(Exception):
    pass


_llm: ChatGoogleGenerativeAI | None = None


def _get_chat_llm() -> ChatGoogleGenerativeAI:
    global _llm
    if _llm is None:
        settings = get_settings()
        _llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_CHAT_MODEL,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.3,
        )
    return _llm


async def create_chat(
    db: AsyncSession, visitor_id: int, title: str | None
) -> Chat:
    chat = Chat(visitor_id=visitor_id)
    if title:
        chat.title = title
    db.add(chat)
    await db.commit()
    await db.refresh(chat)
    return chat


async def list_chats(
    db: AsyncSession, visitor_id: int, limit: int, offset: int
) -> tuple[list[Chat], int]:
    filters = (
        Chat.visitor_id == visitor_id,
        Chat.is_active.is_(True),
        Chat.deleted_at.is_(None),
    )
    total = (
        await db.execute(select(func.count(Chat.id)).where(*filters))
    ).scalar_one()
    result = await db.execute(
        select(Chat)
        .where(*filters)
        .order_by(Chat.created_at.desc(), Chat.id.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars().all()), total


async def get_chat_for_visitor(
    db: AsyncSession, chat_id: int, visitor_id: int
) -> Chat:
    chat = await db.get(Chat, chat_id)
    if chat is None or chat.deleted_at is not None or chat.visitor_id != visitor_id:
        raise ChatNotFoundError(f"Chat {chat_id} not found")
    return chat


async def list_messages(
    db: AsyncSession, chat_id: int, visitor_id: int, limit: int, offset: int
) -> tuple[list[ChatMessage], int]:
    await get_chat_for_visitor(db, chat_id, visitor_id)
    filters = (
        ChatMessage.chat_id == chat_id,
        ChatMessage.deleted_at.is_(None),
    )
    total = (
        await db.execute(select(func.count(ChatMessage.id)).where(*filters))
    ).scalar_one()
    result = await db.execute(
        select(ChatMessage)
        .where(*filters)
        .order_by(ChatMessage.id.asc())
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars().all()), total


async def _load_recent_history(
    db: AsyncSession, chat: Chat, exclude_message_id: int
) -> list[ChatMessage]:
    """Messages newer than the summarized range, oldest first."""
    result = await db.execute(
        select(ChatMessage)
        .where(
            ChatMessage.chat_id == chat.id,
            ChatMessage.deleted_at.is_(None),
            ChatMessage.id > (chat.last_summarized_message_id or 0),
            ChatMessage.id != exclude_message_id,
        )
        .order_by(ChatMessage.id.asc())
    )
    return list(result.scalars().all())


def _approx_tokens(chat: Chat, history: list[ChatMessage]) -> int:
    chars = len(chat.summary or "") + sum(len(m.content) for m in history)
    return chars // APPROX_CHARS_PER_TOKEN


def _transcript(messages: list[ChatMessage]) -> str:
    return "\n".join(
        f"{'Usuario' if m.role == ChatMessageRole.USER else 'Asistente'}: {m.content}"
        for m in messages
    )


async def _maybe_summarize(
    db: AsyncSession, chat: Chat, history: list[ChatMessage]
) -> list[ChatMessage]:
    """Fold old messages into ``chat.summary`` when over budget.

    Returns the (possibly trimmed) history to send verbatim.
    """
    if (
        len(history) <= KEEP_RECENT_MESSAGES
        or _approx_tokens(chat, history) <= HISTORY_TOKEN_BUDGET
    ):
        return history

    to_fold = history[:-KEEP_RECENT_MESSAGES]
    kept = history[-KEEP_RECENT_MESSAGES:]

    response = await _get_chat_llm().ainvoke(
        SUMMARY_PROMPT.format_messages(
            previous_summary=chat.summary or "",
            messages=_transcript(to_fold),
        )
    )
    chat.summary = response.text.strip()
    chat.last_summarized_message_id = to_fold[-1].id
    await db.commit()
    return kept


def _to_langchain_messages(history: list[ChatMessage]) -> list[BaseMessage]:
    return [
        HumanMessage(m.content)
        if m.role == ChatMessageRole.USER
        else AIMessage(m.content)
        for m in history
    ]


def _format_context(docs) -> str:
    if not docs:
        return "(no se encontró información relevante)"
    blocks = []
    for i, doc in enumerate(docs, 1):
        meta = doc.metadata
        label = COLLECTION_LABELS.get(meta.get("collection"), "Fuente")
        attribution = [label]
        if meta.get("candidate_name"):
            attribution.append(f"candidato: {meta['candidate_name']}")
        if meta.get("title"):
            attribution.append(meta["title"])
        if meta.get("media_outlet"):
            attribution.append(meta["media_outlet"])
        if meta.get("publishing_house"):
            attribution.append(meta["publishing_house"])
        url = meta.get("url") or meta.get("url_video_audio")
        if url:
            attribution.append(f"URL: {url}")
        blocks.append(f"[{i}] ({' — '.join(attribution)})\n{doc.page_content}")
    return "\n\n".join(blocks)


def _sources_payload(docs) -> list[dict]:
    sources = []
    for i, doc in enumerate(docs, 1):
        meta = doc.metadata
        sources.append(
            {
                "ref": i,
                "collection": meta.get("collection"),
                "score": meta.get("score"),
                "candidate_id": meta.get("candidate_id"),
                "candidate_name": meta.get("candidate_name"),
                "title": meta.get("title"),
                "url": meta.get("url") or meta.get("url_video_audio"),
            }
        )
    return sources


async def _generate_title(question: str, answer: str) -> str | None:
    try:
        response = await _get_chat_llm().ainvoke(
            TITLE_PROMPT.format_messages(question=question, answer=answer)
        )
    except Exception:
        logger.warning("Chat title generation failed", exc_info=True)
        return None
    title = response.text.strip().strip('"')
    return title[:150] or None


async def stream_chat_response(
    db: AsyncSession, chat: Chat, content: str
) -> AsyncIterator[dict]:
    """Run one chat turn and yield SSE events.

    Events: ``sources`` (retrieved refs), ``token`` (answer deltas), ``title``
    (only when the chat gets named), ``done`` (persisted messages) and
    ``error``.
    """
    started = time.monotonic()

    user_message = ChatMessage(
        chat_id=chat.id, role=ChatMessageRole.USER, content=content
    )
    db.add(user_message)
    await db.commit()
    await db.refresh(user_message)

    try:
        history = await _load_recent_history(db, chat, user_message.id)
        is_first_exchange = not history and chat.summary is None
        history = await _maybe_summarize(db, chat, history)

        docs = await ElegioRetriever().ainvoke(content)
        yield {"event": "sources", "data": json.dumps(_sources_payload(docs))}

        # The visitor's name is not persisted anywhere: once the user shares
        # it, it reaches later turns through the verbatim history or the
        # rolling summary, so the slot itself stays empty.
        messages = CHAT_PROMPT.format_messages(
            user_name="",
            conversation_summary=chat.summary or "(sin resumen)",
            context=_format_context(docs),
            history=_to_langchain_messages(history),
            question=content,
        )

        answer = ""
        aggregate: AIMessageChunk | None = None
        async for chunk in _get_chat_llm().astream(messages):
            # Chunk addition merges usage_metadata correctly (deltas add up).
            aggregate = chunk if aggregate is None else aggregate + chunk
            delta = chunk.text
            if not delta:
                continue
            answer += delta
            yield {"event": "token", "data": json.dumps({"delta": delta})}

        tokens_used = 0
        if aggregate is not None and aggregate.usage_metadata:
            tokens_used = aggregate.usage_metadata.get("total_tokens", 0)

        latency_ms = int((time.monotonic() - started) * 1000)
        assistant_message = ChatMessage(
            chat_id=chat.id,
            role=ChatMessageRole.ASSISTANT,
            content=answer,
            tokens_used=tokens_used,
            latency_ms=latency_ms,
        )
        db.add(assistant_message)
        await db.commit()
        await db.refresh(assistant_message)

        if is_first_exchange and chat.title == DEFAULT_CHAT_TITLE:
            title = await _generate_title(content, answer)
            if title:
                chat.title = title
                await db.commit()
                yield {"event": "title", "data": json.dumps({"title": title})}

        yield {
            "event": "done",
            "data": json.dumps(
                {
                    "user_message": ChatMessageRead.model_validate(
                        user_message
                    ).model_dump(mode="json"),
                    "assistant_message": ChatMessageRead.model_validate(
                        assistant_message
                    ).model_dump(mode="json"),
                }
            ),
        }
    except Exception:
        logger.exception("Chat streaming failed for chat %s", chat.id)
        await db.rollback()
        yield {
            "event": "error",
            "data": json.dumps(
                {"detail": "No se pudo generar la respuesta. Intenta de nuevo."}
            ),
        }
