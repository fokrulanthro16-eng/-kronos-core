import structlog
from fastapi import APIRouter, Request, Query, HTTPException

from app.middleware.rate_limiter import limiter
from app.models.sandbox import SandboxInspectionResponse
from app.models.saas import StoredSandboxRecord
from app.services.sandbox_inspector import run_sandbox_inspection
from app.services.report_store_service import store_sandbox

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
        try:
            store_sandbox(StoredSandboxRecord(
                sandbox_result_json=result.model_dump(mode="json"),
                verdict=result.verdict.value,
                demo_mode=demo,
            ))
        except Exception as save_exc:
            log.warning("sandbox_save_failed", error=str(save_exc))
        return result
    except Exception as exc:
        log.error("sandbox_error", error=str(exc))
        raise HTTPException(status_code=500, detail="Sandbox inspection failed — internal error")
