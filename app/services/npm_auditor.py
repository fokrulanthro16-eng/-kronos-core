import uuid
import re
from datetime import datetime, timezone
from difflib import SequenceMatcher
from typing import List, Tuple

from app.models.audit import (
    AuditSummary,
    PackageAuditRequest,
    PackageAuditResponse,
    PackageResult,
    PackageRisk,
)

_TRUSTED_PACKAGES = {
    "express", "fastify", "helmet", "cors", "zod", "pino", "dotenv",
    "jsonwebtoken", "bcryptjs", "uuid", "nanoid", "undici",
    "express-rate-limit", "express-validator", "prisma", "pg", "ioredis",
    "winston", "morgan", "compression", "cookie-parser", "lodash",
    "axios", "node-fetch", "chalk", "commander", "yargs", "inquirer",
    "jest", "mocha", "chai", "sinon", "supertest", "prettier", "eslint",
    "typescript", "ts-node", "nodemon", "concurrently", "cross-env",
    "multer", "sharp", "stripe", "twilio", "socket.io", "ws",
    "mongoose", "sequelize", "knex", "typeorm", "mikro-orm",
    "redis", "bull", "agenda", "node-cron", "luxon", "date-fns",
    "joi", "yup", "class-validator", "reflect-metadata", "tsyringe",
    "passport", "passport-local", "passport-jwt",
}

_FORBIDDEN_PACKAGES = {
    "request": ("Use undici or node-fetch instead", "deprecated and unmaintained since 2020"),
    "node-uuid": ("Use uuid or nanoid instead", "renamed to uuid; this is a phantom/old alias"),
    "event-stream": ("No safe alternative — avoid stream manipulation packages", "used in supply chain attack 2018"),
    "colors.js": ("Use chalk instead", "author sabotaged package in 2022 protest"),
    "faker.js": ("Use @faker-js/faker instead", "author deleted and sabotaged package 2022"),
    "crossenv": ("Use cross-env instead", "typosquat of cross-env used to steal credentials"),
    "lodahs": ("Use lodash instead", "typosquat of lodash"),
    "loadsh": ("Use lodash instead", "typosquat of lodash"),
    "pino-logger": ("Use pino instead", "unnecessary wrapper with unknown maintainer"),
}

_KNOWN_TYPOSQUATS = {
    "expresss": "express",
    "mongooze": "mongoose",
    "requiest": "undici",
    "brcyptjs": "bcryptjs",
    "jsonwebtokken": "jsonwebtoken",
    "helmt": "helmet",
    "undicii": "undici",
    "cros": "cors",
    "dotenvs": "dotenv",
    "axois": "axios",
    "jst": "jest",
}

_SUSPICIOUS_PATTERNS = [
    re.compile(r"^node-[a-z]+-[a-z]+$"),
    re.compile(r".*(hack|steal|exfil|bypass|spoof|inject|exploit).*", re.IGNORECASE),
    re.compile(r"^[a-z]{1,3}$"),
    re.compile(r".*-js-[a-z]+$"),
    re.compile(r".*_[a-z]+_.*"),
]

_DEPRECATED_KNOWN = {
    "request", "request-promise", "node-uuid", "jade", "coffee-script",
    "bower", "grunt", "gulp", "forever", "q", "bluebird",
}


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def _detect_typosquat(name: str) -> Tuple[bool, str, float]:
    for trusted in _TRUSTED_PACKAGES:
        sim = _similarity(name, trusted)
        if 0.80 <= sim < 1.0 and name != trusted:
            return True, trusted, sim
    return False, "", 0.0


def _audit_single(name: str) -> PackageResult:
    name_clean = name.strip().lower()

    if name_clean in _KNOWN_TYPOSQUATS:
        trusted = _KNOWN_TYPOSQUATS[name_clean]
        return PackageResult(
            name=name,
            risk=PackageRisk.TYPOSQUAT,
            reason=f"Known typosquat of '{trusted}' — possible credential-harvesting package",
            safe_alternative=trusted,
            confidence=1.0,
        )

    if name_clean in _FORBIDDEN_PACKAGES:
        alt, reason = _FORBIDDEN_PACKAGES[name_clean]
        return PackageResult(
            name=name,
            risk=PackageRisk.DANGEROUS,
            reason=f"Explicitly forbidden: {reason}",
            safe_alternative=alt,
            confidence=1.0,
        )

    if name_clean in _TRUSTED_PACKAGES:
        return PackageResult(
            name=name,
            risk=PackageRisk.SAFE,
            reason="Package is on the KRONOS trusted allowlist",
            confidence=1.0,
        )

    is_typo, matched, sim = _detect_typosquat(name_clean)
    if is_typo:
        return PackageResult(
            name=name,
            risk=PackageRisk.TYPOSQUAT,
            reason=f"Highly similar to trusted package '{matched}' (similarity: {sim:.0%}) — possible typosquat",
            safe_alternative=matched,
            confidence=round(sim, 2),
        )

    if name_clean in _DEPRECATED_KNOWN:
        return PackageResult(
            name=name,
            risk=PackageRisk.DEPRECATED,
            reason="Package is known-deprecated and should not be used in new projects",
            confidence=0.95,
        )

    for pattern in _SUSPICIOUS_PATTERNS:
        if pattern.match(name_clean):
            return PackageResult(
                name=name,
                risk=PackageRisk.SUSPICIOUS,
                reason="Package name matches a suspicious naming pattern — manual review required",
                confidence=0.7,
            )

    return PackageResult(
        name=name,
        risk=PackageRisk.UNKNOWN,
        reason="Package not found on KRONOS allowlist — not trusted, not forbidden. Verify before use.",
        confidence=0.5,
    )


def audit_packages(request: PackageAuditRequest) -> PackageAuditResponse:
    audit_id = f"KAU-{uuid.uuid4().hex[:12].upper()}"
    audited_at = datetime.now(timezone.utc).isoformat()

    results = [_audit_single(pkg) for pkg in request.packages]

    safe_count = sum(1 for r in results if r.risk == PackageRisk.SAFE)
    dangerous_count = sum(1 for r in results if r.risk in (PackageRisk.DANGEROUS, PackageRisk.TYPOSQUAT))
    flagged_count = sum(1 for r in results if r.risk != PackageRisk.SAFE)

    if dangerous_count > 0:
        verdict = "FAIL — dangerous or typosquatted packages detected. Do NOT install."
    elif flagged_count > len(results) // 2:
        verdict = "WARN — majority of packages are unverified. Review before installation."
    else:
        verdict = "PASS — all audited packages are safe or low-risk."

    recommendations: List[str] = []
    for r in results:
        if r.safe_alternative:
            recommendations.append(f"Replace '{r.name}' with '{r.safe_alternative}'")
    if not recommendations:
        recommendations.append("All packages passed — keep dependency list minimal and versioned.")

    return PackageAuditResponse(
        audit_id=audit_id,
        audited_at=audited_at,
        results=results,
        summary=AuditSummary(
            total=len(results),
            safe=safe_count,
            flagged=flagged_count,
            dangerous=dangerous_count,
            overall_verdict=verdict,
        ),
        recommendations=recommendations,
    )
