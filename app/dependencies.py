import uuid
from typing import Optional

from fastapi import Header, HTTPException, Request

from app.config import get_settings


async def verify_api_key(
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
) -> None:
    """Enforce API key authentication.

    No-op when API_KEY is unset (development mode). In production, set
    API_KEY in the environment and all /api/v1/* calls must carry the header.
    """
    cfg = get_settings()
    if not cfg.API_KEY:
        return  # dev mode — open access
    if not x_api_key or x_api_key != cfg.API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key. Provide X-API-Key header.",
        )


def get_request_id(request: Request) -> str:
    return getattr(request.state, "request_id", str(uuid.uuid4()))
