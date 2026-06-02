# KRONOS CORE — Security Checklist

Use this checklist before every production deployment, client demo, and competition submission.
Mark each item ✅ when confirmed, ⚠️ if acceptable risk, ❌ if unresolved.

---

## 1. Dependency Audit

### Python Backend

```bash
# Run from project root
pip install pip-audit
pip-audit -r requirements.txt

# Alternatively, check with safety
pip install safety
safety check -r requirements.txt
```

- [ ] All Python dependencies pinned to minimum versions in `requirements.txt`
- [ ] No known CVEs with CRITICAL or HIGH severity
- [ ] No deprecated packages in active use

### Node.js Frontend

```bash
cd frontend
npm audit
```

- [ ] `npm audit` returns 0 vulnerabilities
- [ ] `postcss` override applied (`>=8.5.10`) — included in `package.json`
- [ ] No packages marked `deprecated` or with known supply chain issues
- [ ] Only packages from the approved list are installed (see `package.json`)

**Current frontend audit status:** ✅ 0 vulnerabilities (as of v1.0)

---

## 2. CORS Policy

File: `app/main.py`

- [ ] `allow_origins` is an explicit list — **never** `["*"]` in production
- [ ] Origins list comes from `settings.origins_list` (environment variable)
- [ ] `allow_credentials=False` unless session cookies are intentionally used
- [ ] `allow_methods=["GET", "POST"]` — minimum required methods only
- [ ] `allow_headers=["Content-Type", "Authorization"]` — explicit, not `["*"]`

**Verification:**
```bash
curl -H "Origin: https://evil.com" http://127.0.0.1:8000/api/v1/health -v 2>&1 | grep -i "access-control"
# Should return no Access-Control-Allow-Origin header
```

---

## 3. Rate Limiting

File: `app/middleware/rate_limiter.py`, individual routers

- [ ] Global limit: 60 requests/minute per IP (configurable via `RATE_LIMIT_PER_MINUTE`)
- [ ] Blueprint endpoint: 20/min (tighter — CPU-intensive)
- [ ] Audit endpoint: 30/min
- [ ] Sandbox endpoint: 15/min (tightest — system calls)
- [ ] Rate limit exceeded returns HTTP 429, not 500
- [ ] nginx adds a second layer of rate limiting in production (see `nginx/nginx.conf`)

---

## 4. Security Response Headers

File: `app/middleware/security_headers.py`

- [ ] `X-Content-Type-Options: nosniff`
- [ ] `X-Frame-Options: DENY`
- [ ] `X-XSS-Protection: 1; mode=block`
- [ ] `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- [ ] `Referrer-Policy: strict-origin-when-cross-origin`
- [ ] `Content-Security-Policy` — path-aware:
  - API routes: `script-src 'none'` (maximum restriction)
  - `/docs`, `/redoc`: CDN allowed + `unsafe-inline` (required by Swagger UI)
- [ ] `Permissions-Policy: geolocation=(), microphone=(), camera=()`
- [ ] `Cache-Control: no-store, no-cache, must-revalidate`

**Verification:**
```bash
curl -s -I http://127.0.0.1:8000/api/v1/health | grep -iE "x-|strict|referrer|content-security|cache"
```

---

## 5. Input Validation

- [ ] All request bodies validated by Pydantic v2 models with explicit field types
- [ ] String fields have `min_length` and `max_length` constraints
- [ ] Numeric fields have `ge` / `le` bounds
- [ ] Invalid input returns HTTP 422 with field-level errors — never 500
- [ ] No user input is executed as shell commands, SQL queries, or file paths
- [ ] Package names in audit endpoint are stripped before processing

**Verification:**
```bash
# Should return 422, not 500
curl -X POST http://127.0.0.1:8000/api/v1/blueprint \
  -H "Content-Type: application/json" \
  -d '{"objective":"short"}'
```

---

## 6. Secrets and Configuration

- [ ] `SECRET_KEY` is set via environment variable — never hard-coded
- [ ] No secrets in `app/config.py` (default values are placeholder strings, not real keys)
- [ ] `.env` is listed in `.gitignore` — confirmed not tracked by git
- [ ] `.env.example` contains only placeholder values
- [ ] `git grep -i "secret\|password\|token\|api_key"` returns no committed secrets

**Verification:**
```bash
git grep -rn "SECRET_KEY\s*=\s*[a-f0-9]\{32\}" -- "*.py" "*.env"
# Should return nothing
```

---

## 7. Structured Logging

File: `app/main.py`, all routers

- [ ] `structlog` configured with JSON renderer
- [ ] Timestamps in ISO format
- [ ] Log level tag on every entry
- [ ] No PII logged (email addresses, user data)
- [ ] No credentials, tokens, or passwords logged
- [ ] Errors logged server-side with full detail; client receives generic message only
- [ ] Correlation reference returned in error responses for support tracing

---

## 8. Error Handling

- [ ] Global exception handler catches unhandled exceptions → HTTP 500 with generic message
- [ ] HTTP 404 returns structured JSON, not HTML
- [ ] HTTP 405 returns structured JSON
- [ ] Rate limit exceeded returns HTTP 429 (handled by slowapi)
- [ ] No stack traces exposed to clients

---

## 9. Docker Container Hardening

File: `docker-compose.yml`, `Dockerfile`

- [ ] Multi-stage build — final image is slim Python base
- [ ] Application user is non-root (UID 10001, GID 10001)
- [ ] `cap_drop: ALL` — no Linux capabilities granted
- [ ] `security_opt: no-new-privileges:true`
- [ ] `read_only: true` — root filesystem is read-only
- [ ] `tmpfs: /tmp` — writable scratch space via tmpfs, not persistent disk
- [ ] `restart: unless-stopped` — automatic recovery
- [ ] Resource limits set: CPU 1.0, memory 512MB
- [ ] Health check wired to `/api/v1/health`

**Verification:**
```bash
docker inspect kronos-core | python -m json.tool | grep -A5 -i "capDrop\|ReadonlyRootfs\|NoNewPrivileges"
```

---

## 10. Sandbox Inspector Safety Limits

File: `app/services/sandbox_inspector.py`

- [ ] Sandbox only **reads** system state — never modifies processes, network, or filesystem
- [ ] Demo mode only **simulates** blocked connections — no real network calls made
- [ ] No subprocess execution initiated by the inspector
- [ ] psutil calls are wrapped in try/except — exceptions degrade gracefully, never crash the service
- [ ] AccessDenied and NoSuchProcess exceptions from psutil are silently ignored (expected in restricted environments)
- [ ] IP range comparison is string-prefix matching against a static list — no DNS resolution, no network requests

---

## 11. Production Deployment Checklist

Before going live:

- [ ] `APP_ENV=production` in environment
- [ ] `SECRET_KEY` is a real random 32+ character hex string
- [ ] `ALLOWED_ORIGINS` contains only your actual domain(s)
- [ ] HTTPS is configured (TLS certificate issued, nginx configured)
- [ ] HSTS header is active (`max-age=31536000`)
- [ ] `LOG_LEVEL=INFO` (not DEBUG — DEBUG may log request bodies)
- [ ] Docker container running as non-root confirmed
- [ ] Health check returning 200 before routing traffic
- [ ] Rate limits tested under expected load
- [ ] Dependency audit run and clean within last 7 days

---

## Running the Full Pre-Deploy Check

```bash
# From project root

# 1. Python dependency audit
pip install pip-audit
pip-audit -r requirements.txt

# 2. Run all backend tests
pytest tests/ -v

# 3. Frontend dependency audit
cd frontend
npm audit

# 4. TypeScript type check
npm run lint

# 5. Production build
npm run build

# 6. Confirm no secrets tracked
git status
git grep -rn "SECRET_KEY=" -- "*.py"
```

All six steps must pass cleanly before any deployment to a non-local environment.
