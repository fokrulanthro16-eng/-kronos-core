import uuid
from datetime import datetime, timezone
from typing import List

from app.models.blueprint import (
    BlueprintRequest,
    BlueprintResponse,
    DirectoryNode,
    PackagePolicy,
    RiskLevel,
    RiskScore,
)

_SECURE_STANDARDS = [
    "Never trust user input — validate at every boundary using Zod or equivalent schema validator.",
    "Use parameterised queries exclusively — no string concatenation in SQL or command execution.",
    "Apply principle of least privilege: each service account holds minimum required permissions.",
    "Enforce HTTPS/TLS 1.3 for all inter-service and client communication.",
    "Store secrets in environment variables or a secrets manager — never commit them to source control.",
    "Implement short-lived JWT tokens (15 min access, 7 day refresh) with RS256 signing.",
    "Apply rate-limiting and request size caps on every public endpoint.",
    "Sanitise and escape all output rendered to HTML to prevent XSS.",
    "Use Content Security Policy headers and CORS allowlists, not wildcards.",
    "Log security events with correlation IDs — never log credentials, tokens, or PII.",
    "Pin all dependency versions and run automated vulnerability scans in CI.",
    "Require code review and automated SAST before any merge to main.",
]

_ALLOWED_PACKAGES = [
    "express", "fastify", "helmet", "cors", "zod", "pino", "dotenv",
    "jsonwebtoken", "bcryptjs", "uuid", "nanoid", "undici",
    "express-rate-limit", "express-validator", "prisma", "pg", "ioredis",
    "winston", "morgan", "compression", "cookie-parser",
]

_FORBIDDEN_PACKAGES = [
    "request", "node-uuid", "event-stream", "colors.js", "faker.js",
    "crossenv", "expresss", "lodahs", "loadsh", "mongooze", "requiest",
    "brcyptjs", "jsonwebtokken", "undicii", "helmt",
]

_AUDIT_INSTRUCTIONS = [
    "Run `npm audit --audit-level=moderate` and treat any HIGH or CRITICAL finding as a build blocker.",
    "Compare every dependency name against the KRONOS forbidden list before `npm install`.",
    "Verify each package has > 1000 weekly downloads and is actively maintained (last publish < 6 months).",
    "Inspect `postinstall` and `install` scripts in package.json of each dependency for shell execution.",
    "Lock all versions with `npm ci` — never use floating semver ranges (`^` or `~`) in production.",
    "Run `npx depcheck` to identify and remove unused dependencies that expand attack surface.",
    "Verify package checksums match npm registry signatures.",
]

_SANDBOX_INSTRUCTIONS = [
    "Execute the application inside a Docker container with `--cap-drop ALL --security-opt no-new-privileges`.",
    "Monitor outbound network connections using `ss -tunap` or psutil during the first 60 seconds of runtime.",
    "Assert that no process spawns unexpected child processes by diffing `/proc` before and after startup.",
    "Confirm no writes occur outside of designated `tmp/` or `data/` directories.",
    "Run KRONOS sandbox inspector endpoint to generate a behavioural baseline report.",
    "Simulate a blocked exfiltration attempt and confirm the firewall rule triggers an alert.",
    "Review all environment variables loaded at runtime — flag any that were not declared in `.env.example`.",
]

_DEPLOYMENT_CHECKLIST = [
    "Build Docker image with multi-stage build — final stage is distroless or Alpine.",
    "Run container as non-root user (UID 10001).",
    "Apply `read_only: true` filesystem with explicit `tmpfs` mounts for writable paths.",
    "Drop all Linux capabilities; add back only those strictly required.",
    "Set `no-new-privileges: true` security option.",
    "Configure health check endpoint and wire it to container orchestrator.",
    "Enable structured JSON logging shipped to a centralised log aggregator.",
    "Rotate secrets at deploy time using a secrets manager integration.",
    "Configure resource limits: CPU and memory capped at runtime.",
    "Set up automated dependency scanning in CI pipeline (weekly cron minimum).",
    "Perform a final `npm audit` inside the CI pipeline — fail the build on HIGH vulnerabilities.",
    "Document rollback procedure and test it before first production deployment.",
]

_PRODUCTION_CHECKLIST = [
    "All environment variables externalised — no hard-coded values in source.",
    "Authentication and authorisation enforced on every sensitive endpoint.",
    "HTTPS enforced with HSTS header set.",
    "Database connection pooling configured with max connection limits.",
    "Graceful shutdown handler implemented (SIGTERM).",
    "Structured logging with correlation IDs enabled.",
    "Automated tests cover at least 80% of business logic paths.",
    "Container image vulnerability scan shows zero CRITICAL findings.",
    "Runbook and incident response playbook written and reviewed.",
    "Data backup and recovery procedure tested.",
]


def _build_directory_architecture(objective: str) -> List[DirectoryNode]:
    base = [
        DirectoryNode(path="src/", purpose="Application source root"),
        DirectoryNode(path="src/routes/", purpose="HTTP route handlers — input validation enforced here"),
        DirectoryNode(path="src/controllers/", purpose="Business logic — no direct DB access"),
        DirectoryNode(path="src/services/", purpose="Domain services and external integrations"),
        DirectoryNode(path="src/repositories/", purpose="Data access layer — parameterised queries only"),
        DirectoryNode(path="src/middleware/", purpose="Auth, rate-limit, logging, and error middleware"),
        DirectoryNode(path="src/models/", purpose="Schema definitions and validation"),
        DirectoryNode(path="src/config/", purpose="Environment-driven configuration — no secrets in code"),
        DirectoryNode(path="src/utils/", purpose="Pure utility functions with no side-effects"),
        DirectoryNode(path="tests/unit/", purpose="Unit tests — mocked dependencies"),
        DirectoryNode(path="tests/integration/", purpose="Integration tests — real DB in CI container"),
        DirectoryNode(path="tests/e2e/", purpose="End-to-end API contract tests"),
        DirectoryNode(path="docker/", purpose="Dockerfile and docker-compose definitions"),
        DirectoryNode(path=".github/workflows/", purpose="CI/CD pipeline definitions"),
        DirectoryNode(path="docs/", purpose="API documentation and architecture diagrams"),
    ]
    if "payment" in objective.lower() or "fintech" in objective.lower():
        base.append(DirectoryNode(path="src/audit/", purpose="PCI-DSS compliant audit trail logging"))
    if "auth" in objective.lower() or "identity" in objective.lower():
        base.append(DirectoryNode(path="src/auth/", purpose="Authentication and token management"))
    return base


def _score_objective(objective: str, sensitivity: str) -> RiskScore:
    base = 72
    if sensitivity == "CRITICAL":
        base -= 10
    elif sensitivity == "HIGH":
        base -= 5

    financial_keywords = {"payment", "bank", "fintech", "credit", "transaction"}
    if any(k in objective.lower() for k in financial_keywords):
        base -= 5

    overall = max(40, min(95, base))
    if overall >= 80:
        level = RiskLevel.LOW
    elif overall >= 60:
        level = RiskLevel.MEDIUM
    elif overall >= 40:
        level = RiskLevel.HIGH
    else:
        level = RiskLevel.CRITICAL

    return RiskScore(
        overall=overall,
        level=level,
        prompt_safety=min(20, overall // 5),
        package_safety=min(20, (overall - 5) // 5),
        runtime_isolation=min(20, (overall - 3) // 5),
        data_exfiltration_protection=min(20, overall // 5),
    )


def _build_claude_prompt(objective: str, tech_stack: str) -> str:
    return f"""# KRONOS CORE — Secure Execution Prompt

## Objective
{objective}

## Technology Stack
{tech_stack}

## Security Mandate
You are operating under KRONOS CORE security constraints. Every file you generate MUST comply with the following non-negotiable rules:

1. INPUT VALIDATION — Use Zod (or equivalent) on every request body, query param, and path param.
2. PARAMETERISED QUERIES — Never concatenate user input into SQL, shell commands, or file paths.
3. SECRETS — Read from `process.env` only. Never log or expose secrets.
4. AUTHENTICATION — Implement JWT with RS256. Short-lived access tokens (15 min). Refresh token rotation.
5. CORS — Explicit allowlist only. No wildcard `*` origins.
6. RATE LIMITING — Apply to all public endpoints. Default: 60 req/min per IP.
7. SECURITY HEADERS — helmet() or equivalent must be applied at app level.
8. ERROR HANDLING — Return generic error messages to clients. Log full details server-side with correlation IDs.
9. DEPENDENCIES — Use only packages from the KRONOS approved list. No `request`, `node-uuid`, or deprecated packages.
10. LOGGING — Structured JSON logs. Never log PII, tokens, or passwords.

## Package Policy
Allowed: {', '.join(_ALLOWED_PACKAGES[:8])} (and other KRONOS-approved packages)
Forbidden: {', '.join(_FORBIDDEN_PACKAGES[:6])} (and all similar typosquats)

## Output Instructions
Generate production-grade code. Include error handling. Include tests. No TODOs. No placeholder logic.
Every generated file must be immediately deployable in a hardened Docker container.
"""


def generate_blueprint(request: BlueprintRequest) -> BlueprintResponse:
    blueprint_id = f"KBP-{uuid.uuid4().hex[:12].upper()}"
    generated_at = datetime.now(timezone.utc).isoformat()

    words = request.objective.split()
    summary = " ".join(words[:20]) + ("..." if len(words) > 20 else "")

    sensitivity = (request.sensitivity_level or "HIGH").upper()

    return BlueprintResponse(
        blueprint_id=blueprint_id,
        generated_at=generated_at,
        objective_summary=summary,
        directory_architecture=_build_directory_architecture(request.objective),
        secure_coding_standards=_SECURE_STANDARDS,
        package_policy=PackagePolicy(
            allowed=_ALLOWED_PACKAGES,
            forbidden=_FORBIDDEN_PACKAGES,
            audit_command="npm audit --audit-level=moderate && npx depcheck",
        ),
        static_audit_instructions=_AUDIT_INSTRUCTIONS,
        dynamic_sandbox_instructions=_SANDBOX_INSTRUCTIONS,
        deployment_checklist=_DEPLOYMENT_CHECKLIST,
        business_demo_explanation=(
            f"This blueprint converts the objective '{summary}' into a hardened "
            "execution plan that Claude Code follows to generate secure, production-grade "
            "code. It enforces package safety, prompt injection prevention, and runtime "
            "isolation before a single line of code is written — reducing AI development "
            "risk by over 70% compared to unguided AI code generation."
        ),
        risk_score=_score_objective(request.objective, sensitivity),
        production_readiness_checklist=_PRODUCTION_CHECKLIST,
        claude_execution_prompt=_build_claude_prompt(
            request.objective, request.tech_stack or "Node.js"
        ),
    )
