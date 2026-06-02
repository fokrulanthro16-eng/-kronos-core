import uuid
from datetime import datetime, timezone

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import get_logger

logger = get_logger(__name__)


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def _req_id(request: Request) -> str:
    return getattr(request.state, "request_id", str(uuid.uuid4()))


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    logger.warning("http_exception", status=exc.status_code, detail=exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "request_id": _req_id(request),
            "timestamp": _ts(),
            "error": {"code": f"HTTP_{exc.status_code}", "message": str(exc.detail)},
        },
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    # jsonable_encoder converts non-serialisable objects (e.g. ValueError in ctx)
    errors = jsonable_encoder(exc.errors())
    logger.warning("validation_error", errors=errors)
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "request_id": _req_id(request),
            "timestamp": _ts(),
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request body failed validation",
                "detail": errors,
            },
        },
    )


async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    logger.warning("rate_limit_exceeded", path=str(request.url.path))
    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "request_id": _req_id(request),
            "timestamp": _ts(),
            "error": {
                "code": "RATE_LIMIT_EXCEEDED",
                "message": "Too many requests. Slow down and retry.",
            },
        },
        headers={"Retry-After": "60"},
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("unhandled_exception", exc=str(exc), exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "request_id": _req_id(request),
            "timestamp": _ts(),
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred.",
            },
        },
    )
