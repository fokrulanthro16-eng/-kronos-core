import structlog
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response

from app.middleware.rate_limiter import limiter
from app.services.demo_generator import get_enterprise_report
from app.services.pdf_export_service import (
    build_enterprise_report_pdf,
    build_audit_report_pdf,
    build_blueprint_report_pdf,
)

log = structlog.get_logger()
router = APIRouter(prefix="/api/v1/export", tags=["Export"])

_PDF_HEADERS = {
    "Content-Disposition": 'attachment; filename="kronos-report.pdf"',
    "Cache-Control": "no-store",
}


def _pdf_response(pdf_bytes: bytes, filename: str) -> Response:
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-store",
        },
    )


@router.get(
    "/enterprise/pdf",
    summary="Download the current enterprise readiness report as a branded PDF",
    response_class=Response,
    responses={200: {"content": {"application/pdf": {}}}},
)
@limiter.limit("10/minute")
async def enterprise_pdf(request: Request):
    log.info("pdf_export_request", type="enterprise")
    try:
        report = get_enterprise_report()
        pdf = build_enterprise_report_pdf(report.model_dump(mode="json"))
        return _pdf_response(pdf, "kronos-enterprise-report.pdf")
    except ImportError as exc:
        log.error("pdf_export_missing_lib", error=str(exc))
        raise HTTPException(status_code=501, detail="PDF export requires reportlab: pip install reportlab")
    except Exception as exc:
        log.error("pdf_export_error", type="enterprise", error=str(exc))
        raise HTTPException(status_code=500, detail="PDF generation failed — internal error")


@router.get(
    "/demo/pdf",
    summary="Download a KRONOS CORE pitch/demo summary as a branded PDF",
    response_class=Response,
    responses={200: {"content": {"application/pdf": {}}}},
)
@limiter.limit("10/minute")
async def demo_pdf(request: Request):
    log.info("pdf_export_request", type="demo")
    try:
        report = get_enterprise_report()
        data   = report.model_dump(mode="json")
        data["report_type"] = "Competition / Investor Demo"
        pdf = build_enterprise_report_pdf(data)
        return _pdf_response(pdf, "kronos-demo-report.pdf")
    except ImportError as exc:
        log.error("pdf_export_missing_lib", error=str(exc))
        raise HTTPException(status_code=501, detail="PDF export requires reportlab: pip install reportlab")
    except Exception as exc:
        log.error("pdf_export_error", type="demo", error=str(exc))
        raise HTTPException(status_code=500, detail="PDF generation failed — internal error")
