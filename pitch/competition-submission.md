# KRONOS CORE — Competition Submission Document

*Copy-paste ready for hackathon forms, university competition portals, and accelerator applications.*

---

## Project Title

KRONOS CORE — Autonomous Security & Prompt Architecture Gateway

---

## Category

Cybersecurity / AI Safety / Developer Tooling / Enterprise Infrastructure

---

## Short Description (≤ 280 characters)

KRONOS CORE is an enterprise security gateway that converts AI prompts into hardened Claude blueprints, catches typosquatted npm packages before install, inspects runtime behaviour for exfiltration, and scores AI pipelines on a 100-point security scale.

---

## Long Description (≤ 1000 words)

KRONOS CORE solves the four security risks that every organisation using AI coding tools faces — simultaneously, in a single deployable microservice.

**The Problem**

AI coding tools like Claude Code, GitHub Copilot, and Cursor are transforming how software is built. But they introduce four security risks that existing tooling does not address together:

1. **Unsafe prompts.** AI generates insecure code when given vague objectives. No existing tool hardens the prompt before the AI sees it.

2. **Typosquatted packages.** Attackers register package names like `expresss` (one extra 's') or `lodahs` on npm, designed to match what an AI or careless developer might type. Once installed, they silently harvest credentials.

3. **Phantom packages.** Language models hallucinate. They recommend package names that don't exist — or that have been registered by malicious actors to catch exactly these hallucinations.

4. **Runtime exfiltration.** AI-generated code can contain hidden outbound connections that harvest API keys, tokens, or user data after deployment. Current detection requires expensive enterprise SIEM tooling.

**The Solution**

KRONOS CORE operates as four sequential security layers:

**Layer 1 — Blueprint Engine:** Accepts a raw project objective in plain English. Returns a structured Claude execution prompt enforcing 12 non-negotiable security standards: input validation, parameterised queries, JWT configuration, CORS allowlisting, rate limiting, structured logging, and more. The AI executes within these constraints or not at all.

**Layer 2 — NPM Auditor:** Every package name is checked against a 50+ item trusted allowlist. Unknown packages are flagged. Explicitly dangerous packages (supply chain attack history, author sabotage) are blocked. Typosquats are caught using fuzzy string similarity — `expresss` scores 91% similar to `express` and is immediately flagged. This requires zero network requests and zero npm installs.

**Layer 3 — Sandbox Inspector:** Uses Python's `psutil` library to inspect the live runtime environment — running processes, open network connections, and writable filesystem paths. Outbound connection destinations are checked against known malicious IP ranges. Any exfiltration indicator triggers a `BLOCKED` verdict.

**Layer 4 — Security Scorer:** Six dimensions scored 0–20 each, normalised to 0–100. Returns a risk level (LOW / MEDIUM / HIGH / CRITICAL), per-category findings, fix recommendations, and an executive summary aligned to OWASP, NIST SP 800-53, ISO 27001, SOC 2, and PCI-DSS.

**Technical Implementation**

- Backend: FastAPI (Python), Pydantic v2, psutil, structlog, slowapi
- Frontend: Next.js 16, React 19, TypeScript, Tailwind CSS 4
- Testing: 50 pytest tests, 0 failures
- Deployment: Docker multi-stage build, non-root user, cap_drop ALL, read-only filesystem
- Documentation: Swagger UI, full README, pitch materials, demo scripts

The backend exposes 8 API endpoints, all rate-limited, CORS-locked, with path-aware Content Security Policy headers. The frontend provides a live dashboard, audit tool, sandbox inspector, blueprint generator, and boardroom enterprise report — all pulling real data from the backend.

**Live Demo:** The full product is functional and can be demonstrated live from a single `docker compose up` command.

---

## Problem Solved

KRONOS CORE addresses the governance gap in AI-assisted software development. It provides:

1. A documented security layer that can serve as compliance evidence for ISO 27001, SOC 2, and PCI-DSS audit trails
2. The first product to combine AI prompt hardening with static package supply chain audit and live runtime inspection in one API
3. A self-hosted, data-sovereign solution that works in regulated environments where SaaS tools are blocked

---

## Innovation

**Technical innovation:**
- Fuzzy typosquat detection using sequence similarity — catches attacks that exact-match blocklists miss
- AI prompt architecture layer — the first product to harden the AI prompt before code generation, not audit the output after
- Path-aware Content Security Policy middleware — the product's own HTTP security enforces the same principles it teaches

**Business innovation:**
- Compliance evidence generation as a product feature — turns security tooling into a procurement document
- Self-hosted zero-egress model — unlocks government and banking verticals where cloud tools are blocked
- Four-layer integrated approach — replaces four separate tools with one API and one deployment

---

## Technical Stack

| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI 0.115+, Python 3.10+ |
| Data validation | Pydantic v2 |
| Runtime inspection | psutil 6+ |
| Rate limiting | slowapi |
| Logging | structlog |
| Frontend | Next.js 16, React 19, TypeScript |
| Styling | Tailwind CSS 4 |
| Icons | Lucide React |
| Testing | pytest, pytest-asyncio, httpx |
| Deployment | Docker (multi-stage), Docker Compose |
| Documentation | Swagger UI (pinned CDN), ReDoc |

---

## Social and Commercial Impact

**Commercial impact:**
- Reduces AI development risk by providing an automated pre-deployment security gate
- Generates compliance evidence that reduces audit preparation time and cost
- Enables smaller teams to meet enterprise security standards without a dedicated security engineer

**Social impact:**
- Reduces the risk of supply chain attacks reaching production systems that handle personal or financial data
- Provides university computer science departments with a tool to teach secure-by-design principles in an AI-first curriculum
- Enables government digital teams to adopt AI coding tools without compromising documented security processes

---

## Target Users

1. AI-native startups using LLMs for product development
2. Software engineering teams at companies adopting AI coding tools
3. Security engineers and compliance officers at regulated organisations
4. Computer science educators teaching AI-assisted development
5. Cybersecurity consultants advising clients on AI governance

---

## Demo Instructions

**Requirements:** Python 3.10+, Node.js 18+, pip, npm

```bash
# Clone / navigate to project
cd kronos-core

# Start backend (Terminal 1)
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000

# Start frontend (Terminal 2)
cd frontend
npm install
npm run dev

# Open in browser
# http://localhost:3000        → Full dashboard
# http://127.0.0.1:8000/docs  → API documentation
```

**Demo flow (3 minutes):**
1. `localhost:3000` — landing page shows problem + solution
2. `localhost:3000/dashboard` — live security score and sandbox verdict
3. `localhost:3000/audit` → load examples → run → see TYPOSQUAT and DANGEROUS detections
4. `localhost:3000/sandbox` → run inspection → see blocked C2 connection
5. `localhost:3000/enterprise` → view compliance alignment report
6. `127.0.0.1:8000/docs` → show full live API

---

## Future Roadmap

| Version | Feature | Timeline |
|---------|---------|----------|
| v1.1 | Claude API integration for live blueprint refinement | Q3 2026 |
| v1.2 | VS Code + JetBrains IDE extension | Q4 2026 |
| v2.0 | Native GitHub Actions / GitLab CI integration | Q1 2027 |
| v2.1 | SOC 2 Type II compliance module | Q2 2027 |
| v3.0 | Multi-language: Python pip, Go modules, Rust cargo | Q3 2027 |

---

## Creator

**Fokrul Islam**
fokrulanthro16@gmail.com
+8801732457882

---

*KRONOS CORE v1.0 — Built for companies, institutions, and competition judges who understand that AI development risk is a solved problem — if you have the right tool.*
