# KRONOS CORE — Required Screenshots

*Take these screenshots for portfolio, competition submission, GitHub README, and institution sales.*

---

## How to Take Screenshots

- **Windows:** `Win + Shift + S` → select area → paste into image editor or save
- **Browser:** F11 for full-screen, then screenshot
- **Recommended resolution:** 1920×1080 or higher
- **Recommended format:** PNG (lossless)
- **File naming:** `kronos-[page]-[what].png`

---

## Screenshot List

---

### 1. Home Page — Hero Section
**URL:** `http://localhost:3000`
**What to capture:** The full hero with "KRONOS CORE" title, tagline, stats bar (4 security layers / 8 endpoints / 6 dimensions / 50 tests), and the two CTA buttons.
**Use for:** GitHub README hero image, competition submission, portfolio top card.
**Filename:** `kronos-home-hero.png`

---

### 2. Home Page — Problem Section
**URL:** `http://localhost:3000` (scroll down)
**What to capture:** The four risk cards (01 Unsafe AI Prompts, 02 Typosquatted Packages, 03 Phantom Packages, 04 Runtime Exfiltration).
**Use for:** Pitch slide: "The Problem".
**Filename:** `kronos-home-problem.png`

---

### 3. Dashboard — Security Score
**URL:** `http://localhost:3000/dashboard`
**What to capture:** The full dashboard showing health card (HEALTHY green badge), security score card with number and 6 bars, sandbox verdict card (CLEAN).
**Use for:** Investor summary, product overview, GitHub README.
**Filename:** `kronos-dashboard-score.png`

---

### 4. Audit Page — Typosquat Detection in Action
**URL:** `http://localhost:3000/audit`
**What to do:** Click "Load example packages", click "Run KRONOS Audit", wait for results.
**What to capture:** The results list showing `expresss` (TYPOSQUAT red badge), `event-stream` (DANGEROUS red badge), `express` (SAFE green badge), `helmet` (SAFE green badge) all visible together.
**Use for:** This is the HERO screenshot — use everywhere. It proves the product works.
**Filename:** `kronos-audit-typosquat.png`

---

### 5. Audit Page — Summary Bar
**URL:** `http://localhost:3000/audit` (after running audit)
**What to capture:** The summary card at the top showing "FAIL — dangerous or typosquatted packages detected" with the SAFE / FLAGGED / DANGEROUS / TOTAL counters.
**Use for:** Showing the audit verdict clearly.
**Filename:** `kronos-audit-summary.png`

---

### 6. Sandbox Page — Zero-Exfiltration Verdict
**URL:** `http://localhost:3000/sandbox`
**What to do:** Click "Run Sandbox Inspection".
**What to capture:** The verdict banner (CLEAN green), the metrics grid (processes, network, filesystem), and the blocked actions panel (red — showing the simulated C2 connection blocked).
**Use for:** Proving runtime sandboxing capability. The red "blocked actions" panel is the visual hook.
**Filename:** `kronos-sandbox-clean.png`

---

### 7. Enterprise Report — Compliance Section
**URL:** `http://localhost:3000/enterprise`
**What to capture:** The compliance alignment grid showing OWASP, NIST SP 800-53, ISO 27001, SOC 2 Type II, PCI-DSS.
**Use for:** Institution sales. Showing to procurement teams and auditors.
**Filename:** `kronos-enterprise-compliance.png`

---

### 8. Enterprise Report — Full Page
**URL:** `http://localhost:3000/enterprise`
**What to capture:** As much of the enterprise report as fits on screen — executive summary, capabilities, compliance.
**Use for:** Boardroom presentation, institutional sales meetings.
**Filename:** `kronos-enterprise-full.png`

---

### 9. Blueprint Generator — Result
**URL:** `http://localhost:3000/blueprint`
**What to do:** Click "Example 1", click "Generate Secure Claude Blueprint", wait for result.
**What to capture:** The blueprint result showing the risk score, directory architecture, and the beginning of the Claude execution prompt.
**Use for:** Demonstrating AI prompt hardening capability.
**Filename:** `kronos-blueprint-result.png`

---

### 10. FastAPI Swagger UI
**URL:** `http://127.0.0.1:8000/docs`
**What to capture:** The full Swagger page showing the KRONOS CORE title and all 8 endpoint groups listed.
**Use for:** GitHub README, proving the API is fully documented.
**Filename:** `kronos-api-docs.png`

---

### 11. Terminal — Tests Passing
**What to do:** Run `pytest tests/ -v` from the project root.
**What to capture:** The terminal output showing all 50 test names with green "PASSED" and the final line: `50 passed, 6 warnings in X.XXs`
**Use for:** Proving code quality. Include in competition submission.
**Filename:** `kronos-terminal-tests.png`

---

### 12. Terminal — Backend Running
**What to capture:** The terminal showing the uvicorn startup output:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```
Plus a few JSON log lines from structlog.
**Use for:** Showing the product is live.
**Filename:** `kronos-terminal-backend.png`

---

### 13. Terminal — Frontend Build
**What to do:** Run `npm run build` from the `frontend/` directory.
**What to capture:** The Next.js build output showing `✓ Compiled successfully` and the route table listing all 6 pages.
**Use for:** Proving production build quality.
**Filename:** `kronos-terminal-build.png`

---

## Priority Order

If you can only take 5 screenshots, take these:

| Priority | Screenshot | Why |
|----------|-----------|-----|
| 1 | `kronos-audit-typosquat.png` | The product's killer feature, visually clear |
| 2 | `kronos-dashboard-score.png` | Shows real-time data + scoring at a glance |
| 3 | `kronos-sandbox-clean.png` | The blocked C2 action is visually dramatic |
| 4 | `kronos-enterprise-compliance.png` | Unlocks institutional buyers |
| 5 | `kronos-terminal-tests.png` | Proves code quality to technical judges |

---

## Organising Your Screenshots

```
screenshots/
├── kronos-home-hero.png
├── kronos-home-problem.png
├── kronos-dashboard-score.png
├── kronos-audit-typosquat.png
├── kronos-audit-summary.png
├── kronos-sandbox-clean.png
├── kronos-enterprise-compliance.png
├── kronos-enterprise-full.png
├── kronos-blueprint-result.png
├── kronos-api-docs.png
├── kronos-terminal-tests.png
├── kronos-terminal-backend.png
└── kronos-terminal-build.png
```
