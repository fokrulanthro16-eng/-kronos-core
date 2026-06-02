import socket
from typing import Any, Dict, List, Optional, Tuple

import psutil

from app.core.logging import get_logger

logger = get_logger(__name__)

# Ports associated with C2 frameworks, cryptominers, IRC botnets, and known backdoors
_SUSPICIOUS_PORTS = frozenset({
    4444, 4445, 4446,       # Metasploit / Meterpreter defaults
    31337,                   # Elite hacker / BackOrifice
    1337,                    # Common backdoor port
    6666, 6667, 6668, 6669, # IRC botnet C2
    3333, 5555, 7777,        # Cryptominer pool ports
    8088, 9999,              # Uncommon high-ports used by RATs
    65535,                   # Max port — often used to evade simple filters
})

_FAMILY_MAP: Dict[int, str] = {
    socket.AF_INET: "IPv4",
    socket.AF_INET6: "IPv6",
}
if hasattr(socket, "AF_UNIX"):
    _FAMILY_MAP[socket.AF_UNIX] = "Unix"

_TYPE_MAP: Dict[int, str] = {
    socket.SOCK_STREAM: "TCP",
    socket.SOCK_DGRAM: "UDP",
}


def _suspicious(conn: Any) -> Tuple[bool, Optional[str]]:
    if conn.raddr:
        rport = getattr(conn.raddr, "port", 0)
        if rport in _SUSPICIOUS_PORTS:
            return True, f"Active connection to suspicious remote port {rport}"
    if conn.laddr:
        lport = getattr(conn.laddr, "port", 0)
        if lport in _SUSPICIOUS_PORTS:
            return True, f"Service listening on suspicious port {lport}"
    return False, None


def _fmt_addr(addr) -> Optional[str]:
    if not addr:
        return None
    return f"{addr.ip}:{addr.port}" if hasattr(addr, "ip") else str(addr)


def _proc_name(pid: Optional[int]) -> Optional[str]:
    if not pid:
        return None
    try:
        return psutil.Process(pid).name()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return "unknown"


def inspect_sockets() -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    try:
        for conn in psutil.net_connections(kind="all"):
            is_sus, reason = _suspicious(conn)
            results.append({
                "fd": conn.fd,
                "family": _FAMILY_MAP.get(conn.family, str(conn.family)),
                "type": _TYPE_MAP.get(conn.type, str(conn.type)),
                "local_addr": _fmt_addr(conn.laddr),
                "remote_addr": _fmt_addr(conn.raddr),
                "status": getattr(conn, "status", None),
                "pid": conn.pid,
                "process_name": _proc_name(conn.pid),
                "suspicious": is_sus,
                "reason": reason,
            })
    except psutil.AccessDenied as exc:
        logger.warning("socket_inspect_access_denied", error=str(exc))
    except PermissionError as exc:
        logger.warning("socket_inspect_permission_error", error=str(exc))
    except Exception as exc:
        logger.error("socket_inspect_error", error=str(exc))
    return results


def get_suspicious_connections() -> List[Dict[str, Any]]:
    return [c for c in inspect_sockets() if c["suspicious"]]
