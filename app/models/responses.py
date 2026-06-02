from datetime import datetime, timezone
from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ErrorDetail(BaseModel):
    code: str
    message: str
    detail: Optional[Any] = None


class APIResponse(BaseModel, Generic[T]):
    """Standard envelope for all successful API responses."""
    success: bool = True
    request_id: str
    timestamp: str = Field(default_factory=_utc_now)
    data: Optional[T] = None


class APIErrorResponse(BaseModel):
    """Standard envelope for all error responses."""
    success: bool = False
    request_id: str
    timestamp: str = Field(default_factory=_utc_now)
    error: ErrorDetail


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
    uptime_seconds: float
    checks: dict
