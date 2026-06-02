import structlog
from fastapi import APIRouter, Request, HTTPException

from app.middleware.rate_limiter import limiter
from app.models.audit import PackageAuditRequest, PackageAuditResponse
from app.services.npm_auditor import audit_packages

log = structlog.get_logger()
router = APIRouter(prefix="/api/v1", tags=["NPM Audit"])


@router.post(
    "/audit",
    response_model=PackageAuditResponse,
    summary="Static npm package security audit with typosquat and forbidden package detection",
)
@limiter.limit("30/minute")
async def run_audit(request: Request, body: PackageAuditRequest):
    log.info("audit_request", package_count=len(body.packages))
    try:
        result = audit_packages(body)
        log.info(
            "audit_complete",
            audit_id=result.audit_id,
            safe=result.summary.safe,
            flagged=result.summary.flagged,
        )
        return result
    except Exception as exc:
        log.error("audit_error", error=str(exc))
        raise HTTPException(status_code=500, detail="Audit failed — internal error")
