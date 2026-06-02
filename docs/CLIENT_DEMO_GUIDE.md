# KRONOS CORE — Client Demo Guide

This guide is for the product owner to use during any live client or institutional demonstration.
Read the "What to say" sections aloud. The commands are ready to copy-paste.

---

## Before the Demo (10 minutes ahead)

### Start the backend

```bash
cd kronos-core

# If using a virtual environment
source .venv/bin/activate       # macOS/Linux
# or: .venv\Scripts\activate    # Windows

uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Keep this terminal visible. The streaming JSON logs show the system is alive.

### Start the frontend

```bash
# New terminal
cd kronos-core/frontend
npm run dev
```

### Confirm both are working

```bash
# Quick sanity check
curl http://127.0.0.1:8000/api/v1/health
# → {"status":"healthy","service":"KRONOS CORE",...}
```

Open `http://localhost:3000` in your browser. The home page should load with the dark cyber theme.

### Open these tabs in order

1. `http://localhost:3000` — Home
2. `http://localhost:3000/dashboard` — Dashboard
3. `http://localhost:3000/audit` — NPM Audit
4. `http://localhost:3000/sandbox` — Sandbox
5. `http://localhost:3000/enterprise` — Enterprise Report
6. `http://localhost:3000/blueprint` — Blueprint
7. `http://127.0.0.1:8000/docs` — API Docs

---

## The Problem KRONOS CORE Solves

**Use this framing to open every client conversation:**

> "Your team is using AI coding tools. That's good — they accelerate development significantly.
> But AI coding tools introduce four security risks that nothing in your current stack addresses:
>
> One: The AI generates insecure code because no one hardened the prompt before it ran.
>
> Two: The AI recommends or developers mistype package names — and malicious packages with
> near-identical names are waiting on npm, harvesting credentials the moment they're installed.
>
> Three: Language models sometimes hallucinate package names that don't exist — or that
> malicious actors registered specifically to catch those hallucinations.
>
> Four: AI-generated code can contain hidden network calls that exfiltrate data
> after deployment, silently, in production.
>
> KRONOS CORE is the layer that sits between your team's intent and your production environment
> and closes all four gaps."

---

## Page-by-Page Demo Script

### Page 1: Home — `localhost:3000`

**What to show:**
- The hero section with the product name and tagline
- The four risk cards (01–04)
- The architecture flow diagram showing the four layers
- The stats bar: 4 layers / 8 endpoints / 6 dimensions / 50 tests

**What to say:**
> "This is the product overview. You can see the four problems it solves listed right here.
> The architecture shows how they're solved in sequence — each layer gates the next.
> No layer can be bypassed. Blueprint runs first, then audit, then sandbox, then scoring."

---

### Page 2: Dashboard — `localhost:3000/dashboard`

**What to show:**
- Health card showing HEALTHY (green badge)
- Security score card with the number and six coloured bars
- Sandbox verdict card (CLEAN)
- The API endpoint status list at the bottom

**What to say:**
> "The dashboard pulls live data from the backend on load. Nothing here is static.
> The security score is 82 out of 100, computed dynamically from real inputs.
> The six bars are the six security dimensions. The sandbox verdict is CLEAN —
> meaning no exfiltration indicators were detected in the current runtime.
> Every endpoint in this list is live and responding right now."

---

### Page 3: NPM Audit — `localhost:3000/audit`

**What to show:**
1. Click "Load example packages" to fill the input
2. Click "Run KRONOS Audit"
3. Point to `expresss` → TYPOSQUAT (red)
4. Point to `event-stream` → DANGEROUS (red)
5. Point to `express` → SAFE (green)

**How to explain the NPM audit:**
> "The NPM auditor uses an allowlist-first model. Every package not on our trusted list gets flagged.
> But the interesting part is typosquat detection.
>
> `expresss` — with three s's — is 91% similar to `express`. KRONOS catches that with
> fuzzy string matching and flags it as a TYPOSQUAT before npm install ever runs.
>
> `event-stream` was used in a real supply chain attack in 2018. An attacker injected malicious
> code into it and it harvested cryptocurrency wallet credentials from thousands of developers.
> KRONOS blocks it permanently.
>
> This entire analysis runs in milliseconds. No network requests. No npm install.
> Pure static analysis against our intelligence database."

---

### Page 4: Sandbox — `localhost:3000/sandbox`

**What to show:**
1. Click "Run Sandbox Inspection"
2. Show the CLEAN verdict
3. Point to the blocked actions panel — the red items showing simulated C2 connection blocked

**How to explain sandboxing:**
> "The sandbox inspects what's actually happening in the runtime environment right now.
>
> It checks every running process for suspicious names — things like curl, wget, netcat,
> or crypto miners that shouldn't be running in a production backend.
>
> It checks every open network connection and compares destination IPs against known
> command-and-control IP ranges.
>
> It checks whether sensitive filesystem paths like /etc or /usr are writable.
>
> In demo mode, it also simulates an attack: it tests whether a connection attempt to
> 185.220.101.0 port 4444 — a known Tor exit node used as C2 infrastructure —
> would be detected and blocked. It is. You can see it in the blocked actions panel.
>
> The verdict: CLEAN. This runtime is safe to deploy."

---

### Page 5: Enterprise Report — `localhost:3000/enterprise`

**How to explain the enterprise report:**
> "This is what you show your legal team or your auditors.
>
> KRONOS CORE generates a structured compliance report that maps its security controls
> to five major frameworks: OWASP Top 10, NIST SP 800-53, ISO 27001 Annex A.14,
> SOC 2 Type II, and PCI-DSS.
>
> Each compliance item tells the auditor exactly which KRONOS control addresses it.
>
> The report also includes integration options — GitHub Actions, GitLab CI, Jenkins —
> and deployment models, so your infrastructure team knows exactly how to operationalise it.
>
> This document is generated automatically by the API. No manual documentation required."

---

### Page 6: Blueprint Generator — `localhost:3000/blueprint`

**What to show:**
1. Click "Example 1" (the fintech example)
2. Click "Generate Secure Claude Blueprint"
3. Scroll through: risk score, directory architecture, package policy, Claude prompt

**What to say:**
> "The blueprint engine is the first layer. Before your developer opens Claude Code,
> they submit their project objective here.
>
> The engine returns a complete execution blueprint:
> a directory architecture that's already structured for security,
> 12 security standards that Claude must enforce,
> an approved package list and forbidden package list,
> and a ready-to-paste Claude execution prompt.
>
> The developer copies that prompt into Claude. The AI executes within those constraints.
> It can't hallucinate a forbidden package. It can't generate code without input validation.
> The guardrails are in the prompt before anything else runs."

---

### Page 7: API Docs — `127.0.0.1:8000/docs`

**What to say:**
> "For your engineering team — the full API documentation.
> Every endpoint is live and testable from this interface.
> Eight endpoints, all rate-limited, all documented with request and response schemas.
> Your CI/CD pipeline integrates with this via standard HTTP calls."

---

## Closing the Demo

**For software companies:**
> "KRONOS CORE integrates into your existing CI/CD in one afternoon.
> It's a single HTTP call per step — one for the blueprint before development,
> one for the audit before install, one for the sandbox before deployment.
> The reports it generates satisfy your security review process automatically."

**For banks and compliance-driven organisations:**
> "The enterprise report maps directly to your existing compliance frameworks.
> Your audit team gets documented evidence that every AI-assisted feature went through
> a security review process before it reached production."

**For universities:**
> "Students submit their project objective to KRONOS CORE before writing code.
> They receive a security blueprint they must follow. Every submission has a documented
> security posture before assessment. You've built secure coding into the curriculum
> without changing your teaching materials."

**Universal close:**
> "KRONOS CORE is self-hosted. Your data never leaves your environment.
> It deploys with `docker compose up` in under five minutes.
> The pilot is free. Shall we schedule a deployment call?"

---

## Frequently Asked Questions from Clients

**"How is this different from npm audit?"**
> npm audit only checks packages against known CVEs. Typosquatted packages like `expresss`
> have no CVE — the attack is the name itself. KRONOS catches those. npm audit doesn't.

**"Does this need an internet connection?"**
> No. The entire core — blueprint generation, package audit, sandbox inspection, scoring —
> runs offline. The only external dependency is the Swagger UI CDN for `/docs`, which is
> optional and has a ReDoc fallback.

**"Can we integrate this with our existing CI/CD?"**
> Yes. Every capability is an HTTP POST or GET. GitHub Actions, GitLab CI, Jenkins —
> any pipeline that can make an HTTP request integrates in under 10 minutes.
> See `docs/DEPLOYMENT.md` for examples.

**"What about false positives in the audit?"**
> The audit uses an allowlist-first model. If a legitimate package isn't on our trusted list,
> it's flagged as UNKNOWN, not blocked. The developer reviews and decides. Over time, the
> allowlist expands. We can also accept custom allowlist configuration in Enterprise tier.

**"Is the sandbox safe to run in production?"**
> Yes. The sandbox inspector only **reads** system state using psutil. It never modifies
> processes, network configurations, or filesystem permissions. It's a passive observer.

**"What data does KRONOS CORE store?"**
> Nothing, by default. Every API call is stateless. No audit results, blueprint outputs,
> or sandbox reports are persisted. If you need audit history, that's a feature on the
> Enterprise roadmap backed by a database integration.
