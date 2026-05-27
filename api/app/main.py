import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api.v1.router import api_router
from app.core.bm25_index import get_bm25_index
from app.core.config import get_settings
from app.core.database import AsyncSessionLocal
from app.core.rate_limit import limiter

settings = get_settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not settings.EAGER_LOAD_SEARCH_ON_STARTUP:
        logger.info("Skipping search pre-load; EAGER_LOAD_SEARCH_ON_STARTUP is disabled")
        yield
        return

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_origin_regex=settings.CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(api_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"app": settings.APP_NAME, "env": settings.APP_ENV}
