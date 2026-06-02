import structlog
from fastapi import APIRouter, Request, HTTPException

from app.middleware.rate_limiter import limiter
from app.models.demo import CompetitionDemoResponse
from app.services.demo_generator import get_competition_demo

log = structlog.get_logger()
router = APIRouter(prefix="/api/v1", tags=["Competition Demo"])


@router.get(
    "/demo",
    response_model=CompetitionDemoResponse,
    summary="Full competition and investor demo: problem, solution, architecture, pitch, and roadmap",
)
@limiter.limit("30/minute")
async def competition_demo(request: Request):
    log.info("demo_request")
    try:
        result = get_competition_demo()
        return result
    except Exception as exc:
        log.error("demo_error", error=str(exc))
        raise HTTPException(status_code=500, detail="Demo generation failed — internal error")
