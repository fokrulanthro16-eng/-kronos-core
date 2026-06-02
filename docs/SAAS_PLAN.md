# KRONOS CORE — SaaS Implementation Plan

This document describes the phased roadmap from the current demo-ready v1.0 to a full multi-tenant SaaS product. Each phase is self-contained and deployable independently.

---

## Current State: Demo Mode (v1.0)

- All 8 API endpoints are stateless — no database, no authentication
- The backend and frontend work out of the box with no environment variables beyond the basics
- Docker-deployable in 5 minutes
- Suitable for: local demo, competition presentation, institutional pilot

---

## Phase 1: Auth + Database Foundation ✅ (Current)

**Status:** Infrastructure files created. Waiting for Supabase project configuration.

### What was built in this phase

- `app/config.py` — optional Supabase env vars (`SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_ANON_KEY`, `JWT_SECRET`) with graceful degradation
- `app/db/supabase_client.py` — adapter that activates when vars are set; returns clear errors otherwise
- `app/security/auth.py` — JWT dependency (passthrough in demo mode, verifies in SaaS mode)
- `app/models/saas.py` — Pydantic models for SaaS request/response shapes
- `app/services/report_store_service.py` — no-op in demo mode, persists to Supabase in SaaS mode
- `app/services/org_service.py` — organisation lookup and creation (no-op without Supabase)
- `app/routers/saas.py` — `/api/v1/saas/status` and `/api/v1/saas/schema` endpoints
- `supabase/migrations/001_initial_schema.sql` — full production-quality PostgreSQL schema
- `docs/DATABASE_SCHEMA.md` — documented schema with RLS policy explanations
- `frontend/app/saas/page.tsx` — SaaS Roadmap page showing live configuration status
- `.env.example` and `frontend/.env.example` — updated with all SaaS environment variables

### To activate Phase 1 database features

```bash
# 1. Create a Supabase project at https://supabase.com
# 2. Copy the project URL and keys from the Supabase dashboard
# 3. Set them in .env:
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_ANON_KEY=your-anon-key
JWT_SECRET=your-jwt-secret  # from Settings → API → JWT Settings

# 4. Install the Supabase Python client
pip install supabase

# 5. Run the migration
supabase db push
# or: psql $DATABASE_URL -f supabase/migrations/001_initial_schema.sql

# 6. Confirm activation
curl http://127.0.0.1:8000/api/v1/saas/status
# → {"saas_mode": true, "database_configured": true, ...}
```

---

## Phase 2: Real Login / Register with Supabase Auth

**Goal:** Users can sign up, log in, and belong to an organisation. Protected endpoints require a valid JWT.

### Backend changes

- Add `POST /api/v1/auth/register` — proxy to Supabase Auth `signUp`
- Add `POST /api/v1/auth/login` — proxy to Supabase Auth `signInWithPassword`
- Add `POST /api/v1/auth/logout` — invalidate session
- Add `GET /api/v1/auth/me` — return current user profile
- Activate `require_user` dependency on blueprint, audit, sandbox, score endpoints
- Add `organization_id` to audit payloads when user is authenticated

### Frontend changes

- Add `/login` page with email/password form
- Add `/register` page with org creation flow
- Add Supabase JS client: `npm install @supabase/supabase-js @supabase/ssr`
- Persist session in httpOnly cookie via Next.js middleware
- Show user email and org name in Navbar
- Redirect unauthenticated users to `/login` for protected pages

### Dependencies to install

```bash
# Backend
pip install supabase PyJWT

# Frontend
npm install @supabase/supabase-js @supabase/ssr
```

---

## Phase 3: Save Blueprint / Audit / Sandbox Reports

**Goal:** Every API call made by an authenticated user is persisted to their organisation's history.

### Backend changes

- After a successful blueprint response, call `report_store_service.store_blueprint()`
- After a successful audit response, call `report_store_service.store_audit()`
- After a successful sandbox response, call `report_store_service.store_sandbox()`
- After a successful score/enterprise response, call `report_store_service.store_enterprise_report()`
- Add `GET /api/v1/history/blueprints` — paginated list for current user's org
- Add `GET /api/v1/history/audits` — paginated list
- Add `GET /api/v1/history/sandbox` — paginated list
- Add `GET /api/v1/history/reports` — paginated list

### Frontend changes

- Add `/history` page with tabs: Blueprints | Audits | Sandbox | Reports
- Each tab shows a table of saved records with timestamp, verdict/score, and view link
- Clicking a record shows the full stored JSON in the same UI panels used for live results
- Add "Save Report" toggle to existing pages (enabled by default in SaaS mode)

---

## Phase 4: PDF Enterprise Report Export

**Goal:** Any enterprise report can be downloaded as a branded PDF.

### Backend changes

- Add `GET /api/v1/enterprise/report/pdf` endpoint
- Use `weasyprint` to render the enterprise report HTML template as PDF
- Sign the PDF with a report ID for authenticity
- Allow download of previously stored reports from Phase 3 by ID

### Frontend changes

- Add "Download PDF" button on `/enterprise` page
- PDF includes KRONOS CORE header, compliance alignment tables, score, timestamp, report ID

### Dependencies to install

```bash
pip install weasyprint
```

---

## Phase 5: Stripe Subscription Billing

**Goal:** Users can upgrade their organisation to Team or Enterprise tier, enabling higher rate limits and additional features.

### Backend changes

- Add `POST /api/v1/billing/checkout` — create Stripe Checkout session
- Add `POST /api/v1/billing/portal` — open Stripe Customer Portal
- Add `POST /api/v1/billing/webhook` — handle Stripe events (`customer.subscription.updated`, `invoice.payment_failed`)
- Update `subscription_status` table on webhook receipt
- Enforce plan limits: Starter (5 devs, 500 blueprints/month), Team (25 devs, unlimited), Enterprise (custom)

### Frontend changes

- Add `/billing` page with current plan, usage stats, and upgrade CTA
- Show Upgrade buttons on Dashboard when usage limits are approached
- Success/cancel redirect pages for Stripe Checkout

### Dependencies to install

```bash
pip install stripe
```

---

## Phase 6: Organisation Workspace + Admin Dashboard

**Goal:** Team admins can manage members, view org-level usage, and configure custom allowlists.

### Backend changes

- Add `GET /api/v1/org/members` — list members with roles
- Add `POST /api/v1/org/members/invite` — invite by email
- Add `DELETE /api/v1/org/members/{user_id}` — remove member
- Add `PATCH /api/v1/org/members/{user_id}/role` — change role
- Add `GET /api/v1/org/usage` — blueprint/audit counts for the billing period
- Add `PUT /api/v1/org/allowlist` — custom trusted package list per org

### Frontend changes

- Add `/settings` page with tabs: Members | Billing | Custom Allowlist | Org Profile
- Admin and owner roles see member management UI
- Usage bar showing monthly blueprint/audit consumption vs plan limit

---

## Phase 7: Production Deployment with Domain + HTTPS

**Goal:** KRONOS CORE is accessible at a public domain with a proper SSL certificate.

### Infrastructure

- Register domain (e.g. `kronos-core.io` or `kronos.dev`)
- Set up VPS on DigitalOcean/Hetzner (2 vCPU, 4GB RAM minimum)
- Configure nginx reverse proxy with Certbot SSL
- Deploy backend with Docker Compose
- Deploy frontend with PM2 or Vercel
- Configure Supabase project with production credentials
- Set up Sentry for error monitoring
- Set up PostHog or Plausible for analytics

### CI/CD

- GitHub Actions: lint → test → build → deploy on push to `main`
- Staging environment on push to `develop`
- Automated `npm audit` and `pip-audit` checks on every PR

---

## Feature Flag Strategy

Each phase introduces features that are gated by environment variables:

| Feature | Gates On | Phase |
|---------|----------|-------|
| Database persistence | `SUPABASE_URL` set | 1 |
| JWT authentication | `JWT_SECRET` set | 2 |
| Auth-required endpoints | `AUTH_REQUIRED=true` | 2 |
| Report history | Auth + Supabase | 3 |
| PDF export | `PDF_EXPORT_ENABLED=true` | 4 |
| Stripe billing | `STRIPE_SECRET_KEY` set | 5 |

**Demo mode** (default) activates when none of these are set. All 8 original endpoints continue to work without any SaaS configuration.

---

## Timeline Estimate

| Phase | Effort | Target |
|-------|--------|--------|
| Phase 1 (foundation) | Complete | Now |
| Phase 2 (auth) | 1–2 weeks | Q3 2026 |
| Phase 3 (history) | 1 week | Q3 2026 |
| Phase 4 (PDF) | 3 days | Q3 2026 |
| Phase 5 (billing) | 2 weeks | Q4 2026 |
| Phase 6 (workspace) | 2 weeks | Q4 2026 |
| Phase 7 (production) | 1 week | Q4 2026 |
