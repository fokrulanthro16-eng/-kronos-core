from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Paths that serve Swagger UI / ReDoc HTML — these need scripts and CDN styles.
_DOCS_PATHS = frozenset({"/docs", "/redoc", "/openapi.json"})

# Tight CSP for all API endpoints: no scripts at all.
_API_CSP = "default-src 'self'; script-src 'none'; object-src 'none'"

# Relaxed CSP for interactive docs only.
# Swagger UI loads its bundle from cdn.jsdelivr.net and uses inline event
# handlers, so 'unsafe-inline' is required for that path only.
_DOCS_CSP = (
    "default-src 'self'; "
    "script-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
    "style-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
    "img-src 'self' data: https://fastapi.tiangolo.com; "
    "connect-src 'self'; "
    "object-src 'none'"
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        is_docs = request.url.path in _DOCS_PATHS or request.url.path.startswith("/docs/")

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = _DOCS_CSP if is_docs else _API_CSP
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        response.headers["X-Powered-By"] = "KRONOS-CORE"
        return response
