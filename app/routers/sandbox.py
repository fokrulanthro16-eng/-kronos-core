import structlog
from fastapi import APIRouter, Request, Query, HTTPException

from app.middleware.rate_limiter import limiter
from app.models.sandbox import SandboxInspectionResponse
from app.services.sandbox_inspector import run_sandbox_inspection

log = structlog.get_logger()
router = APIRouter(prefix="/api/v1", tags=["Sandbox"])


@router.get(
    "/sandbox",
    response_model=SandboxInspectionResponse,
    summary="Dynamic runtime behavioural sandbox inspection with zero-exfiltration demo mode",
)
@limiter.limit("15/minute")
async def sandbox_inspect(
    request: Request,
    demo: bool = Query(default=True, description="Enable demo mode with simulated blocked actions"),
):
    log.info("sandbox_request", demo_mode=demo)
    try:
        result = run_sandbox_inspection(demo_mode=demo)
        log.info("sandbox_complete", inspection_id=result.inspection_id, verdict=result.verdict)
        return result
    except Exception as exc:
        log.error("sandbox_error", error=str(exc))
        raise HTTPException(status_code=500, detail="Sandbox inspection failed — internal error")
