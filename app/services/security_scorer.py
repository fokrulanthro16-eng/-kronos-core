import uuid
from datetime import datetime, timezone
from typing import List

from app.models.security_score import (
    RiskLevel,
    ScoreCategory,
    SecurityScoreRequest,
    SecurityScoreResponse,
)


def _score_prompt_safety(blueprint_generated: bool) -> ScoreCategory:
    score = 18 if blueprint_generated else 8
    findings = []
    if blueprint_generated:
        findings.append("KRONOS Blueprint generated — secure execution prompt enforced")
        findings.append("Prompt injection guardrails active")
    else:
        findings.append("No blueprint generated — AI prompt injection risk is UNMITIGATED")
    return ScoreCategory(
        name="Prompt Safety",
        score=score,
        max_score=20,
        status="PASS" if score >= 14 else "FAIL",
        findings=findings,
    )


def _score_package_safety(total: int, flagged: int) -> ScoreCategory:
    if total == 0:
        score = 10
        findings = ["No packages audited — static audit not yet run"]
        status = "WARN"
    else:
        ratio = flagged / total
        if ratio == 0:
            score = 20
            status = "PASS"
            findings = [f"All {total} packages passed KRONOS audit", "No typosquats or forbidden packages detected"]
        elif ratio <= 0.1:
            score = 15
            status = "WARN"
            findings = [f"{flagged}/{total} packages flagged — review required"]
        elif ratio <= 0.3:
            score = 8
            status = "FAIL"
            findings = [f"{flagged}/{total} packages flagged — significant risk", "Do not deploy until resolved"]
        else:
            score = 2
            status = "CRITICAL"
            findings = [f"{flagged}/{total} packages are risky — STOP deployment", "Possible supply chain compromise"]
    return ScoreCategory(name="Package Safety", score=score, max_score=20, status=status, findings=findings)


def _score_runtime_isolation(sandbox_passed: bool, docker_hardened: bool) -> ScoreCategory:
    score = 0
    findings = []
    if sandbox_passed:
        score += 12
        findings.append("Sandbox inspection PASSED — no exfiltration indicators")
    else:
        findings.append("Sandbox inspection FAILED — runtime isolation not verified")
    if docker_hardened:
        score += 8
        findings.append("Docker hardening applied: cap_drop ALL, no-new-privileges, non-root user")
    else:
        findings.append("Docker hardening not confirmed — apply cap_drop and no-new-privileges")
    status = "PASS" if score >= 16 else ("WARN" if score >= 10 else "FAIL")
    return ScoreCategory(name="Runtime Isolation", score=score, max_score=20, status=status, findings=findings)


def _score_exfiltration(sandbox_passed: bool, auth: bool) -> ScoreCategory:
    score = 0
    findings = []
    if sandbox_passed:
        score += 12
        findings.append("Zero outbound exfiltration indicators in sandbox run")
    else:
        findings.append("Sandbox not clean — exfiltration risk unquantified")
    if auth:
        score += 5
        findings.append("Authentication layer reduces internal data exposure risk")
    else:
        findings.append("No auth layer confirmed — unauthenticated endpoints may expose data")
    score = min(20, score + 3)
    findings.append("Network egress monitoring recommended in production")
    status = "PASS" if score >= 16 else ("WARN" if score >= 10 else "FAIL")
    return ScoreCategory(name="Data Exfiltration Protection", score=score, max_score=20, status=status, findings=findings)


def _score_deployment(docker_hardened: bool, tls: bool, input_val: bool) -> ScoreCategory:
    score = 0
    findings = []
    if docker_hardened:
        score += 7
        findings.append("Container hardening: read-only fs, tmpfs, cap_drop ALL")
    else:
        findings.append("Container hardening incomplete")
    if tls:
        score += 7
        findings.append("TLS enabled — data in transit encrypted")
    else:
        findings.append("TLS not confirmed — plaintext risk in transit")
    if input_val:
        score += 6
        findings.append("Input validation enforced — injection attack surface reduced")
    else:
        findings.append("Input validation not confirmed")
    status = "PASS" if score >= 16 else ("WARN" if score >= 10 else "FAIL")
    return ScoreCategory(name="Deployment Hardening", score=score, max_score=20, status=status, findings=findings)


def _score_production_readiness(blueprint_generated: bool, auth: bool, tls: bool) -> ScoreCategory:
    score = 0
    findings = []
    checks = [
        (blueprint_generated, "Secure execution blueprint generated", 7),
        (auth, "Authentication implemented", 7),
        (tls, "TLS / HTTPS enforced", 6),
    ]
    for passed, msg, pts in checks:
        if passed:
            score += pts
            findings.append(f"PASS: {msg}")
        else:
            findings.append(f"MISSING: {msg}")
    status = "PASS" if score >= 16 else ("WARN" if score >= 10 else "FAIL")
    return ScoreCategory(name="Production Readiness", score=score, max_score=20, status=status, findings=findings)


def compute_security_score(request: SecurityScoreRequest) -> SecurityScoreResponse:
    score_id = f"KSC-{uuid.uuid4().hex[:12].upper()}"
    scored_at = datetime.now(timezone.utc).isoformat()

    categories = [
        _score_prompt_safety(request.blueprint_generated),
        _score_package_safety(request.packages_audited, request.packages_flagged),
        _score_runtime_isolation(request.sandbox_passed, request.docker_hardened),
        _score_exfiltration(request.sandbox_passed, request.auth_implemented),
        _score_deployment(request.docker_hardened, request.tls_enabled, request.input_validation),
        _score_production_readiness(request.blueprint_generated, request.auth_implemented, request.tls_enabled),
    ]

    raw = sum(c.score for c in categories)
    max_raw = sum(c.max_score for c in categories)
    total = round(raw * 100 / max_raw)

    if total >= 85:
        risk_level = RiskLevel.LOW
    elif total >= 65:
        risk_level = RiskLevel.MEDIUM
    elif total >= 40:
        risk_level = RiskLevel.HIGH
    else:
        risk_level = RiskLevel.CRITICAL

    recs: List[str] = []
    for cat in categories:
        if cat.status in ("FAIL", "CRITICAL", "WARN"):
            recs.append(f"Improve {cat.name}: {cat.findings[-1]}")
    if not recs:
        recs.append("Maintain current security posture and schedule quarterly review.")

    enterprise_ready = total >= 75 and all(c.status in ("PASS", "WARN") for c in categories)

    summary = (
        f"KRONOS CORE Security Score: {total}/100 — Risk Level: {risk_level.value}. "
        f"{'Enterprise deployment approved subject to WARN items.' if enterprise_ready else 'Enterprise deployment NOT approved — resolve FAIL items before production.'}"
    )

    return SecurityScoreResponse(
        score_id=score_id,
        scored_at=scored_at,
        total_score=total,
        risk_level=risk_level,
        categories=categories,
        recommendations=recs,
        executive_summary=summary,
        enterprise_ready=enterprise_ready,
    )
