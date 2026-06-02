"""
SaaS introspection endpoints.

GET /api/v1/saas/status  — whether Supabase / auth env vars are configured
GET /api/v1/saas/schema  — planned database table summary

These endpoints require no authentication and expose no secret values.
They are safe to call from the frontend to render the SaaS Roadmap page.
"""
import structlog
from fastapi import APIRouter, Request

from app.config import settings
from app.db.supabase_client import is_available
from app.middleware.rate_limiter import limiter
from app.models.saas import (
    SaasFeatureStatus,
    SaasSchemaResponse,
    SaasSchemaTable,
    SaasStatusResponse,
)

log = structlog.get_logger()
router = APIRouter(prefix="/api/v1/saas", tags=["SaaS"])


@router.get(
    "/status",
    response_model=SaasStatusResponse,
    summary="SaaS configuration status — which environment variables are set",
)
@limiter.limit("30/minute")
async def saas_status(request: Request) -> SaasStatusResponse:
    log.info("saas_status_request")

    db_configured = settings.supabase_configured
    db_live = is_available()
    auth_ready = settings.auth_configured

    features = [
        SaasFeatureStatus(
            feature="Database (Supabase)",
            status="configured" if db_configured else "not_configured",
            description="Persistent storage for blueprints, audits, sandbox reports, and scores",
            phase="Phase 1",
        ),
        SaasFeatureStatus(
            feature="Supabase SDK",
            status="active" if db_live else ("configured" if db_configured else "not_configured"),
            description="supabase Python package installed and client initialised",
            phase="Phase 1",
        ),
        SaasFeatureStatus(
            feature="JWT Authentication",
            status="configured" if auth_ready else "not_configured",
            description="Verify Supabase-issued JWTs on protected endpoints",
            phase="Phase 2",
        ),
        SaasFeatureStatus(
            feature="User Registration / Login",
            status="planned",
            description="Supabase Auth email/password and OAuth sign-in",
            phase="Phase 2",
        ),
        SaasFeatureStatus(
            feature="Organisation Workspaces",
            status="planned",
            description="Team-level isolation with role-based access",
            phase="Phase 2",
        ),
        SaasFeatureStatus(
            feature="Saved Audit History",
            status="planned",
            description="Persist every blueprint/audit/sandbox/score result per organisation",
            phase="Phase 3",
        ),
        SaasFeatureStatus(
            feature="PDF Enterprise Report Export",
            status="planned",
            description="Downloadable branded PDF from /api/v1/enterprise/report",
            phase="Phase 4",
        ),
        SaasFeatureStatus(
            feature="Stripe Subscription Billing",
            status="planned",
            description="Starter / Team / Enterprise tiers with usage metering",
            phase="Phase 5",
        ),
        SaasFeatureStatus(
            feature="Admin Dashboard",
            status="planned",
            description="Organisation usage metrics, member management, billing overview",
            phase="Phase 6",
        ),
    ]

    if db_configured:
        message = (
            "Supabase environment variables are set. "
            + ("Client ready." if db_live else "Install 'supabase' package to activate: pip install supabase")
        )
    else:
        message = (
            "Running in demo mode. "
            "Set SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, and JWT_SECRET in .env to enable SaaS features."
        )

    return SaasStatusResponse(
        saas_mode=db_configured,
        database_configured=db_configured,
        auth_configured=auth_ready,
        supabase_url_set=bool(settings.supabase_url),
        supabase_keys_set=bool(settings.supabase_service_role_key and settings.supabase_anon_key),
        jwt_secret_set=auth_ready,
        features=features,
        message=message,
    )


@router.get(
    "/schema",
    response_model=SaasSchemaResponse,
    summary="Planned SaaS database schema — table descriptions and phases",
)
@limiter.limit("30/minute")
async def saas_schema(request: Request) -> SaasSchemaResponse:
    tables = [
        SaasSchemaTable(
            table="users_profile",
            description="Extended profile for each authenticated user (mirrors Supabase auth.users)",
            key_columns=["id (uuid, PK)", "email", "full_name", "avatar_url", "created_at"],
            phase="Phase 2",
        ),
        SaasSchemaTable(
            table="organizations",
            description="Workspace / company entity that groups members and reports",
            key_columns=["id (uuid, PK)", "name", "slug", "owner_id (FK)", "plan", "created_at"],
            phase="Phase 2",
        ),
        SaasSchemaTable(
            table="organization_members",
            description="Many-to-many join: users ↔ organisations with role",
            key_columns=["id", "organization_id (FK)", "user_id (FK)", "role", "created_at"],
            phase="Phase 2",
        ),
        SaasSchemaTable(
            table="blueprint_requests",
            description="Saved output from POST /api/v1/blueprint",
            key_columns=["id", "organization_id (FK)", "user_id (FK)", "objective", "risk_score", "created_at"],
            phase="Phase 3",
        ),
        SaasSchemaTable(
            table="npm_audit_reports",
            description="Saved output from POST /api/v1/audit",
            key_columns=["id", "organization_id (FK)", "package_names", "overall_verdict", "created_at"],
            phase="Phase 3",
        ),
        SaasSchemaTable(
            table="sandbox_reports",
            description="Saved output from GET /api/v1/sandbox",
            key_columns=["id", "organization_id (FK)", "verdict", "demo_mode", "created_at"],
            phase="Phase 3",
        ),
        SaasSchemaTable(
            table="enterprise_reports",
            description="Saved output from GET /api/v1/enterprise/report",
            key_columns=["id", "organization_id (FK)", "security_score", "enterprise_ready", "created_at"],
            phase="Phase 3",
        ),
        SaasSchemaTable(
            table="subscription_status",
            description="Stripe subscription and plan metadata per organisation",
            key_columns=[
                "id", "organization_id (FK)", "plan", "status",
                "stripe_customer_id", "stripe_subscription_id", "current_period_end",
            ],
            phase="Phase 5",
        ),
    ]

    return SaasSchemaResponse(
        schema_version="1.0",
        database="PostgreSQL via Supabase",
        tables=tables,
        rls_enabled=True,
        migration_file="supabase/migrations/001_initial_schema.sql",
    )
