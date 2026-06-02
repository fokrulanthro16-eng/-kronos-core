import structlog
from fastapi import APIRouter, Request, HTTPException

from app.middleware.rate_limiter import limiter
from app.models.blueprint import BlueprintRequest, BlueprintResponse
from app.services.blueprint_engine import generate_blueprint

log = structlog.get_logger()
router = APIRouter(prefix="/api/v1", tags=["Blueprint"])


@router.post(
    "/blueprint",
    response_model=BlueprintResponse,
    summary="Generate a secure execution blueprint from a raw project objective",
)
@limiter.limit("20/minute")
async def create_blueprint(request: Request, body: BlueprintRequest):
    log.info("blueprint_request", objective_len=len(body.objective), tech_stack=body.tech_stack)
    try:
        blueprint = generate_blueprint(body)
        log.info("blueprint_generated", blueprint_id=blueprint.blueprint_id)
        return blueprint
    except Exception as exc:
        log.error("blueprint_error", error=str(exc))
        raise HTTPException(status_code=500, detail="Blueprint generation failed — internal error")
