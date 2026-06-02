from fastapi import APIRouter
from datetime import datetime, timezone

from app.config import settings

router = APIRouter(prefix="/api/v1", tags=["Health"])


@router.get("/health", summary="Service health check")
async def health():
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/", summary="Root — product info")
async def root():
    return {
        "product": "KRONOS CORE",
        "version": settings.app_version,
        "description": (
            "Autonomous Security & Prompt Architecture Gateway. "
            "Converts raw project objectives into secure Claude execution blueprints."
        ),
        "endpoints": {
            "health": "/api/v1/health",
            "blueprint": "POST /api/v1/blueprint",
            "audit": "POST /api/v1/audit",
            "sandbox": "GET /api/v1/sandbox",
            "security_score": "POST /api/v1/security/score",
            "demo": "GET /api/v1/demo",
            "enterprise_report": "GET /api/v1/enterprise/report",
            "docs": "/docs",
        },
    }
