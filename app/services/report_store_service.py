"""
Report persistence service.

In demo mode (no Supabase configured): every method is a no-op that returns
None.  No errors are raised — the caller ignores the return value and
continues normally.

In SaaS mode (Supabase configured + `supabase` package installed): records are
inserted into the relevant table and the inserted row's `id` is returned.

Activate by:
1. Setting SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY in .env
2. Running the migration:  supabase/migrations/001_initial_schema.sql
3. Installing the package:  pip install supabase
"""
from __future__ import annotations

import structlog
from typing import Optional

from app.db.supabase_client import is_available, get_client
from app.models.saas import (
    StoredAuditRecord,
    StoredBlueprintRecord,
    StoredEnterpriseReportRecord,
    StoredSandboxRecord,
)

log = structlog.get_logger()


def _insert(table: str, record: dict) -> Optional[str]:
    """Insert a record and return its id, or None if Supabase is unavailable."""
    if not is_available():
        return None
    try:
        db = get_client()
        result = db.table(table).insert(record).execute()
        rows = result.data
        if rows:
            return rows[0].get("id")
    except Exception as exc:
        log.warning("report_store_failed", table=table, error=str(exc))
    return None


def store_blueprint(record: StoredBlueprintRecord) -> Optional[str]:
    return _insert(
        "blueprint_requests",
        {
            "organization_id": record.organization_id,
            "user_id": record.user_id,
            "objective": record.objective,
            "generated_blueprint": record.generated_blueprint,
            "risk_score": record.risk_score,
        },
    )


def store_audit(record: StoredAuditRecord) -> Optional[str]:
    return _insert(
        "npm_audit_reports",
        {
            "organization_id": record.organization_id,
            "user_id": record.user_id,
            "package_names": record.package_names,
            "audit_result_json": record.audit_result_json,
            "overall_verdict": record.overall_verdict,
        },
    )


def store_sandbox(record: StoredSandboxRecord) -> Optional[str]:
    return _insert(
        "sandbox_reports",
        {
            "organization_id": record.organization_id,
            "user_id": record.user_id,
            "sandbox_result_json": record.sandbox_result_json,
            "verdict": record.verdict,
            "demo_mode": record.demo_mode,
        },
    )


def store_enterprise_report(record: StoredEnterpriseReportRecord) -> Optional[str]:
    return _insert(
        "enterprise_reports",
        {
            "organization_id": record.organization_id,
            "user_id": record.user_id,
            "report_json": record.report_json,
            "security_score": record.security_score,
            "enterprise_ready": record.enterprise_ready,
        },
    )
