"""
JWT authentication module.

Phase 2 status: PASSTHROUGH MODE
  — All existing demo endpoints work without any token.
  — `get_current_user_optional` returns None in demo mode.
  — `require_user` raises 401 only when called on a protected endpoint.

To activate real JWT verification:
  1. Set JWT_SECRET in .env (copy from Supabase Dashboard → Settings → API → JWT Secret)
  2. pip install PyJWT
  3. Apply `Depends(require_user)` to any endpoint you want to protect.
"""
from __future__ import annotations

from typing import Optional

import structlog
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import settings

log = structlog.get_logger()

_bearer = HTTPBearer(auto_error=False)


def extract_bearer_token(authorization_header: Optional[str]) -> Optional[str]:
    """Parse 'Bearer <token>' from a raw Authorization header string."""
    if not authorization_header:
        return None
    parts = authorization_header.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None


def verify_supabase_jwt(token: str) -> Optional[dict]:
    """
    Verify a Supabase-issued JWT.

    Returns the decoded payload dict on success, or None if:
    - JWT_SECRET is not configured (demo mode passthrough)
    - PyJWT is not installed

    Raises HTTPException(401) if the token is present but invalid/expired.
    """
    if not settings.auth_configured:
        return None

    try:
        import jwt  # PyJWT  # type: ignore[import]
    except ImportError:
        log.warning("auth_jwt_unavailable", hint="pip install PyJWT")
        return None

    try:
        payload: dict = jwt.decode(
            token,
            settings.jwt_secret,  # type: ignore[arg-type]
            algorithms=["HS256"],
            options={"verify_exp": True},
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=401, detail=f"Invalid token: {exc}")


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(_bearer),
) -> Optional[dict]:
    """Extract and verify a JWT if present.  Returns None in demo mode."""
    if not credentials:
        return None
    return verify_supabase_jwt(credentials.credentials)


async def require_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(_bearer),
) -> dict:
    """Require a valid JWT.  Raises HTTP 401 if not present or invalid.

    Not applied to any current endpoint — reserved for Phase 2+ protected routes.
    Add as a dependency:  user: dict = Depends(require_user)
    """
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Provide a valid Bearer token.",
        )
    user = verify_supabase_jwt(credentials.credentials)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Configure JWT_SECRET to enable auth.",
        )
    return user
