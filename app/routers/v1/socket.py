from fastapi import APIRouter, Depends, Request

from app.dependencies import get_request_id, verify_api_key
from app.limiter import limiter
from app.models.responses import APIResponse
from app.services.socket_inspector import get_suspicious_connections, inspect_sockets
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get(
    "/inspect",
    response_model=APIResponse[dict],
    summary="Snapshot all current system socket connections",
)
@limiter.limit("20/minute")
async def socket_inspect(
    request: Request,
    _: None = Depends(verify_api_key),
) -> APIResponse[dict]:
    req_id = get_request_id(request)
    connections = inspect_sockets()
    suspicious = [c for c in connections if c["suspicious"]]
    return APIResponse(
        request_id=req_id,
        data={
            "total_connections": len(connections),
            "suspicious_count": len(suspicious),
            "connections": connections,
        },
    )


@router.get(
    "/suspicious",
    response_model=APIResponse[dict],
    summary="Return only flagged suspicious socket connections",
)
@limiter.limit("20/minute")
async def socket_suspicious(
    request: Request,
    _: None = Depends(verify_api_key),
) -> APIResponse[dict]:
    req_id = get_request_id(request)
    suspicious = get_suspicious_connections()
    return APIResponse(
        request_id=req_id,
        data={
            "alert": len(suspicious) > 0,
            "suspicious_count": len(suspicious),
            "connections": suspicious,
        },
    )
