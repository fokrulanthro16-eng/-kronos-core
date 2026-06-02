import json

from fastapi import APIRouter, Depends, HTTPException, Request

from app.dependencies import get_request_id, verify_api_key
from app.limiter import limiter
from app.models.audit import (
    AuditResult,
    BulkAuditResult,
    LockfileRequest,
    PackageRequest,
    PackagesRequest,
)
from app.models.responses import APIResponse
from app.services import allowlist as allowlist_svc
from app.services import npm_audit
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post(
    "/package",
    response_model=APIResponse[AuditResult],
    summary="Audit a single npm package",
)
@limiter.limit("30/minute")
async def audit_package(
    request: Request,
    pkg: PackageRequest,
    _: None = Depends(verify_api_key),
) -> APIResponse[AuditResult]:
    req_id = get_request_id(request)
    result = await npm_audit.audit_package(pkg.name, pkg.version)
    logger.info("audit_done", package=pkg.name, risk=result.risk_level, score=result.score)
    return APIResponse(request_id=req_id, data=result)


@router.post(
    "/packages",
    response_model=APIResponse[BulkAuditResult],
    summary="Audit multiple npm packages in bulk",
)
@limiter.limit("10/minute")
async def audit_packages(
    request: Request,
    body: PackagesRequest,
    _: None = Depends(verify_api_key),
) -> APIResponse[BulkAuditResult]:
    req_id = get_request_id(request)
    results = [await npm_audit.audit_package(p.name, p.version) for p in body.packages]
    bulk = BulkAuditResult(
        total=len(results),
        safe=sum(1 for r in results if r.risk_level == "safe"),
        warned=sum(1 for r in results if r.warnings and not r.blocked),
        blocked=sum(1 for r in results if r.blocked),
        results=results,
    )
    return APIResponse(request_id=req_id, data=bulk)


@router.post(
    "/lockfile",
    response_model=APIResponse[BulkAuditResult],
    summary="Audit all packages declared in a package-lock.json or yarn.lock",
)
@limiter.limit("5/minute")
async def audit_lockfile(
    request: Request,
    body: LockfileRequest,
    _: None = Depends(verify_api_key),
) -> APIResponse[BulkAuditResult]:
    req_id = get_request_id(request)
    packages: list[PackageRequest] = []

    if "package-lock.json" in body.filename:
        try:
            data = json.loads(body.content)
        except json.JSONDecodeError:
            raise HTTPException(400, "Invalid JSON in package-lock.json")

        deps = data.get("packages", data.get("dependencies", {}))
        for raw_name, pkg_info in deps.items():
            name = raw_name.replace("node_modules/", "", 1) if raw_name.startswith("node_modules/") else raw_name
            if not name or name.startswith("//"):
                continue
            version = pkg_info.get("version") if isinstance(pkg_info, dict) else None
            try:
                packages.append(PackageRequest(name=name, version=version))
            except Exception:
                continue

    elif "yarn.lock" in body.filename:
        for line in body.content.splitlines():
            stripped = line.strip()
            if stripped.endswith(":") and not stripped.startswith("#") and not stripped.startswith(" "):
                raw_name = stripped.rstrip(":").split("@")[0].strip('"')
                if raw_name:
                    try:
                        packages.append(PackageRequest(name=raw_name))
                    except Exception:
                        continue
    else:
        raise HTTPException(400, "Unsupported lockfile — submit package-lock.json or yarn.lock")

    if not packages:
        raise HTTPException(400, "No packages parsed from lockfile")
    if len(packages) > 200:
        raise HTTPException(400, "Lockfile too large — maximum 200 packages per scan")

    results = [await npm_audit.audit_package(p.name, p.version) for p in packages[:50]]
    bulk = BulkAuditResult(
        total=len(results),
        safe=sum(1 for r in results if r.risk_level == "safe"),
        warned=sum(1 for r in results if r.warnings and not r.blocked),
        blocked=sum(1 for r in results if r.blocked),
        results=results,
    )
    return APIResponse(request_id=req_id, data=bulk)


@router.get(
    "/allowlist",
    response_model=APIResponse[dict],
    summary="Return the current approved package allowlist",
)
async def get_allowlist(
    request: Request,
    _: None = Depends(verify_api_key),
) -> APIResponse[dict]:
    req_id = get_request_id(request)
    packages = allowlist_svc.get_allowlist()
    return APIResponse(
        request_id=req_id,
        data={"packages": packages, "count": len(packages)},
    )
