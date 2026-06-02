"""
Auth introspection router.

GET /api/v1/auth/status  — whether auth/Supabase environment variables are set.

This endpoint never returns actual secret values — only boolean flags.
It is used by the frontend SaaS page and is safe to call unauthenticated.
"""
import structlog
from fastapi import APIRouter, Request
from pydantic import BaseModel

from app.config import settings
from app.middleware.rate_limiter import limiter

log = structlog.get_logger()
router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


class AuthStatusResponse(BaseModel):
    auth_configured: bool
    supabase_url_configured: bool
    anon_key_configured: bool
    service_role_configured: bool
    jwt_secret_configured: bool
    mode: str          # "configured" | "demo"
    message: str


@router.get(
    "/status",
    response_model=AuthStatusResponse,
    summary="Auth configuration status — which environment variables are set (no secrets exposed)",
)
@limiter.limit("30/minute")
async def auth_status(request: Request) -> AuthStatusResponse:
    url_ok = bool(settings.supabase_url)
    anon_ok = bool(settings.supabase_anon_key)
    svc_ok = bool(settings.supabase_service_role_key)
    jwt_ok = settings.auth_configured
    fully_configured = url_ok and anon_ok and svc_ok and jwt_ok

    mode = "configured" if fully_configured else "demo"

    if fully_configured:
        message = "All auth environment variables are set. JWT verification is active."
    else:
        missing = []
        if not url_ok:
            missing.append("SUPABASE_URL")
        if not anon_ok:
            missing.append("SUPABASE_ANON_KEY")
        if not svc_ok:
            missing.append("SUPABASE_SERVICE_ROLE_KEY")
        if not jwt_ok:
            missing.append("JWT_SECRET")
        message = f"Demo mode. Missing: {', '.join(missing)}. See docs/SUPABASE_AUTH_SETUP.md."

    log.info("auth_status_request", mode=mode)

    return AuthStatusResponse(
        auth_configured=jwt_ok,
        supabase_url_configured=url_ok,
        anon_key_configured=anon_ok,
        service_role_configured=svc_ok,
        jwt_secret_configured=jwt_ok,
        mode=mode,
        message=message,
    )
