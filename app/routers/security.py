import structlog
from fastapi import APIRouter, Request, HTTPException

from app.middleware.rate_limiter import limiter
from app.models.security_score import SecurityScoreRequest, SecurityScoreResponse
from app.services.security_scorer import compute_security_score

log = structlog.get_logger()
router = APIRouter(prefix="/api/v1", tags=["Security Score"])


@router.post(
    "/security/score",
    response_model=SecurityScoreResponse,
    summary="Compute a 6-dimension enterprise security score across the full KRONOS pipeline",
)
@limiter.limit("20/minute")
async def security_score(request: Request, body: SecurityScoreRequest):
    log.info("score_request", body=body.model_dump())
    try:
        result = compute_security_score(body)
        log.info(
            "score_complete",
            score_id=result.score_id,
            total=result.total_score,
            risk=result.risk_level,
        )
        return result
    except Exception as exc:
        log.error("score_error", error=str(exc))
        raise HTTPException(status_code=500, detail="Security scoring failed — internal error")
