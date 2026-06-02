from typing import List, Optional, Tuple

import httpx

from app.config import get_settings
from app.core.logging import get_logger
from app.models.audit import (
    AuditResult,
    InstallScriptAnalysis,
    PackageMetadata,
    RiskLevel,
    TyposquatMatch,
    VulnerabilityInfo,
)
from app.services.allowlist import is_allowlisted
from app.services.typosquatting import analyze_install_scripts, detect_typosquatting

logger = get_logger(__name__)
settings = get_settings()


async def fetch_package_metadata(name: str, version: Optional[str] = None) -> Optional[dict]:
    url = f"{settings.NPM_REGISTRY_URL}/{name}"
    if version:
        url += f"/{version}"
    try:
        async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT_SECONDS) as client:
            resp = await client.get(url, headers={"Accept": "application/json"})
            if resp.status_code == 200:
                return resp.json()
            if resp.status_code == 404:
                return None
    except httpx.TimeoutException:
        logger.warning("npm_registry_timeout", package=name)
    except Exception as exc:
        logger.error("npm_registry_error", package=name, error=str(exc))
    return None


def _score_and_level(
    allowlisted: bool,
    is_typosquat: bool,
    typosquat_matches: List[TyposquatMatch],
    metadata: Optional[PackageMetadata],
    install_risk: int,
    vulnerabilities: List[VulnerabilityInfo],
) -> Tuple[int, RiskLevel]:
    score = 50

    if allowlisted:
        score += 30
    if is_typosquat:
        score -= 50
    elif typosquat_matches:
        score -= 40 if typosquat_matches[0].distance == 1 else 20

    if metadata:
        if not metadata.exists_on_registry:
            score -= 30
        if not metadata.has_repository:
            score -= 5

    score -= install_risk // 5

    severity_penalty = {"critical": 30, "high": 20, "moderate": 10, "low": 5}
    for v in vulnerabilities:
        score -= severity_penalty.get(v.severity, 5)

    score = max(0, min(100, score))
    if score >= 80:
        return score, RiskLevel.SAFE
    if score >= 60:
        return score, RiskLevel.LOW
    if score >= 40:
        return score, RiskLevel.MEDIUM
    if score >= 20:
        return score, RiskLevel.HIGH
    return score, RiskLevel.CRITICAL


async def audit_package(name: str, version: Optional[str] = None) -> AuditResult:
    logger.info("audit_start", package=name, version=version)
    name = name.lower()
    warnings: List[str] = []

    allowlisted = is_allowlisted(name)
    typosquat_matches = detect_typosquatting(name)
    is_typosquat = bool(typosquat_matches) and typosquat_matches[0].distance <= 2

    raw = await fetch_package_metadata(name, version)

    if raw is None:
        warnings.append(f"'{name}' not found on the npm registry")
        return AuditResult(
            package_name=name,
            version=version,
            risk_level=RiskLevel.BLOCKED,
            score=0,
            allowlisted=allowlisted,
            blocked=True,
            block_reason="Package absent from npm registry — likely a phantom package",
            is_typosquat=is_typosquat,
            typosquat_matches=typosquat_matches,
            metadata=PackageMetadata(exists_on_registry=False),
            warnings=warnings,
        )

    # Resolve version
    resolved_version = version or raw.get("dist-tags", {}).get("latest")
    version_data: dict = {}
    if resolved_version and "versions" in raw:
        version_data = raw["versions"].get(resolved_version, {})
    elif "versions" in raw:
        keys = list(raw["versions"].keys())
        if keys:
            resolved_version = keys[-1]
            version_data = raw["versions"][resolved_version]

    repository = version_data.get("repository") or raw.get("repository")
    scripts = version_data.get("scripts", {})
    deps_count = len(version_data.get("dependencies", {}))
    time_data = raw.get("time", {})
    author_raw = raw.get("author") or version_data.get("author") or ""
    author_str = (
        author_raw if isinstance(author_raw, str)
        else author_raw.get("name", "") if isinstance(author_raw, dict)
        else str(author_raw)
    )

    metadata = PackageMetadata(
        exists_on_registry=True,
        version=resolved_version,
        description=(raw.get("description") or version_data.get("description")),
        author=author_str,
        created_at=time_data.get("created"),
        has_repository=bool(repository),
        dependencies_count=deps_count,
    )

    install_analysis: Optional[InstallScriptAnalysis] = None
    if scripts:
        install_analysis = analyze_install_scripts(scripts)
        if install_analysis.risk_score > 0:
            warnings.append(
                f"Suspicious install scripts detected "
                f"(risk score {install_analysis.risk_score}/100)"
            )

    if is_typosquat:
        warnings.append(
            f"TYPOSQUATTING DETECTED: '{name}' is suspiciously similar to "
            f"'{typosquat_matches[0].similar_to}' (distance={typosquat_matches[0].distance})"
        )
    if not metadata.has_repository:
        warnings.append("No repository link — reduced trust signal")
    if not allowlisted:
        warnings.append("Not on the approved allowlist")

    install_risk = install_analysis.risk_score if install_analysis else 0
    score, risk_level = _score_and_level(
        allowlisted, is_typosquat, typosquat_matches, metadata, install_risk, []
    )

    blocked = False
    block_reason: Optional[str] = None
    if is_typosquat:
        blocked, block_reason = True, (
            f"Typosquatting attack — '{name}' mimics '{typosquat_matches[0].similar_to}'"
        )
        risk_level, score = RiskLevel.BLOCKED, 0
    elif install_risk >= 60:
        blocked, block_reason = True, "Highly suspicious install lifecycle scripts"
        risk_level, score = RiskLevel.BLOCKED, 0

    return AuditResult(
        package_name=name,
        version=resolved_version,
        risk_level=risk_level,
        score=score,
        allowlisted=allowlisted,
        blocked=blocked,
        block_reason=block_reason,
        is_typosquat=is_typosquat,
        typosquat_matches=typosquat_matches,
        vulnerabilities=[],
        install_script_analysis=install_analysis,
        metadata=metadata,
        warnings=warnings,
    )
