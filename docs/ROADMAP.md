# KRONOS CORE — Product Roadmap

This document describes the planned evolution of KRONOS CORE from its current v1.0 local microservice into a full multi-tenant SaaS platform.

---

## Current State: v1.0 (Released)

- ✅ FastAPI backend — 8 endpoints, rate-limited, CORS-locked, Docker-hardened
- ✅ Blueprint Engine — converts raw objectives to secure Claude execution prompts
- ✅ NPM Auditor — allowlist + fuzzy typosquat + forbidden package detection
- ✅ Sandbox Inspector — psutil process/network/filesystem inspection
- ✅ Security Scorer — 6-dimension composite 0–100 score
- ✅ Competition Demo & Enterprise Report endpoints
- ✅ Next.js frontend — 6 pages, live API integration
- ✅ Swagger UI + ReDoc documentation
- ✅ Docker Compose deployment with full hardening
- ✅ 50 tests passing, 0 failures
- ✅ Pitch materials, deployment docs, security checklist

---

## v1.1 — AI Integration (Q3 2026)

**Goal:** Connect KRONOS CORE to the Claude API for dynamic, context-aware blueprints.

### Features
- [ ] Claude API integration for live blueprint refinement
  - User submits objective → KRONOS generates base blueprint → Claude refines with project-specific context
  - Streaming response support for real-time blueprint generation
- [ ] Prompt injection detection layer
  - Scan submitted objectives for prompt injection patterns before forwarding to Claude
  - Flag and sanitise suspicious inputs
- [ ] Blueprint versioning
  - Store multiple blueprint revisions for the same objective
  - Diff view between versions
- [ ] Tech-stack-aware blueprints
  - Python/FastAPI stack generates Python-specific security standards
  - Go stack generates Go-specific recommendations

**Infrastructure:** Add `ANTHROPIC_API_KEY` environment variable. Claude API calls are optional — core functionality remains fully offline.

---

## v1.2 — IDE Extensions (Q4 2026)

**Goal:** Bring KRONOS CORE into the developer's daily workflow via IDE plugins.

### Features
- [ ] **VS Code extension**
  - Right-click menu: "Generate KRONOS Blueprint" on any file
  - Inline warnings for forbidden package names detected in `package.json`
  - Status bar showing current project security score
- [ ] **JetBrains plugin**
  - Same capability for IntelliJ IDEA, WebStorm, PyCharm
- [ ] **CLI tool** (`kronos` command)
  - `kronos blueprint "Build a payment API"` → outputs blueprint to terminal
  - `kronos audit package.json` → audits all dependencies in a package file
  - `kronos score` → computes security score for current directory
  - Installable via `pip install kronos-core-cli` or `npm install -g kronos-cli`

---

## v2.0 — CI/CD Native Integration (Q1 2027)

**Goal:** KRONOS CORE becomes a first-class gate in automated pipelines, not just a manual tool.

### Features
- [ ] **GitHub App**
  - Installs on any GitHub repository
  - Automatically audits `package.json` on every PR
  - Posts inline PR comments with audit findings
  - Blocks merge if DANGEROUS or TYPOSQUAT packages detected
  - Generates security score badge for README
- [ ] **GitLab CI component**
  - Native `.gitlab-ci.yml` component for one-line integration
- [ ] **GitHub Actions marketplace action**
  - `uses: kronos-core/audit-action@v1`
- [ ] **Jenkins shared library**
  - `kronosAudit()` pipeline step
- [ ] **Pre-commit hook**
  - `kronos-audit` runs before every git commit, blocking forbidden packages

---

## v2.1 — User Authentication & Workspaces (Q2 2027)

**Goal:** Transform KRONOS CORE from a single-user tool into a team product.

### Features
- [ ] User authentication (see `docs/AUTH_PLAN.md` for provider options)
- [ ] Organisation workspaces
  - Each organisation has isolated audit history and custom allowlists
  - Invite team members by email
  - Role-based access: Admin, Developer, Viewer
- [ ] Custom allowlist management
  - Organisation admins define their approved package list via UI
  - Custom forbidden packages per organisation
- [ ] Audit history
  - Every audit, blueprint, sandbox inspection, and score stored in PostgreSQL
  - Searchable by date, package name, risk level
  - Filter by team member
- [ ] Saved blueprints
  - Blueprint templates saved and reused across projects
  - Share blueprints with team
- [ ] Notification system
  - Email alerts when a high-risk package is detected in any team audit
  - Slack/webhook integration

**Infrastructure additions:**
- PostgreSQL database (managed: Supabase or Railway)
- Redis for session management and rate-limit state
- Background job queue (for async blueprint generation with Claude API)

---

## v2.2 — PDF Export & Reporting (Q2 2027)

**Goal:** Make the enterprise report truly boardroom-ready with downloadable PDF output.

### Features
- [ ] **PDF export** for enterprise reports
  - Uses `weasyprint` or `reportlab` server-side
  - Branded with KRONOS CORE header
  - Includes all compliance alignment tables
  - Timestamped and signed with report ID
- [ ] **Email delivery**
  - Send security score report to specified email addresses
  - Scheduled weekly summary email: "Your team ran 12 audits this week. 3 packages were blocked."
- [ ] **Executive dashboard**
  - Organisation-level view: total audits, blocked packages over time, score trend
  - Exportable as CSV or PDF for quarterly security reviews
- [ ] **Audit certificate**
  - One-page compliance certificate: "KRONOS CORE Security Review — [Project Name] — [Score] — [Date]"

---

## v2.3 — SOC 2 Type II Module (Q2 2027)

**Goal:** Make KRONOS CORE a formal part of a company's SOC 2 evidence collection.

### Features
- [ ] Structured evidence export matching SOC 2 control identifiers
- [ ] Change log: track who ran which audit and when, with immutable timestamps
- [ ] Retention policy: configurable audit log retention (30 / 90 / 365 days)
- [ ] Auditor export: single ZIP with all evidence for a specified date range
- [ ] Integration with Vanta, Drata, Secureframe (evidence sync via API)

---

## v3.0 — Multi-Language Support (Q3 2027)

**Goal:** Expand beyond npm to cover every major package ecosystem.

### Features
- [ ] **Python pip audit**
  - Allowlist-first model for PyPI packages
  - Typosquat detection (numpy → nump, requests → requestes)
  - Known malicious packages (e.g., `ctx`, `discord.py-self`)
- [ ] **Go modules audit**
  - Check `go.mod` imports against trusted module list
  - Flag packages with no version tags or abandoned repositories
- [ ] **Rust cargo audit**
  - Integrate with `cargo-audit` output parsing
  - Custom forbidden crate list
- [ ] **Java Maven / Gradle**
  - Dependency audit via coordinate comparison
- [ ] **Universal package.json / requirements.txt scanner**
  - Single endpoint accepts any dependency file format
  - Returns normalised risk report across languages

---

## v3.1 — GitHub Repository Scanner (Q3 2027)

**Goal:** Give KRONOS CORE the ability to audit an entire repository, not just a package list.

### Features
- [ ] Accept a GitHub repository URL
- [ ] Clone (or use GitHub API) to scan all dependency files
- [ ] Detect hard-coded secrets using pattern matching (API keys, tokens, private keys)
- [ ] Identify outdated dependencies with available security patches
- [ ] Detect Dockerfile misconfigurations (running as root, missing health check, exposed secrets)
- [ ] Return a unified repository security report

---

## v3.2 — Multi-Tenant SaaS (Q4 2027)

**Goal:** Full SaaS platform with self-serve signup, billing, and usage metering.

### Features
- [ ] **Stripe subscription integration**
  - Starter / Team / Enterprise tiers
  - Usage-based billing for blueprint generations
  - Free tier: 10 audits/month, 5 blueprints/month
- [ ] **Self-serve onboarding**
  - Sign up → verify email → create organisation → connect GitHub → first audit in < 5 minutes
- [ ] **Admin dashboard**
  - Usage metrics per organisation
  - Subscription management
  - Support ticket integration
- [ ] **White-label option**
  - Reseller partners can deploy KRONOS CORE with custom branding
  - API key management for reseller billing passthrough
- [ ] **SLA tiers**
  - Starter: best-effort
  - Team: 99.9% uptime SLA
  - Enterprise: 99.95% + dedicated support Slack channel

---

## Infrastructure Evolution

| Version | Database | Auth | Cache | Jobs | Deployment |
|---------|---------|------|-------|------|-----------|
| v1.0 | None (stateless) | None | None | None | Docker single-container |
| v2.1 | PostgreSQL (Supabase) | Supabase Auth / Clerk | Redis | None | Docker Compose + nginx |
| v2.2 | PostgreSQL + S3 | Supabase Auth | Redis | Celery/ARQ | Kubernetes or Railway |
| v3.2 | PostgreSQL + S3 | Supabase Auth + SSO | Redis Cluster | Celery + Flower | Kubernetes multi-region |

---

## What Will NOT Change

These core properties are invariant across all versions:

1. **Self-hosted option always available** — enterprise customers can always run on-premises
2. **Stateless API remains functional** — every endpoint works without authentication (for self-hosted)
3. **Zero external dependency for core audit** — allowlist + typosquat detection runs fully offline
4. **Non-root Docker** — the hardened container model is permanent
5. **Open audit log** — no obfuscation of what KRONOS CORE does or why it flags a package
