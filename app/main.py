import structlog
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.middleware.rate_limiter import limiter
from app.routers import health, blueprint, audit, sandbox, security, demo, enterprise, saas, auth, history, export, billing

# Pinned Swagger UI version — avoids silent breakage from floating @5 tag.
_SWAGGER_JS = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.18.2/swagger-ui-bundle.js"
_SWAGGER_CSS = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.18.2/swagger-ui.css"
_REDOC_JS = "https://cdn.jsdelivr.net/npm/redoc@2.1.5/bundles/redoc.standalone.js"

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.JSONRenderer(),
    ]
)

log = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("kronos_startup", version=settings.app_version, env=settings.app_env)
    yield
    log.info("kronos_shutdown")


app = FastAPI(
    title="KRONOS CORE",
    description=(
        "**Autonomous Security & Prompt Architecture Gateway**\n\n"
        "KRONOS CORE converts raw project objectives into hardened Claude execution blueprints, "
        "audits npm packages for supply chain threats, inspects runtime behaviour for exfiltration, "
        "and scores overall enterprise security posture across 6 dimensions.\n\n"
        "Built for software companies, AI startups, banks, government digital teams, and universities "
        "that need a security governance layer over AI-assisted development."
    ),
    version=settings.app_version,
    # Disable built-in docs routes so we can mount custom ones with pinned CDN assets.
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(SecurityHeadersMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "product": "KRONOS CORE", "docs": "/docs"},
    )


@app.exception_handler(405)
async def method_not_allowed_handler(request: Request, exc):
    return JSONResponse(
        status_code=405,
        content={"error": "Method not allowed"},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    log.error("unhandled_exception", path=str(request.url), error=str(exc))
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "reference": "Check service logs for correlation ID"},
    )


@app.get("/docs", include_in_schema=False)
async def swagger_ui() -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="KRONOS CORE — API Docs",
        swagger_js_url=_SWAGGER_JS,
        swagger_css_url=_SWAGGER_CSS,
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
    )


@app.get("/redoc", include_in_schema=False)
async def redoc_ui() -> HTMLResponse:
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="KRONOS CORE — ReDoc",
        redoc_js_url=_REDOC_JS,
    )


app.include_router(health.router)
app.include_router(blueprint.router)
app.include_router(audit.router)
app.include_router(sandbox.router)
app.include_router(security.router)
app.include_router(demo.router)
app.include_router(enterprise.router)
app.include_router(saas.router)
app.include_router(auth.router)
app.include_router(history.router)
app.include_router(export.router)
app.include_router(billing.router)
