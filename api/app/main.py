import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api.v1.router import api_router
from app.core.bm25_index import get_bm25_index
from app.core.config import get_settings
from app.core.database import AsyncSessionLocal
from app.core.embedder import get_embedder
from app.core.rate_limit import limiter

settings = get_settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    t0 = time.perf_counter()
    try:
        logger.info("Loading embedding model (multilingual-e5-large)...")
        _ = get_embedder().model
        logger.info("Embedder ready in %.1fs", time.perf_counter() - t0)
    except Exception:
        logger.exception("Embedder pre-load failed; will fall back to lazy load")

    t1 = time.perf_counter()
    try:
        logger.info("Building BM25 index from proposal_chunks...")
        async with AsyncSessionLocal() as db:
            await get_bm25_index().ensure_loaded(db)
        logger.info("BM25 index ready in %.1fs", time.perf_counter() - t1)
    except Exception:
        logger.exception("BM25 pre-load failed; will fall back to lazy load")

    yield


app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG, lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(api_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"app": settings.APP_NAME, "env": settings.APP_ENV}
