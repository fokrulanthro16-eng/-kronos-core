# KRONOS CORE

> **Autonomous Security & Prompt Architecture Gateway**
>
> *The security layer every AI-first engineering team needs — and cannot build themselves.*

[![CI](https://github.com/Fokrul/kronos-core/actions/workflows/ci.yml/badge.svg)](https://github.com/Fokrul/kronos-core/actions/workflows/ci.yml)
[![Backend Tests](https://img.shields.io/badge/tests-82%20passed-00ff88?style=flat-square)](#testing)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square)](#local-setup)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?style=flat-square)](#backend-api-endpoints)
[![Next.js](https://img.shields.io/badge/Next.js-16-black?style=flat-square)](#frontend-pages)
[![Docker](https://img.shields.io/badge/docker-hardened-2496ED?style=flat-square)](#docker-deployment)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](#)

---

## One-Line Pitch

**KRONOS CORE converts raw project objectives into secure Claude execution blueprints, audits every npm dependency for supply chain threats, inspects runtime behaviour for exfiltration, and scores your AI development pipeline on a 100-point enterprise security scale — all from a single API.**

---

## Executive Summary

Organisations adopting AI coding tools face an invisible compounding risk: AI generates insecure code, hallucinated packages get installed, typosquatted libraries steal credentials, and hidden network calls exfiltrate data after deployment. No existing tool addresses all four risks in one place.

KRONOS CORE is an API-first security gateway microservice that sits between a developer's intent and the AI model. It enforces secure execution standards before development begins, audits packages before they are installed, and inspects runtime behaviour before deployment is approved. It generates human-readable compliance reports suitable for boardrooms, procurement teams, and competition judges.

- **Backend:** FastAPI microservice — 13 endpoint groups, rate-limited, CORS-locked, security-headered, structured logging
- **Frontend:** Next.js dashboard — 14 pages, live API integration, dark cyber-security theme
- **Tests:** 82 passing, 0 failing
- **Deploy:** Docker Compose in under 5 minutes

### SaaS Features (Phase 1–6 complete)

| Feature | Status |
|---|---|
| Blueprint generator | Live |
| NPM audit (typosquat detection) | Live |
| Sandbox inspection | Live |
| Enterprise report + PDF export | Live |
| Security score | Live |
| Supabase Auth (login/register) | Live |
| Report history (database-backed) | Live |
| PDF export for reports | Live |
| Billing & subscription foundation | Live |
| CI/CD (GitHub Actions) | Live |

---

## The Problem

Every company using AI coding assistants faces four invisible, compounding risks:

| # | Risk | Real-World Impact | Current Coverage |
|---|------|-------------------|-----------------|
| 1 | **Unsafe AI Prompts** | AI produces code missing auth, validation, or encryption because the prompt was never hardened | None |
| 2 | **Typosquatted Packages** | `expresss`, `lodahs`, `crossenv` harvest credentials silently at `npm install` time | Manual review — fails at scale |
| 3 | **Phantom Packages** | LLMs confidently hallucinate package names that either don't exist or are malicious | None |
| 4 | **Runtime Exfiltration** | Post-deployment outbound calls harvest tokens, keys, and user data invisibly | Expensive enterprise SIEM only |

**KRONOS CORE solves all four in a single deployable microservice.**

---

## Why This Matters Now

- Global AI coding tool adoption is accelerating — 14M+ developers expected by 2026
- Supply chain attacks via npm rose 700% between 2020–2024 (Sonatype State of the Software Supply Chain)
- Prompt injection and insecure AI output are cited in OWASP Top 10 for LLMs (2025)
- No product currently combines AI prompt hardening + static package audit + runtime sandboxing in one API
- Enterprises have compliance requirements but no tooling that generates AI-specific security evidence

---

## Solution

KRONOS CORE operates in four sequential security layers. Each layer gates the next.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Developer Intent  →  Raw project objective in plain English             │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │
               ┌───────────────▼───────────────┐
               │   LAYER 1: Blueprint Engine    │  Converts objective into hardened
               │   POST /api/v1/blueprint       │  Claude execution prompt with 12
               │                                │  non-negotiable security standards
               └───────────────┬───────────────┘
                               │
               ┌───────────────▼───────────────┐
               │   LAYER 2: NPM Auditor         │  Allowlist-first scanning.
               │   POST /api/v1/audit           │  Fuzzy typosquat detection.
               │                                │  Forbidden package enforcement.
               └───────────────┬───────────────┘
                               │
               ┌───────────────▼───────────────┐
               │   LAYER 3: Sandbox Inspector   │  Live process + network + fs
               │   GET  /api/v1/sandbox         │  inspection. Blocks exfiltration
               │                                │  indicators. Demo mode included.
               └───────────────┬───────────────┘
                               │
               ┌───────────────▼───────────────┐
               │   LAYER 4: Security Scorer     │  6-dimension composite score.
               │   POST /api/v1/security/score  │  0–100. Executive summary.
               │                                │  Enterprise readiness verdict.
               └───────────────┬───────────────┘
                               │
                     ✓ Deploy Gate — Go / No-Go
```

---

## Core Features

### Blueprint Engine
- Accepts a plain-English project objective
- Returns a complete Claude execution blueprint including:
  - Context-aware directory architecture (fintech projects auto-add `/src/audit/`)
  - 12 non-negotiable secure coding standards (validation, parameterised queries, secrets management, CORS, rate limiting, logging)
  - Approved and forbidden package lists with audit command
  - Static audit + dynamic sandbox testing instructions
  - 12-item deployment checklist, 10-item production readiness checklist
  - Risk score across 4 sub-dimensions
  - Copy-paste-ready hardened Claude execution prompt

### Static NPM Audit

**Allowlist-first model:** Every package not on the KRONOS trusted list is flagged. The trusted list covers 50+ commonly used, maintained packages.

**Typosquat detection:** Uses Python's `difflib.SequenceMatcher` to compute similarity between submitted package names and every trusted package. Any package with ≥ 80% similarity to a trusted name — but not equal to it — is flagged as `TYPOSQUAT`.

**Examples caught:**
| Submitted | Risk | Trusted Alternative |
|-----------|------|---------------------|
| `expresss` | TYPOSQUAT | `express` |
| `lodahs` | DANGEROUS | `lodash` |
| `crossenv` | DANGEROUS | `cross-env` |
| `event-stream` | DANGEROUS | — (supply chain attack, 2018) |
| `colors.js` | DANGEROUS | `chalk` (author sabotaged, 2022) |
| `faker.js` | DANGEROUS | `@faker-js/faker` |

**Risk levels returned:** `SAFE · UNKNOWN · SUSPICIOUS · DEPRECATED · TYPOSQUAT · DANGEROUS · PHANTOM`

### Dynamic Behavioural Sandboxing

Uses Python `psutil` to inspect the live runtime environment:

- **Process inspection:** Counts all running processes, flags high-CPU processes, detects suspicious process names (`curl`, `wget`, `nc`, `ncat`, `nmap`, crypto miners)
- **Network inspection:** Enumerates all open sockets, checks outbound destination IPs against known suspicious ranges (C2 infrastructure, known malicious ASNs)
- **Filesystem inspection:** Checks whether sensitive system paths (`/etc`, `/usr`, `/bin`) are writable
- **Demo mode:** Simulates three blocked attack patterns:
  1. Outbound connection to `185.220.101.0:4444` (Tor exit node / known C2 range)
  2. Write attempt to `/etc/hosts`
  3. Subprocess spawn bypass attempt
- **Verdict:** `CLEAN · SUSPICIOUS · BLOCKED`

### Enterprise Security Score

Six dimensions, each scored 0–20, normalised to 0–100:

| Dimension | What It Measures |
|-----------|-----------------|
| Prompt Safety | Blueprint generated, secure execution constraints enforced |
| Package Safety | Ratio of flagged vs. audited packages |
| Runtime Isolation | Sandbox inspection result + Docker hardening status |
| Data Exfiltration Protection | Network scan results + auth layer presence |
| Deployment Hardening | Container config, TLS, input validation |
| Production Readiness | Auth, TLS, blueprint — all three present |

Returns: total score, risk level (`LOW / MEDIUM / HIGH / CRITICAL`), per-category findings, fix recommendations, executive summary, enterprise readiness boolean.

### Enterprise Report

Generates a boardroom-ready compliance document including:
- Executive summary
- Full capability list
- Compliance alignment: OWASP Top 10, CIS Docker Benchmark, NIST SP 800-53, ISO 27001 A.14, SOC 2 Type II, PCI-DSS
- Integration options (GitHub Actions, GitLab CI, Jenkins, Kubernetes)
- Deployment models (self-hosted, cloud, on-premises)
- Pricing model tiers
- Support model description

---

## Architecture Overview

```
kronos-core/
├── app/
│   ├── main.py                     FastAPI app — CORS, rate-limit, security headers, routers
│   ├── config.py                   Pydantic Settings — env-driven, no hard-coded secrets
│   ├── middleware/
│   │   ├── security_headers.py     Path-aware CSP: strict for API, relaxed for /docs
│   │   └── rate_limiter.py         slowapi — 60 req/min default per IP
│   ├── models/                     Pydantic v2 request/response schemas
│   ├── services/
│   │   ├── blueprint_engine.py     Blueprint generation logic
│   │   ├── npm_auditor.py          Allowlist + fuzzy typosquat + forbidden detection
│   │   ├── sandbox_inspector.py    psutil process/network/fs inspection
│   │   ├── security_scorer.py      6-dimension normalised scoring
│   │   └── demo_generator.py       Competition pitch + enterprise report
│   └── routers/                    One router per endpoint group
├── frontend/
│   ├── app/                        Next.js App Router pages
│   ├── components/                 Navbar, StatusBadge, CopyButton
│   └── lib/api.ts                  Typed fetch client with error handling
├── tests/                          50 pytest tests — all passing
├── pitch/                          Competition and sales materials
├── Dockerfile                      Multi-stage, non-root UID 10001
├── docker-compose.yml              cap_drop ALL, no-new-privileges, read-only fs
└── requirements.txt
```

---

## Backend API Endpoints

| Method | Endpoint | Rate Limit | Description |
|--------|----------|-----------|-------------|
| `GET` | `/api/v1/health` | 60/min | Service health check |
| `GET` | `/api/v1/` | 60/min | Product info + endpoint map |
| `POST` | `/api/v1/blueprint` | 20/min | Generate secure execution blueprint |
| `POST` | `/api/v1/audit` | 30/min | Static npm package security audit |
| `GET` | `/api/v1/sandbox` | 15/min | Runtime behavioural sandbox inspection |
| `POST` | `/api/v1/security/score` | 20/min | Compute 6-dimension security score |
| `GET` | `/api/v1/demo` | 30/min | Competition/investor pitch response |
| `GET` | `/api/v1/enterprise/report` | 20/min | Enterprise readiness + compliance report |
| `GET` | `/docs` | — | Swagger UI (pinned CDN, path-aware CSP) |
| `GET` | `/redoc` | — | ReDoc API documentation |

---

## Frontend Pages

| Route | Description |
|-------|-------------|
| `/` | Landing — hero, 4-risk problem, architecture flow, customers, CTA |
| `/dashboard` | Live health, security score bars, sandbox verdict, audit demo, endpoint status |
| `/blueprint` | Objective input → full blueprint with Claude prompt, directory plan, package policy |
| `/audit` | Package list → per-package risk badges, typosquat detection, recommendations |
| `/sandbox` | One-click inspection → blocked actions, process/network/fs metrics |
| `/enterprise` | Boardroom report — compliance, pricing, integration, support |

---

## Security Model

| Control | Implementation |
|---------|---------------|
| Input validation | Pydantic v2 on every endpoint — schema-enforced at boundary |
| Rate limiting | slowapi — 60 req/min default, per-endpoint overrides |
| CORS | Explicit allowlist — no wildcard `*` |
| Content Security Policy | Path-aware: `script-src 'none'` for API, CDN-allowed for `/docs` |
| Security headers | HSTS, X-Content-Type-Options, X-Frame-Options DENY, Referrer-Policy |
| Secrets | Environment variables only — never committed |
| Logging | structlog JSON — PII, tokens, and passwords explicitly excluded |
| Container | Non-root UID 10001, `cap_drop ALL`, `no-new-privileges`, read-only filesystem |
| Error handling | Generic client messages — full error + correlation ID logged server-side |

---

## Local Setup

### Prerequisites
- Python 3.10+ (tested on 3.12 and 3.14)
- Node.js 18+ (tested on 22)
- pip, npm

### Backend

```bash
# Navigate to project root
cd kronos-core

# Install Python dependencies
pip install -r requirements.txt

# Copy environment config
cp .env.example .env

# Start backend
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# API is live at:
#   http://127.0.0.1:8000/api/v1/health
#   http://127.0.0.1:8000/docs
```

### Frontend

```bash
# Navigate to frontend
cd kronos-core/frontend

# Install dependencies
npm install

# Start frontend (requires backend running)
npm run dev

# Dashboard at: http://localhost:3000
```

---

## Testing

```bash
# From project root
cd kronos-core

# Run all 50 tests
pytest tests/ -v

# Expected output:
# 50 passed, 0 failed
```

Test coverage:
- `test_health.py` — health endpoint, security headers, 404 format
- `test_blueprint.py` — generation, fields, ID format, package policy, fintech directory injection
- `test_audit.py` — safe packages, typosquat detection, forbidden packages, empty list rejection
- `test_sandbox.py` — verdict, demo mode, blocked actions, process/network/fs structure
- `test_security_score.py` — scoring, risk levels, enterprise readiness, category breakdown
- `test_demo.py` — competition pitch, enterprise report, compliance alignment
- `test_history.py` — history endpoints, demo mode without Supabase
- `test_pdf_export.py` — PDF generation, content-type, %PDF header validation
- `test_billing.py` — billing status, plans, checkout session demo mode, webhook

---

## Production Deployment

See [`docs/PRODUCTION_DEPLOYMENT.md`](docs/PRODUCTION_DEPLOYMENT.md) for full options:
- **Render** — push to GitHub, point at Dockerfile, done in minutes
- **Railway** — `railway up`, set env vars, live
- **VPS + Docker Compose** — full control, nginx reverse proxy included
- **Vercel** (frontend) + Render (backend) — recommended split

Pre-flight: work through [`docs/PRODUCTION_CHECKLIST.md`](docs/PRODUCTION_CHECKLIST.md) before going live.

Smoke test: `pwsh scripts/production_smoke_test.ps1`

---

## CI/CD

GitHub Actions CI runs on every push and pull request to `main`:
- Python 3.12 backend test suite (`pytest -q`)
- Next.js 22 frontend build (`npm run build`)

No secrets required. No automatic deploys.

See [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

---

## Docker Deployment

```bash
# From project root

# Build image
docker build -t kronos-core:1.0.0 .

# Run with full hardening
docker run -d \
  --name kronos-core \
  -p 8000:8000 \
  --read-only \
  --tmpfs /tmp:size=64m \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  -e SECRET_KEY=your-secret-key-min-32-chars \
  -e ALLOWED_ORIGINS=https://yourdomain.com \
  kronos-core:1.0.0

# OR use Docker Compose (recommended)
export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
docker compose up -d

# Verify
curl http://localhost:8000/api/v1/health
```

Docker security profile:
- Non-root user (UID 10001)
- `cap_drop: ALL`
- `security_opt: no-new-privileges`
- `read_only: true` filesystem
- `tmpfs` for `/tmp`
- CPU and memory limits
- Health check wired to `/api/v1/health`

---

## Demo Flow

*Complete live demo in under 3 minutes.*

```bash
# 1. Confirm backend is live
curl http://127.0.0.1:8000/api/v1/health

# 2. Generate a blueprint
curl -X POST http://127.0.0.1:8000/api/v1/blueprint \
  -H "Content-Type: application/json" \
  -d '{"objective":"Build a fintech payment API with JWT auth","sensitivity_level":"CRITICAL"}'

# 3. Audit packages — watch typosquats get caught
curl -X POST http://127.0.0.1:8000/api/v1/audit \
  -H "Content-Type: application/json" \
  -d '{"packages":["express","expresss","event-stream","helmet","lodahs","jsonwebtoken"]}'

# 4. Run sandbox inspection
curl "http://127.0.0.1:8000/api/v1/sandbox?demo=true"

# 5. Get security score
curl -X POST http://127.0.0.1:8000/api/v1/security/score \
  -H "Content-Type: application/json" \
  -d '{"packages_audited":6,"packages_flagged":0,"sandbox_passed":true,"blueprint_generated":true,"docker_hardened":true,"input_validation":true,"auth_implemented":true,"tls_enabled":true}'

# 6. Pull competition pitch
curl http://127.0.0.1:8000/api/v1/demo

# 7. Pull enterprise report
curl http://127.0.0.1:8000/api/v1/enterprise/report

# Frontend demo:
# http://localhost:3000          → Landing page
# http://localhost:3000/dashboard → Live security dashboard
# http://localhost:3000/audit    → Live typosquat detection
# http://localhost:3000/sandbox  → Live sandbox with blocked actions
# http://localhost:3000/enterprise → Boardroom-ready report
```

---

## Competition Pitch

> *"Every company using AI coding tools has a security blind spot. KRONOS CORE closes it — before the first line of code is written, before the first package is installed, before the first container is deployed."*

**Why KRONOS CORE wins competitions:**

| Judging Criterion | KRONOS CORE Evidence |
|-------------------|---------------------|
| **Innovation** | First product combining AI prompt hardening + allowlist npm audit + psutil runtime sandbox + enterprise scoring in one API |
| **Technical Execution** | FastAPI, Pydantic v2, slowapi, structlog, psutil, 50 tests, multi-stage Docker, Next.js 16 frontend |
| **Business Viability** | Segmented customers, three pricing tiers, compliance alignment, Docker-deployable in 5 min |
| **Presentation** | Live API + interactive frontend + Swagger docs + boardroom enterprise report |
| **Market Impact** | Addresses 14M+ AI developers, supply chain security, AI governance gap |

**Key numbers to know:**
- **50** passing tests · **8** API endpoints · **6** frontend pages
- **4** security layers · **6** scoring dimensions · **0–100** score
- **5 minutes** to deploy via Docker · **3 minutes** for full live demo

---

## Institution Sales Pitch

**Target buyers:** Software companies, banks, government digital teams, universities, cybersecurity consultancies.

**Opening line:**  
*"Your team is using AI coding tools. KRONOS CORE is the compliance layer that proves your AI-generated code was reviewed before it reached production."*

**What you're buying:**
1. A self-hosted API that your CI/CD calls before any AI-assisted PR is merged
2. Automated npm audit reports for regulatory evidence
3. Runtime sandbox inspection reports for security sign-off
4. Enterprise security score PDF-exportable reports for auditors

**Pilot offer:** Deploy via Docker in your environment in under 30 minutes. No data leaves your infrastructure.

---

## Target Customers

| Segment | Pain Point | Value Delivered |
|---------|-----------|-----------------|
| AI Startups | Moving fast with LLMs, no security governance | Enterprise-grade posture without a security team |
| Software Companies | AI tools generate insecure code that passes review | Pre-harden before development begins |
| Banks & FinTech | Regulatory audit trail for AI-assisted development | Compliance evidence report, PCI-DSS blueprint support |
| Gov Digital Teams | Cannot deploy AI code without documented review | Structured security report for procurement approval |
| Universities | Students submit AI code with hidden vulnerabilities | Blueprint-enforced standards from day one |
| Cybersecurity Firms | Clients adopting AI tools with no governance | White-label advisory offering |

---

## Pricing Concept

| Tier | Price | Included |
|------|-------|----------|
| **Starter** | $299/month | 5 developers, 500 blueprints/month, unlimited audits |
| **Team** | $999/month | 25 developers, unlimited blueprints, SIEM export, SSO |
| **Enterprise** | Custom | Unlimited users, on-premises, SLA, dedicated support, quarterly security review |

---

## Roadmap

| Phase | Feature | Timeline |
|-------|---------|----------|
| v1.1 | Claude API integration for live blueprint refinement | Q3 2026 |
| v1.2 | VS Code + JetBrains extension | Q4 2026 |
| v2.0 | GitHub Actions + GitLab CI native integration | Q1 2027 |
| v2.1 | SOC 2 Type II alignment module | Q2 2027 |
| v3.0 | Python pip, Go modules, Rust cargo audit | Q3 2027 |
| v3.1 | Multi-tenant SaaS with team dashboards | Q4 2027 |

---

## Founder Notes

**For competition judges:** Start with the live audit demo — the real-time typosquat catch (`expresss` vs `express`) is the visual hook. Then show the sandbox blocking a simulated C2 connection. Close with the 0–100 security score. Every endpoint is live, every test passes, and the full system deploys in 5 minutes with `docker compose up`.

**For institutional buyers:** Lead with compliance. Show the enterprise report endpoint — it maps directly to OWASP, NIST SP 800-53, ISO 27001, SOC 2, and PCI-DSS. Offer a self-hosted Docker pilot with zero data egress. Present the security score as automated evidence for your audit team.

**For investors:** The moat is the combination. No competitor addresses all four AI development risks (prompt safety, package safety, runtime isolation, exfiltration prevention) in a single API-first microservice. The compliance evidence angle unlocks government and banking procurement at $2k+/month enterprise contracts.

---

*KRONOS CORE v1.0 — Secure by Design. Auditable by Default. Deployable in Minutes.*

**Contact:** Fokrul Islam · fokrulanthro16@gmail.com · +8801732457882
