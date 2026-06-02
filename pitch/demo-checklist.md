# KRONOS CORE — Demo Checklist

*Run through this checklist before every competition, meeting, or demo.*

---

## 30 Minutes Before

- [ ] Laptop charged or plugged in
- [ ] Internet connection confirmed (or note which features work offline)
- [ ] Screen resolution set to 1080p or higher
- [ ] Browser font size set to 110–120% for readability
- [ ] Terminal font size set to 16–18px

---

## Start the Backend

```bash
# From project root
cd c:\Users\WALTON\kronos-core

# Install dependencies if first run
pip install -r requirements.txt

# Start the backend
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**What to say:** *"Backend is live. You can see structured JSON logs streaming here — that's psutil watching the runtime in real time."*

**Confirm it's working:**
```bash
# In a second terminal
curl http://127.0.0.1:8000/api/v1/health
```
Expected: `{"status":"healthy","service":"KRONOS CORE",...}`

---

## Start the Frontend

```bash
# In a separate terminal
cd c:\Users\WALTON\kronos-core\frontend
npm run dev
```

**Confirm it's working:** Open `http://localhost:3000` — the home page should load with the dark cyber theme.

---

## Open These Browser Tabs (in order)

1. `http://localhost:3000` — Landing page
2. `http://localhost:3000/dashboard` — Dashboard
3. `http://localhost:3000/audit` — NPM Audit
4. `http://localhost:3000/sandbox` — Sandbox
5. `http://localhost:3000/enterprise` — Enterprise Report
6. `http://localhost:3000/blueprint` — Blueprint Generator
7. `http://127.0.0.1:8000/docs` — Swagger UI

---

## Run Tests (Optional — for technical judges)

```bash
cd c:\Users\WALTON\kronos-core
pytest tests/ -v
```

**What to say:** *"50 tests. Zero failures. This is a production-grade codebase, not a prototype."*

---

## Page-by-Page Demo Guide

### Tab 1: Home — `localhost:3000`

**What to show:** The hero section ("KRONOS CORE"), the four risk cards, the architecture flow diagram.

**What to say:**
> *"This is the product landing page. You can see the four risks it solves — unsafe prompts, typosquatted packages, phantom packages, runtime exfiltration. The architecture diagram shows the four security layers that gate each other."*

---

### Tab 2: Dashboard — `localhost:3000/dashboard`

**What to show:** Health card (HEALTHY), security score with bar chart, sandbox verdict (CLEAN), endpoint status list.

**What to say:**
> *"The dashboard pulls live data from the backend on load. The security score here is computed dynamically. The six bars represent the six scoring dimensions. Every endpoint in the list is live and responding."*

---

### Tab 3: Audit — `localhost:3000/audit`

**What to show:** Click "Load example packages", then "Run KRONOS Audit". Point to `expresss` (TYPOSQUAT) and `event-stream` (DANGEROUS).

**What to say:**
> *"This is the killer feature. Watch `expresss` — one extra 's' — get flagged as a typosquat in real time. And `event-stream` — a real package used in a 2018 supply chain attack that hit the Copay Bitcoin wallet. KRONOS catches both with zero network requests. Pure static analysis."*

---

### Tab 4: Sandbox — `localhost:3000/sandbox`

**What to show:** Click "Run Sandbox Inspection". Show the verdict (CLEAN), show the blocked actions panel.

**What to say:**
> *"The sandbox inspects the actual running environment — processes, open network connections, filesystem access. In demo mode, it also simulates a blocked connection to a known command-and-control IP address. Verdict: CLEAN. The blocked actions panel shows what KRONOS stopped."*

---

### Tab 5: Enterprise Report — `localhost:3000/enterprise`

**What to show:** Compliance alignment section (OWASP, NIST, ISO 27001, SOC 2, PCI-DSS), pricing tiers.

**What to say:**
> *"This is the boardroom report. It's generated automatically from the API. Compliance alignment with five major frameworks. Pricing model. Integration options. Your legal team can use this as documented evidence of AI security review."*

---

### Tab 6: Blueprint — `localhost:3000/blueprint`

**What to show:** Click "Example 1" to load the fintech objective, click "Generate Secure Claude Blueprint", scroll through the results.

**What to say:**
> *"The blueprint engine takes a plain-English objective and returns a hardened Claude execution prompt. You get a directory architecture, 12 security standards, an approved package list, a deployment checklist, and a ready-to-paste prompt. Copy it straight into Claude Code."*

---

### Tab 7: API Docs — `127.0.0.1:8000/docs`

**What to show:** The Swagger UI with all 8 endpoints listed. Optionally try the `/health` endpoint live.

**What to say:**
> *"Full interactive API documentation. All eight endpoints, all request/response schemas, live testing from the browser. This is production-grade FastAPI documentation."*

---

## After the Demo

- [ ] Save a copy of the audit result as a screenshot
- [ ] Save the enterprise report page as a screenshot
- [ ] Have the GitHub/project folder ready to share
- [ ] Have `pitch/investor-summary.md` open to reference for follow-up questions

---

## If Something Goes Wrong

| Problem | Fix |
|---------|-----|
| Backend not responding | Check terminal for errors. Re-run: `uvicorn app.main:app --host 127.0.0.1 --port 8000` |
| Frontend shows "Cannot reach backend" | Confirm backend is on port 8000. Check `.env` file. |
| Audit results not loading | Try: `curl -X POST http://127.0.0.1:8000/api/v1/audit -H "Content-Type: application/json" -d '{"packages":["express"]}'` |
| Dashboard shows errors | Refresh the page — the dashboard auto-fetches on load |
| Swagger UI blank | Confirm CDN is reachable or use `/redoc` as fallback |
| Port 3000 busy | `npm run dev -- --port 3001`, then update links |
| Port 8000 busy | `uvicorn app.main:app --port 8001` |

---

*Practise the demo twice before any presentation. The flow should feel effortless.*
