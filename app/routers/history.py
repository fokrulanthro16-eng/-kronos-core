import structlog
from fastapi import APIRouter, HTTPException

from app.db.supabase_client import is_available
from app.services.report_store_service import (
    list_blueprints,
    list_audits,
    list_sandbox,
    list_enterprise,
)

log = structlog.get_logger()
router = APIRouter(prefix="/api/v1/history", tags=["History"])

_DEMO_MSG = (
    "Database not configured — running in demo mode. "
    "Run supabase/migrations/001_initial_schema.sql in your Supabase SQL Editor to activate history."
)


@router.get("", summary="Recent saved reports grouped by type")
async def get_all_history():
    db_live = is_available()
    return {
        "demo_mode": not db_live,
        "message": None if db_live else _DEMO_MSG,
        "blueprints": list_blueprints(5),
        "audits": list_audits(5),
        "sandbox": list_sandbox(5),
        "enterprise": list_enterprise(5),
    }


@router.get("/blueprints", summary="Saved blueprint reports")
async def get_blueprint_history():
    records = list_blueprints()
    return {"demo_mode": not is_available(), "records": records, "count": len(records)}


@router.get("/audits", summary="Saved NPM audit reports")
async def get_audit_history():
    records = list_audits()
    return {"demo_mode": not is_available(), "records": records, "count": len(records)}


@router.get("/sandbox", summary="Saved sandbox inspection reports")
async def get_sandbox_history():
    records = list_sandbox()
    return {"demo_mode": not is_available(), "records": records, "count": len(records)}


@router.get("/enterprise", summary="Saved enterprise readiness reports")
async def get_enterprise_history():
    records = list_enterprise()
    return {"demo_mode": not is_available(), "records": records, "count": len(records)}


@router.get("/enterprise/{report_id}/pdf", summary="Download a saved enterprise report as PDF")
async def get_enterprise_report_pdf(report_id: str):
    raise HTTPException(
        status_code=501,
        detail=(
            "Per-record PDF export is not yet implemented. "
            "Use GET /api/v1/export/enterprise/pdf to download the current enterprise report."
        ),
    )
