# KRONOS CORE — Authentication Implementation Plan

Authentication is not implemented in v1.0. This document explains the options and the recommended implementation path for when auth is added.

The current API is stateless and unauthenticated by design — suitable for self-hosted deployments where the host controls access at the network layer. Authentication becomes relevant when KRONOS CORE moves to a multi-tenant SaaS model (v2.1 on the roadmap).

---

## Current Security Posture (v1.0)

Without auth, access control is enforced by:
1. **Rate limiting** — slowapi limits by IP address (60 req/min global)
2. **CORS** — only explicitly allowed origins can call the API from browsers
3. **Network-level access control** — self-hosted deployments restrict access via firewall rules, VPC, or nginx `allow`/`deny` directives
4. **Docker network isolation** — the container is not exposed beyond the configured port

For demo, competition, and institutional pilot use, this is acceptable.

---

## Option 1: Supabase Auth (Recommended for SaaS)

**What it is:** Supabase is a Postgres-as-a-service platform with a built-in Auth module supporting email/password, magic link, OAuth (Google, GitHub, etc.), and enterprise SSO via SAML.

**Why recommended:**
- Managed service — no need to build or maintain auth infrastructure
- Postgres database included — needed for v2.1 audit history feature anyway
- Row-level security (RLS) allows per-organisation data isolation at the database level
- Free tier covers MVP scale (50,000 monthly active users)
- Well-documented Python SDK: `supabase-py`

**Implementation sketch:**

```python
# New dependency: supabase-py
# pip install supabase

# app/services/auth.py
from supabase import create_client, Client

supabase: Client = create_client(
    settings.supabase_url,
    settings.supabase_anon_key
)

async def verify_token(token: str) -> dict:
    user = supabase.auth.get_user(token)
    if not user or not user.user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"user_id": user.user.id, "email": user.user.email}
```

```python
# app/dependencies.py
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    return await verify_token(credentials.credentials)
```

```python
# Apply to a protected endpoint
@router.post("/blueprint")
async def create_blueprint(
    body: BlueprintRequest,
    user: dict = Depends(get_current_user)   # ← add this
):
    ...
```

**New environment variables needed:**
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

**Frontend (Next.js):**
```bash
npm install @supabase/supabase-js @supabase/ssr
```

The Supabase JS client handles token storage, refresh, and passing the Bearer token to the API automatically.

---

## Option 2: Clerk

**What it is:** Clerk is a user management platform with pre-built React components (sign-in, sign-up, user profile). It handles auth UI entirely.

**Why consider it:**
- Fastest time-to-working-auth for Next.js projects (15 minutes)
- Built-in organisation and team management
- React components handle all UI — no custom auth pages needed
- Generous free tier

**Why it may not suit KRONOS CORE long-term:**
- Closed-source, cloud-only — cannot be self-hosted
- Enterprise customers requiring on-premises deployment cannot use it
- Higher cost at scale compared to Supabase

**Implementation:**
```bash
npm install @clerk/nextjs
pip install clerk-backend-api
```

Wrap `app/layout.tsx` in `<ClerkProvider>`. Add `clerkMiddleware()` to `middleware.ts`. Verify JWT on the FastAPI side using Clerk's JWKS endpoint.

---

## Option 3: Auth.js (NextAuth.js)

**What it is:** The standard open-source authentication library for Next.js. Supports 50+ OAuth providers, email/password, magic links, and database sessions.

**Why consider it:**
- Fully open-source, self-hostable
- No vendor dependency
- Built-in support for PostgreSQL session storage
- Works well with the existing Next.js App Router

**Why it's more work:**
- Auth.js handles the frontend auth flow but does NOT provide a backend auth SDK
- Backend (FastAPI) must validate session tokens independently
- JWT validation between Next.js and FastAPI requires a shared secret or JWKS

**Recommended only if:** The product will always be self-hosted and vendor independence is a hard requirement.

---

## Option 4: Enterprise SSO (Future — v3.2)

For government and enterprise buyers, SAML 2.0 / OIDC SSO is frequently a procurement requirement.

**Options:**
- **Supabase** supports SAML SSO in the Team plan ($25/month+)
- **Clerk** supports SAML SSO in the Business plan
- **python-saml** — direct SAML implementation for FastAPI (complex, full control)
- **Keycloak** — open-source identity provider for fully self-hosted enterprise SSO

Enterprise SSO is deferred to v3.2. The auth abstraction layer (Option 1 or 2) must be designed to accommodate it without a rewrite.

---

## Implementation Priority

| When | Action |
|------|--------|
| v1.0 (now) | No auth. Network-level access control for self-hosted. Rate limiting for public demo. |
| v2.1 (Q2 2027) | Add Supabase Auth. Protect blueprint, audit history, and score endpoints. Public health/demo endpoints remain open. |
| v2.2 | Add organisation workspaces to Supabase RLS. Team invite flow. |
| v3.2 | Add Clerk or Supabase SAML SSO for enterprise procurement requirements. |

---

## What to Keep Unauthenticated

Even after auth is added, these endpoints should remain publicly accessible (no token required):
- `GET /api/v1/health` — monitoring and uptime checks
- `GET /api/v1/` — product info
- `GET /api/v1/demo` — competition/investor pitch response
- `GET /docs`, `GET /redoc`, `GET /openapi.json` — API documentation

This ensures KRONOS CORE can always be evaluated without credentials, which is important for competition demos and institutional pilots.

---

## Security Notes for Auth Implementation

When auth is added:
1. **Never store tokens in localStorage** — use httpOnly cookies or Supabase's session management
2. **Short-lived access tokens** — 15 minutes max; refresh token rotation
3. **Token verification on every request** — no caching of auth state server-side
4. **Audit log all authenticated actions** — who called which endpoint, when, from which IP
5. **Separate service-to-service auth** — CI/CD pipelines should use API keys, not user tokens
6. **Rate limit per user, not just per IP** — after auth, rate limits should apply to the authenticated user ID
