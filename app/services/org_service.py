"""
Organisation / workspace service.

Stub for Phase 2.  All public functions return sensible defaults when Supabase
is not configured — callers do not need to check for SaaS mode.
"""
from __future__ import annotations

import structlog
from typing import Optional

from app.db.supabase_client import is_available, get_client

log = structlog.get_logger()


def get_org_for_user(user_id: str) -> Optional[dict]:
    """Return the primary organisation for a user, or None."""
    if not is_available():
        return None
    try:
        db = get_client()
        result = (
            db.table("organization_members")
            .select("organization_id, role, organizations(id, name, slug, plan)")
            .eq("user_id", user_id)
            .limit(1)
            .execute()
        )
        rows = result.data
        return rows[0] if rows else None
    except Exception as exc:
        log.warning("org_lookup_failed", user_id=user_id, error=str(exc))
        return None


def create_org(owner_id: str, name: str, slug: str) -> Optional[dict]:
    """Create a new organisation and add the owner as a member."""
    if not is_available():
        return None
    try:
        db = get_client()
        org_result = (
            db.table("organizations")
            .insert({"owner_id": owner_id, "name": name, "slug": slug, "plan": "starter"})
            .execute()
        )
        org = org_result.data[0] if org_result.data else None
        if org:
            db.table("organization_members").insert(
                {"organization_id": org["id"], "user_id": owner_id, "role": "owner"}
            ).execute()
        return org
    except Exception as exc:
        log.warning("org_create_failed", owner_id=owner_id, error=str(exc))
        return None


def get_org_plan(organization_id: str) -> str:
    """Return the plan name for an org, defaulting to 'starter'."""
    if not is_available():
        return "starter"
    try:
        db = get_client()
        result = (
            db.table("organizations")
            .select("plan")
            .eq("id", organization_id)
            .single()
            .execute()
        )
        return (result.data or {}).get("plan", "starter")
    except Exception as exc:
        log.warning("org_plan_lookup_failed", org_id=organization_id, error=str(exc))
        return "starter"
