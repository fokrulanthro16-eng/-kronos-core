import re

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field, field_validator

from app.dependencies import get_request_id, verify_api_key
from app.limiter import limiter
from app.models.responses import APIResponse
from app.services.sandbox import analyze_package_behavior, get_docker_isolation_command
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


class SandboxRequest(BaseModel):
    package_name: str = Field(..., min_length=1, max_length=214, examples=["express"])

    @field_validator("package_name")
    @classmethod
    def validate(cls, v: str) -> str:
        if not re.match(r'^(@[a-z0-9\-~][a-z0-9\-._~]*/)?[a-z0-9\-~][a-z0-9\-._~]*$', v.lower()):
            raise ValueError(f"Invalid npm package name: '{v}'")
        return v.lower()


@router.post(
    "/analyze",
    response_model=APIResponse[dict],
    summary="Behavioral sandbox analysis of an npm package",
)
@limiter.limit("5/minute")
async def sandbox_analyze(
    request: Request,
    body: SandboxRequest,
    _: None = Depends(verify_api_key),
) -> APIResponse[dict]:
    req_id = get_request_id(request)
    result = await analyze_package_behavior(body.package_name)
    result["docker_isolation_command"] = get_docker_isolation_command(body.package_name)
    return APIResponse(request_id=req_id, data=result)
