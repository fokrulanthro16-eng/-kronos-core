# KRONOS CORE — Production Deployment Checklist

Work through this list top-to-bottom before going live.

---

## Code & Tests

- [ ] `python -m pytest -q` — all tests pass
  ```
  cd kronos-core
  python -m pytest -q
  # Expected: 82 passed, 0 failed
  ```
- [ ] `npm run build` — frontend compiles clean
  ```
  cd frontend
  npm run build
  # Expected: compiled successfully, 0 TypeScript errors
  ```
- [ ] No uncommitted secrets in git history
  ```
  git log --oneline | head -20
  git diff HEAD
  ```
- [ ] `.env` and `frontend/.env.local` are git-ignored
  ```
  git check-ignore -v .env frontend/.env.local
  ```

---

## Environment Variables

- [ ] `APP_ENV=production` is set
- [ ] `SECRET_KEY` is a fresh random 32+ char string
- [ ] `CORS_ALLOWED_ORIGINS` matches your exact frontend domain (no trailing slash)
- [ ] `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are set (SaaS features)
- [ ] `JWT_SECRET` is set (auth features)
- [ ] `STRIPE_SECRET_KEY` is set (billing, if activating)
- [ ] `STRIPE_WEBHOOK_SECRET` is set (billing, if activating)
- [ ] Frontend `NEXT_PUBLIC_API_BASE_URL` points to production backend URL

---

## Database

- [ ] Supabase project created
- [ ] Migration run: `supabase/migrations/001_initial_schema.sql`
  - Open Supabase → SQL Editor → New Query → paste SQL → Run
- [ ] Row-Level Security (RLS) enabled on all tables (migration handles this)

---

## Auth

- [ ] Register endpoint works: `POST /api/v1/auth/status` returns `mode: configured`
- [ ] Frontend `/register` and `/login` pages load
- [ ] Test signup → receive confirmation email → login → `/account` loads

---

## PDF Export

- [ ] `GET /api/v1/export/enterprise/pdf` returns a downloadable PDF
  ```
  curl -o test.pdf http://your-api/api/v1/export/enterprise/pdf
  ```
- [ ] PDF opens correctly and shows KRONOS CORE branding
- [ ] Download PDF button on `/enterprise` frontend page works

---

## Billing

- [ ] `GET /api/v1/billing/status` returns expected response
- [ ] If Stripe configured: `billing_configured: true`
- [ ] If Stripe not yet configured: `demo_mode: true` (safe)
- [ ] `/pricing` page loads and shows 4 plan cards

---

## Infrastructure

- [ ] Docker image builds cleanly
  ```
  docker build -t kronos-core:1.0.0 .
  ```
- [ ] Container starts and health check passes
  ```
  docker compose up -d
  curl http://localhost:8000/api/v1/health
  ```
- [ ] Domain DNS A record points to server IP
- [ ] HTTPS certificate obtained (Let's Encrypt or provider)
- [ ] HTTP → HTTPS redirect configured in nginx
- [ ] Nginx reverse proxy passes requests to backend container

---

## Security

- [ ] Security headers present on API responses
  ```
  curl -I https://api.your-domain.com/api/v1/health
  # Check: x-content-type-options, x-frame-options, strict-transport-security
  ```
- [ ] CORS rejects cross-origin requests from unlisted domains
- [ ] Rate limiting active (test by hitting endpoint 30+ times quickly)
- [ ] `/docs` and `/redoc` accessible (or intentionally blocked by nginx policy)
- [ ] No `SECRET_KEY`, `SERVICE_ROLE_KEY`, or `STRIPE_SECRET_KEY` visible in any API response

---

## Monitoring

- [ ] Container logs flowing: `docker logs -f kronos-core`
- [ ] Health check endpoint reachable from external network
- [ ] Uptime monitor configured (UptimeRobot / Betterstack — free tier works)

---

## Backup & Rollback

- [ ] **Backup:** Supabase automatic daily backups enabled (Dashboard → Settings → Backups)
- [ ] **Rollback plan:** `docker compose down && git checkout <previous-tag> && docker compose up -d --build`
- [ ] Previous Docker image tagged and stored: `docker tag kronos-core:1.0.0 kronos-core:backup`

---

## Go-Live

- [ ] All items above checked
- [ ] Smoke test passes: `scripts/production_smoke_test.ps1`
- [ ] Share backend URL: `https://api.your-domain.com/docs`
- [ ] Share frontend URL: `https://your-domain.com`
