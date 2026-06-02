"""
Supabase client adapter.

Returns a configured Supabase client when credentials are present in the
environment.  Raises a descriptive RuntimeError otherwise — never a silent
import error — so callers can surface a clear message to the operator.

Usage (inside a service function):
    from app.db.supabase_client import get_client
    db = get_client()           # raises if not configured
    result = db.table("...").select("*").execute()

The demo and all existing endpoints work without this client.
"""
from __future__ import annotations

from app.config import settings


def get_client():
    """Return a Supabase client.  Raises RuntimeError if not configured."""
    if not settings.supabase_configured:
        raise RuntimeError(
            "Supabase is not configured. "
            "Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in your .env file. "
            "See .env.example for details."
        )
    try:
        from supabase import create_client  # type: ignore[import]
    except ImportError as exc:
        raise RuntimeError(
            "The 'supabase' Python package is not installed. "
            "Activate it by running:  pip install supabase"
        ) from exc

    return create_client(
        settings.supabase_url,          # type: ignore[arg-type]
        settings.supabase_service_role_key,  # type: ignore[arg-type]
    )


def is_available() -> bool:
    """Return True only if Supabase is configured AND the package is installed."""
    if not settings.supabase_configured:
        return False
    try:
        import supabase  # type: ignore[import]  # noqa: F401
        return True
    except ImportError:
        return False
