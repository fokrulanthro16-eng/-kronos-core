import structlog
from fastapi import APIRouter, Request, HTTPException

from app.middleware.rate_limiter import limiter
from app.models.demo import EnterpriseReportResponse
from app.models.saas import StoredEnterpriseReportRecord
from app.services.demo_generator import get_enterprise_report
from app.services.report_store_service import store_enterprise_report

log = structlog.get_logger()
router = APIRouter(prefix="/api/v1", tags=["Enterprise"])


@router.get(
    "/enterprise/report",
    response_model=EnterpriseReportResponse,
    summary="Generate an enterprise readiness and compliance report for institutional buyers",
)
@limiter.limit("20/minute")
async def enterprise_report(request: Request):
    log.info("enterprise_report_request")
    try:
        result = get_enterprise_report()
        log.info("enterprise_report_generated", report_id=result.report_id)
        try:
            store_enterprise_report(StoredEnterpriseReportRecord(
                report_json=result.model_dump(mode="json"),
                security_score=0,
                risk_level="LOW",
                enterprise_ready=True,
            ))
        except Exception as save_exc:
            log.warning("enterprise_save_failed", error=str(save_exc))
        return result
    except Exception as exc:
        log.error("enterprise_report_error", error=str(exc))
        raise HTTPException(status_code=500, detail="Enterprise report generation failed — internal error")
