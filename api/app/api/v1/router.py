from fastapi import APIRouter

from app.domains.candidate.routes import router as candidate_router
from app.domains.proposal.routes import router as proposal_router
from app.domains.test.routes import router as test_router
from app.domains.test_attempt.routes import router as test_attempt_router
from app.domains.visitor.routes import router as visitor_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(visitor_router)
api_router.include_router(test_router)
api_router.include_router(test_attempt_router)
api_router.include_router(candidate_router)
api_router.include_router(proposal_router)


@api_router.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
