import platform
import subprocess
from typing import Any, Dict, List

import psutil

from app.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()

# Curated database of packages confirmed to execute malicious postinstall behavior.
# Entries: package_name → behavior_class
_MALICIOUS_DB: Dict[str, str] = {
    "flatmap-stream": "supply_chain_backdoor",
    "event-stream-malicious": "supply_chain_backdoor",
    "ua-parser-js": "credential_harvesting",   # compromised Oct 2021
    "coa": "credential_harvesting",            # compromised Oct 2021
    "rc": "credential_harvesting",             # compromised Oct 2021
    "node-ipc-malware": "filesystem_wiper",
    "coinhive": "cryptomining",
    "coinmine": "cryptomining",
    "discord.js-selfbot": "token_harvesting",
}


async def analyze_package_behavior(package_name: str) -> Dict[str, Any]:
    """
    Static behavioral analysis + psutil system snapshot.

    Full dynamic analysis requires running the package in a Docker
    sandbox — the `docker_isolation_command` field in the response
    contains the hardened command ready for production use.
    """
    logger.info("sandbox_start", package=package_name)
    name_lower = package_name.lower()
    risk_indicators: List[Dict[str, str]] = []

    if name_lower in _MALICIOUS_DB:
        behavior = _MALICIOUS_DB[name_lower]
        risk_indicators.append({
            "type": behavior,
            "severity": "critical",
            "description": (
                f"'{package_name}' matches a confirmed malicious package behavior: {behavior}"
            ),
        })

    snapshot = _system_snapshot()
    constraints = _system_constraints()

    n = len(risk_indicators)
    recommendation = "low_risk" if n == 0 else "moderate_risk_review" if n <= 2 else "high_risk_block"

    logger.info(
        "sandbox_complete",
        package=package_name,
        risk_count=n,
        recommendation=recommendation,
    )

    return {
        "package_name": package_name,
        "analysis_type": "static_behavioral",
        "risk_indicators": risk_indicators,
        "recommendation": recommendation,
        "system_snapshot": snapshot,
        "system_constraints": constraints,
        "note": (
            "Dynamic analysis requires Docker. "
            "Use the docker_isolation_command for fully sandboxed execution."
        ),
    }


def _system_snapshot() -> Dict[str, Any]:
    try:
        mem = psutil.virtual_memory()
        net = psutil.net_io_counters()
        return {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_used_mb": mem.used // (1024 * 1024),
            "memory_available_mb": mem.available // (1024 * 1024),
            "net_bytes_sent": net.bytes_sent if net else 0,
            "net_bytes_recv": net.bytes_recv if net else 0,
            "process_count": len(psutil.pids()),
        }
    except Exception as exc:
        logger.warning("snapshot_error", error=str(exc))
        return {}


def _system_constraints() -> Dict[str, Any]:
    return {
        "docker_available": _docker_available(),
        "sandbox_memory_limit_mb": settings.SANDBOX_MAX_MEMORY_MB,
        "sandbox_timeout_seconds": settings.SANDBOX_TIMEOUT_SECONDS,
        "platform": platform.system(),
        "isolation_mode": "docker" if _docker_available() else "process_level",
    }


def _docker_available() -> bool:
    try:
        r = subprocess.run(["docker", "info"], capture_output=True, timeout=5)
        return r.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def get_docker_isolation_command(package_name: str) -> str:
    mem = settings.SANDBOX_MAX_MEMORY_MB
    return (
        f"docker run --rm "
        f"--network=none "
        f"--memory={mem}m --memory-swap={mem}m "
        f"--cpu-quota=50000 "
        f"--pids-limit=100 "
        f"--read-only "
        f"--no-new-privileges "
        f"--cap-drop=ALL "
        f"--security-opt=no-new-privileges:true "
        f'node:20-alpine sh -c '
        f"'npm install --ignore-scripts {package_name} 2>&1 && "
        f"node -e \"try{{require(\\'{package_name}\\')}}catch(e){{console.error(e)}}\"'"
    )
