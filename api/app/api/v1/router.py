from fastapi import APIRouter

from app.domains.answer.routes import router as answer_router
from app.domains.auth.routes import router as auth_router
from app.domains.candidate.routes import router as candidate_router
from app.domains.event.routes import router as event_router
from app.domains.government_plan.routes import router as government_plan_router
from app.domains.proposal.routes import router as proposal_router
from app.domains.question.routes import router as question_router
from app.domains.response_option.routes import router as response_option_router
from app.domains.search.routes import router as search_router
from app.domains.test.routes import router as test_router
from app.domains.test_attempt.routes import router as test_attempt_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)
api_router.include_router(test_router)
api_router.include_router(test_attempt_router)
api_router.include_router(candidate_router)
api_router.include_router(proposal_router)
api_router.include_router(government_plan_router)
api_router.include_router(event_router)
api_router.include_router(question_router)
api_router.include_router(response_option_router)
api_router.include_router(answer_router)
api_router.include_router(search_router)

