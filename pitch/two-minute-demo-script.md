# KRONOS CORE — Two-Minute Live Demo Script

---

## Pre-Demo Setup (before audience arrives)

- [ ] Backend running: `uvicorn app.main:app --host 127.0.0.1 --port 8000`
- [ ] Frontend running: `cd frontend && npm run dev`
- [ ] Browser tabs open: `http://localhost:3000` and `http://127.0.0.1:8000/docs`
- [ ] Terminal visible with backend logs streaming
- [ ] Font size bumped to 18px for readability

---

## Script

**[0:00 — Open the Home page at localhost:3000]**

> "This is KRONOS CORE. An AI security gateway for engineering teams.
> You can see the four risks it solves right here on the landing page —
> unsafe prompts, typosquatted packages, phantom packages, and runtime exfiltration.
> One product. Four layers of protection."

---

**[0:20 — Navigate to /dashboard]**

> "The dashboard hits the live backend the moment it loads.
> You can see the service is healthy, the security score is 82 out of 100,
> and the sandbox verdict is CLEAN.
> Every card here pulls real data from the API — nothing is mocked."

---

**[0:40 — Navigate to /audit]**

> "This is the NPM audit page. Watch what happens when I submit this package list."

*Click 'Load example packages' to fill in: `express, expresss, event-stream, helmet, lodahs, jsonwebtoken`*

*Click 'Run KRONOS Audit'*

> "Look at the results.
> `express` — SAFE. Trusted allowlist.
> `expresss` — TYPOSQUAT. One extra 's'. KRONOS catches it with fuzzy similarity matching.
> `event-stream` — DANGEROUS. This was used in a real supply chain attack in 2018.
> `lodahs` — DANGEROUS. A misspelling of lodash designed to harvest credentials.
>
> This is the kind of mistake that ends companies. KRONOS catches it before the install."

---

**[1:10 — Navigate to /sandbox]**

> "Now the sandbox. This inspects what's actually running."

*Click 'Run Sandbox Inspection'*

> "The sandbox scanned every running process, every open network connection, every sensitive file path.
> Verdict: CLEAN.
> But look at the blocked actions — in demo mode, KRONOS simulated a connection attempt to a known
> command-and-control IP range, and blocked it.
> In production, this runs as a pre-deployment gate."

---

**[1:35 — Navigate to /enterprise]**

> "Finally, the enterprise report. This is what you send to your legal team or an auditor.
> Compliance alignment with OWASP, NIST, ISO 27001, SOC 2, and PCI-DSS.
> Integration options. Deployment models. Pricing.
> All generated automatically. No manual documentation required."

---

**[1:50 — Switch to browser tab with http://127.0.0.1:8000/docs]**

> "And for the technical audience — here's the full Swagger UI.
> Every endpoint is live, documented, and testable right here.
> Eight endpoints. Rate-limited. CORS-locked. Security-headered."

---

**[2:00 — Close]**

> "That's KRONOS CORE. Four security layers. Eight endpoints. Fifty tests passing.
> Docker-deployable in five minutes. Self-hosted.
> The security layer your AI pipeline is missing."

---

## Fallback if internet is slow

If the frontend takes time to load, open the backend directly:
```
curl http://127.0.0.1:8000/api/v1/health
curl -X POST http://127.0.0.1:8000/api/v1/audit \
  -H "Content-Type: application/json" \
  -d '{"packages":["express","expresss","event-stream"]}'
```
The terminal output is clear and still makes the point.
