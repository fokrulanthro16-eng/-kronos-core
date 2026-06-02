# KRONOS CORE — Five-Minute Judge Presentation Script

---

## Pre-Presentation Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Terminal with `pytest tests/ -v` result visible (or screenshot ready)
- [ ] Slides/README open as backup
- [ ] Docker Compose file ready to reference
- [ ] Demo URLs bookmarked

---

## Script

---

### [0:00 – 0:30] Opening Hook

> "I want to start with a question.
>
> How many organisations in this room are using AI to write production code?
>
> And of those — how many have a documented process for auditing what that AI produces
> before it goes into a pull request, before it gets deployed, before it touches customer data?
>
> Most don't. Because the tooling doesn't exist.
>
> That's what I built. This is KRONOS CORE."

---

### [0:30 – 1:30] The Market Problem

> "The AI coding tool market is growing at a rate the security industry hasn't kept up with.
> By 2026, more than 14 million developers will be using AI to write production code.
>
> But AI coding tools create four security risks that no existing product addresses together:
>
> **First.** Unsafe prompts. When a developer pastes a raw objective into an AI tool, the AI doesn't
> know about OWASP. It doesn't enforce JWT expiry, parameterised queries, or CORS allowlists
> unless you tell it to. Most developers don't.
>
> **Second.** Typosquatted packages. In 2024 alone, tens of thousands of malicious packages were
> uploaded to npm with names like `expresss` — one extra letter — designed to steal credentials
> the moment a developer runs npm install.
>
> **Third.** Phantom packages. Language models hallucinate. They recommend package names that
> don't exist or that have been registered by malicious actors. There is no current tooling
> to catch this before the install.
>
> **Fourth.** Runtime exfiltration. A seemingly functional app can contain hidden network calls
> that harvest API keys, tokens, and user data post-deployment. Current detection requires
> expensive enterprise SIEM tooling most teams can't afford.
>
> KRONOS CORE solves all four. In a single API. Deployable in five minutes."

---

### [1:30 – 2:30] Technical Innovation

> "KRONOS CORE is a FastAPI microservice with four security layers that gate each other.
>
> **Layer one** is the Blueprint Engine. You give it a raw project objective —
> 'build a fintech payment API with JWT auth' — and it returns a structured Claude execution prompt
> that enforces 12 non-negotiable secure coding standards. The AI cannot deviate from them.
>
> **Layer two** is the NPM Auditor. Every package name is checked against a trusted allowlist.
> Unknown packages are flagged. Known dangerous packages are blocked. And — this is the part
> that doesn't exist anywhere else — we use fuzzy string similarity to detect typosquats.
> `expresss` with three s's scores 91% similar to `express`. Flagged. Instantly.
>
> **Layer three** is the Sandbox Inspector. Using Python's psutil library, we scan the live
> runtime — every process, every open network socket, every writable filesystem path.
> We compare outbound connection destinations against known command-and-control IP ranges.
> Any exfiltration indicator triggers a BLOCKED verdict.
>
> **Layer four** is the Security Scorer. Six dimensions, each scored 0 to 20, normalised to 100.
> Returns a risk level — LOW, MEDIUM, HIGH, or CRITICAL — with an executive summary and
> fix recommendations. This output is the compliance evidence."

---

### [2:30 – 3:30] Live Demo

*[Open localhost:3000/audit]*

> "Let me show you the typosquat detection live.
>
> I'm submitting six package names: express, expresss, event-stream, helmet, lodahs, jsonwebtoken.
>
> Watch the results."

*[Click Run KRONOS Audit — pause for results to load]*

> "Express — SAFE. Helmet — SAFE. Jsonwebtoken — SAFE.
>
> Expresss — TYPOSQUAT. Confidence: 100%. Safe alternative: express.
> Event-stream — DANGEROUS. Used in a real supply chain attack in 2018 that compromised
> the Copay cryptocurrency wallet.
> Lodahs — DANGEROUS. A misspelling of lodash.
>
> This runs in milliseconds. No external API calls. No npm install. Pure static analysis."

*[Navigate to /sandbox]*

> "Now the sandbox."

*[Click Run Sandbox Inspection]*

> "Verdict: CLEAN. But look at the blocked actions panel.
> In demo mode, KRONOS simulated an outbound connection to 185.220.101.0:4444 —
> that's a known Tor exit node used as command-and-control infrastructure.
> Blocked. Logged. Reported."

---

### [3:30 – 4:00] Commercial Value

> "The business model is straightforward.
>
> Starter tier: $299 a month per engineering team. That's less than one hour of a senior
> security consultant.
>
> Team tier: $999 a month. Unlimited blueprints, SIEM export, SSO.
>
> Enterprise: custom licensing. On-premises deployment. SLA. This is the tier that unlocks
> banking and government procurement — because the enterprise report we generate maps directly
> to OWASP, NIST 800-53, ISO 27001, SOC 2, and PCI-DSS. Procurement teams can use our output
> as documented compliance evidence. That's worth $2,000 to $10,000 a month to those organisations.
>
> The total addressable market is every company using AI coding tools that also has compliance
> requirements. That is essentially every company that touches regulated data."

---

### [4:00 – 4:30] Why KRONOS CORE Can Win

> "Three things make this submission stand out.
>
> **One: It works.** This is not a mockup. Not a prototype. The backend has 50 passing tests.
> The frontend has a production build. Every endpoint is live and documented. You can call it
> right now from this room.
>
> **Two: The combination is novel.** Every individual component — package audit, runtime inspection,
> security scoring — exists somewhere in the ecosystem. But no product combines all four with an
> AI-specific layer in a single deployable microservice. That combination is the moat.
>
> **Three: The timing is right.** OWASP published its Top 10 for LLMs in 2025. Prompt injection
> and insecure output handling are on it. Regulators are starting to ask about AI governance.
> KRONOS CORE is the tool that answers those questions."

---

### [4:30 – 5:00] Roadmap and Close

> "The roadmap from here:
>
> Version 1.1 adds live Claude API integration for real-time blueprint refinement.
> Version 2.0 adds native GitHub Actions integration — blocking unsafe AI-generated PRs
> before they can be merged. Version 3.0 extends beyond npm to Python pip, Go modules,
> and Rust cargo.
>
> The vision: KRONOS CORE becomes the universal security layer for AI-assisted development,
> regardless of language, model, or stack.
>
> That's KRONOS CORE. Secure by design. Auditable by default. Deployable in minutes.
>
> Thank you."

---

## Q&A Preparation

**Q: How is this different from npm audit?**
> npm audit only checks known CVEs. KRONOS catches typosquats, phantom packages, and packages
> not on our trusted list — none of which appear in the CVE database because the attack is the
> package name itself.

**Q: Does this require an internet connection?**
> No. The entire core runs offline. The only external dependency is the Swagger UI CDN for /docs,
> which is optional. All auditing, sandboxing, and scoring is local.

**Q: Can you integrate with existing CI/CD?**
> Yes. Every capability is a single HTTP call. GitHub Actions, GitLab CI, Jenkins — any pipeline
> that can make an HTTP request can integrate with KRONOS CORE in under 10 minutes.

**Q: What happens if the AI API changes?**
> KRONOS CORE does not depend on the Claude API to function. Blueprint generation is local logic.
> The Claude API integration in v1.1 is additive, not foundational.
