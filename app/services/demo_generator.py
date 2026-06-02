import uuid
from datetime import datetime, timezone

from app.models.demo import (
    CompetitionDemoResponse,
    EnterpriseReportResponse,
    RoadmapItem,
    TargetCustomer,
    TechLayer,
)


def get_competition_demo() -> CompetitionDemoResponse:
    return CompetitionDemoResponse(
        product_name="KRONOS CORE",
        tagline=(
            "The Autonomous Security & Prompt Architecture Gateway that converts raw project "
            "objectives into secure Claude execution blueprints — before a single line of code is written."
        ),
        problem_statement=(
            "Every company using AI coding assistants faces four invisible threats: "
            "(1) AI-generated code that embeds security vulnerabilities because the prompt was not hardened; "
            "(2) typosquatted npm packages silently harvesting credentials; "
            "(3) phantom packages hallucinated by LLMs that don't exist or are malicious; "
            "(4) post-deployment runtime exfiltration through hidden network calls. "
            "Current developer tooling has no layer that addresses all four simultaneously."
        ),
        solution=(
            "KRONOS CORE sits between a developer's intent and the AI model. "
            "It ingests a raw objective, generates a hardened execution blueprint with secure coding "
            "constraints, audits every npm dependency before installation using an allowlist-first model, "
            "and inspects runtime behaviour using sandboxed process/network analysis — "
            "blocking exfiltration before it reaches production."
        ),
        target_customers=[
            TargetCustomer(
                segment="Software Product Companies",
                pain_point="AI coding tools generate insecure code that passes review and reaches production",
                value_delivered="Every AI-assisted feature is pre-hardened before development begins",
            ),
            TargetCustomer(
                segment="AI-Native Startups",
                pain_point="Moving fast with LLMs but have no security governance layer",
                value_delivered="Enterprise-grade security posture without a dedicated security team",
            ),
            TargetCustomer(
                segment="Banks and Financial Institutions",
                pain_point="Regulatory pressure to audit AI tooling and prove secure development practices",
                value_delivered="Audit trail, compliance alignment, and documented risk scoring",
            ),
            TargetCustomer(
                segment="Government Digital Teams",
                pain_point="Cannot deploy AI-generated code without security certification",
                value_delivered="Structured blueprint and sandbox report usable as compliance evidence",
            ),
            TargetCustomer(
                segment="University Computer Science Departments",
                pain_point="Students using AI tools to submit code with hidden vulnerabilities",
                value_delivered="Blueprint-enforced standards teach secure development from day one",
            ),
            TargetCustomer(
                segment="Cybersecurity Consulting Firms",
                pain_point="Clients adopting AI coding tools with no governance framework",
                value_delivered="White-label KRONOS CORE as part of AI security advisory offering",
            ),
        ],
        market_use_cases=[
            "Pre-development security gating: generate a KRONOS blueprint before any AI coding session",
            "CI/CD pipeline integration: block deployments with HIGH npm audit risk or failed sandbox",
            "Developer onboarding: enforce secure coding standards from day one via blueprint",
            "Supply chain security: automated typosquat and phantom package detection before npm install",
            "Compliance evidence: export security score report for ISO 27001 / SOC 2 audit trails",
            "Incident response: retroactive sandbox analysis of deployed services showing anomalous behaviour",
            "Enterprise AI governance: centralised policy enforcement for all AI-assisted development",
        ],
        technical_innovation=[
            "Allowlist-first npm audit with fuzzy typosquat detection using sequence similarity scoring",
            "Prompt injection prevention via structured blueprint generation before any Claude API call",
            "Runtime behavioural sandboxing using psutil process and network socket inspection",
            "Zero-trust package model: packages not on the trusted list are flagged, not silently installed",
            "Composite enterprise security scoring across 6 dimensions with actionable fix recommendations",
            "Docker hardening template: cap_drop ALL, non-root, read-only filesystem, tmpfs scratch",
            "Structured audit log output suitable for SIEM ingestion and compliance reporting",
        ],
        security_architecture=[
            TechLayer(
                layer="Layer 0 — Intent",
                component="Raw project objective from developer",
                security_role="Untrusted input — validated and scoped before any AI interaction",
            ),
            TechLayer(
                layer="Layer 1 — Blueprint Engine",
                component="KRONOS Blueprint Generator",
                security_role="Converts objective into hardened Claude prompt with explicit security constraints",
            ),
            TechLayer(
                layer="Layer 2 — Static Audit",
                component="KRONOS NPM Auditor",
                security_role="Allowlist-first package scanning; blocks typosquats and forbidden packages",
            ),
            TechLayer(
                layer="Layer 3 — Runtime Sandbox",
                component="KRONOS Sandbox Inspector",
                security_role="Process + network + filesystem inspection; blocks exfiltration indicators",
            ),
            TechLayer(
                layer="Layer 4 — Score & Report",
                component="KRONOS Security Scorer",
                security_role="Composite risk score with executive summary for compliance and go/no-go decisions",
            ),
            TechLayer(
                layer="Layer 5 — Deployment Gate",
                component="Docker Hardening + CI Integration",
                security_role="Enforces container isolation: cap_drop, no-new-privileges, non-root runtime",
            ),
        ],
        demo_flow=[
            "1. POST /api/v1/blueprint — submit 'Build a fintech payment API with JWT auth'",
            "2. Receive full Claude execution blueprint with directory architecture and security standards",
            "3. POST /api/v1/audit — submit package list: ['express', 'expresss', 'event-stream', 'helmet']",
            "4. See real-time detection: 'expresss' flagged as TYPOSQUAT, 'event-stream' flagged DANGEROUS",
            "5. GET /api/v1/sandbox?demo=true — run behavioural sandbox inspection",
            "6. See blocked simulated connection to C2 range 185.220.101.0:4444",
            "7. POST /api/v1/security/score — receive composite score: 87/100 LOW RISK",
            "8. GET /api/v1/enterprise/report — receive investor/compliance-ready report",
            "Total demo time: under 3 minutes. All endpoints live and functional.",
        ],
        commercial_value=(
            "KRONOS CORE replaces a combination of: manual security review, external npm audit services, "
            "runtime monitoring agents, and AI prompt engineering consultants — delivering all four in a "
            "single microservice that integrates into any CI/CD pipeline. At $299/month per engineering team, "
            "the addressable market is any organisation using AI coding tools (estimated 14M developers globally "
            "by 2026). Enterprise licensing starts at $2,000/month. "
            "The product also serves as a compliance evidence generator, which unlocks government and banking verticals."
        ),
        competition_advantage=(
            "No existing product combines AI prompt hardening, static npm security, dynamic runtime sandboxing, "
            "and enterprise security scoring in a single API-first microservice. "
            "KRONOS CORE is deployable in under 5 minutes via Docker, requires no AI API keys to run, "
            "and generates human-readable reports that non-technical stakeholders understand. "
            "It is defensible IP, not a commodity wrapper around an existing tool."
        ),
        future_roadmap=[
            RoadmapItem(
                phase="Q3 2026",
                feature="Claude API integration for real-time blueprint refinement",
                business_impact="Blueprints become dynamic and context-aware for complex projects",
            ),
            RoadmapItem(
                phase="Q4 2026",
                feature="VS Code and JetBrains extension",
                business_impact="Developer adoption multiplier — security embedded in the IDE workflow",
            ),
            RoadmapItem(
                phase="Q1 2027",
                feature="GitHub Actions and GitLab CI native integration",
                business_impact="Automated blocking of unsafe AI-generated PRs before merge",
            ),
            RoadmapItem(
                phase="Q2 2027",
                feature="SOC 2 Type II certification and ISO 27001 alignment module",
                business_impact="Unlocks enterprise and government procurement cycles",
            ),
            RoadmapItem(
                phase="Q3 2027",
                feature="Multi-language support: Python pip, Go modules, Rust cargo audit",
                business_impact="Expands TAM to all AI-assisted development regardless of stack",
            ),
        ],
        pitch_closing=(
            "KRONOS CORE solves the last unsolved problem in AI-assisted development: "
            "the gap between what an AI produces and what a production security standard requires. "
            "We close that gap before the first line of code is written, before the first package is installed, "
            "and before the first container is deployed. "
            "This is the security layer every AI-first engineering team needs and cannot build themselves."
        ),
    )


def get_enterprise_report() -> EnterpriseReportResponse:
    report_id = f"KER-{uuid.uuid4().hex[:12].upper()}"
    generated_at = datetime.now(timezone.utc).isoformat()
    return EnterpriseReportResponse(
        report_id=report_id,
        generated_at=generated_at,
        product="KRONOS CORE v1.0",
        executive_summary=(
            "KRONOS CORE is an enterprise-grade AI security gateway microservice that enforces "
            "secure development practices across the full lifecycle of AI-assisted software projects. "
            "It operates as a lightweight API-first service, requiring no external AI API keys for core "
            "functionality, and is deployable on-premises or in private cloud environments to satisfy "
            "data sovereignty requirements."
        ),
        capabilities=[
            "Secure Claude execution blueprint generation from raw project objectives",
            "Allowlist-first npm package static audit with typosquat detection",
            "Runtime process and network behavioural sandboxing via psutil",
            "Composite 6-dimension enterprise security scoring (0–100)",
            "Competition and investor-ready demo mode with full pitch narrative",
            "Structured audit log output for SIEM and compliance evidence",
            "Docker-hardened deployment: non-root, cap_drop ALL, read-only filesystem",
            "Rate-limited, CORS-locked API with security response headers",
        ],
        compliance_alignment=[
            "OWASP Top 10 — input validation, injection prevention, secure headers enforced by design",
            "CIS Docker Benchmark — container hardening template included",
            "NIST SP 800-53 — access control, audit logging, least privilege architecture",
            "ISO 27001 A.14 — secure development lifecycle integration point",
            "SOC 2 Type II — audit trail generation and runtime monitoring hooks",
            "PCI-DSS — payment project blueprints include dedicated audit directory",
        ],
        integration_options=[
            "REST API — integrates with any CI/CD pipeline via HTTP",
            "GitHub Actions — POST to /api/v1/audit in PR check workflow",
            "GitLab CI — curl-based integration in .gitlab-ci.yml",
            "Jenkins — shell step integration with exit-code-based build gating",
            "Docker Compose — run as a sidecar in development environments",
            "Kubernetes — deployable as a ClusterIP service with NetworkPolicy isolation",
        ],
        deployment_models=[
            "Self-hosted Docker (recommended for sensitive environments)",
            "Private cloud (AWS ECS, Azure Container Apps, GCP Cloud Run)",
            "On-premises bare metal with Docker or Podman",
            "Developer workstation (local demo mode)",
        ],
        pricing_model=(
            "Starter: $299/month — up to 5 developers, 500 blueprint generations, unlimited audits. "
            "Team: $999/month — up to 25 developers, unlimited blueprints, SIEM export, SSO. "
            "Enterprise: Custom — unlimited developers, on-premises deployment, SLA, dedicated support."
        ),
        support_model=(
            "Enterprise customers receive: 99.9% SLA, 4-hour response SLA, dedicated Slack channel, "
            "quarterly security architecture review, and priority feature requests."
        ),
        references=[
            "OWASP Foundation — owasp.org",
            "NIST Cybersecurity Framework — nist.gov/cyberframework",
            "CIS Benchmarks — cisecurity.org/cis-benchmarks",
            "npm Security Advisories — npmjs.com/advisories",
            "Anthropic Claude Usage Policy — anthropic.com/usage-policy",
        ],
    )
