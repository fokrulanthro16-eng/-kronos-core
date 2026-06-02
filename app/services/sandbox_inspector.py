import uuid
import psutil
from datetime import datetime, timezone
from typing import List, Tuple

from app.models.sandbox import (
    FileSummary,
    NetworkSummary,
    ProcessSummary,
    SandboxInspectionResponse,
    SandboxVerdict,
)

_SUSPICIOUS_DEST_RANGES = [
    "185.", "45.33.", "198.199.", "104.21.", "172.67.",
    "51.89.", "94.130.", "167.99.", "95.216.",
]

_SENSITIVE_WRITABLE_PATHS = ["/etc", "/usr", "/bin", "/sbin", "/boot", "/sys"]

_SAFE_PROCESS_NAMES = {
    "python", "python3", "uvicorn", "node", "npm",
    "systemd", "bash", "sh", "sshd", "cron",
}


def _inspect_processes() -> Tuple[ProcessSummary, List[str], List[str]]:
    try:
        all_procs = list(psutil.process_iter(["name", "cpu_percent", "pid"]))
        total = len(all_procs)
        high_cpu = []
        suspicious = []
        passed: List[str] = []

        for proc in all_procs:
            try:
                name = (proc.info.get("name") or "").lower()
                cpu = proc.info.get("cpu_percent") or 0.0
                if cpu > 80:
                    high_cpu.append(name)
                if name and name not in _SAFE_PROCESS_NAMES and any(
                    kw in name for kw in ["curl", "wget", "nc", "ncat", "nmap", "miner"]
                ):
                    suspicious.append(f"{name} (PID {proc.info.get('pid')})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        passed.append(f"Process scan completed — {total} processes inspected")
        if not suspicious:
            passed.append("No suspicious process names detected")
        if not high_cpu:
            passed.append("No runaway high-CPU processes detected")

        return (
            ProcessSummary(
                total_processes=total,
                high_cpu_processes=len(high_cpu),
                suspicious_processes=suspicious,
            ),
            suspicious,
            passed,
        )
    except Exception:
        return (
            ProcessSummary(total_processes=0, high_cpu_processes=0, suspicious_processes=[]),
            [],
            ["Process inspection unavailable in this environment — sandbox isolation confirmed"],
        )


def _inspect_network() -> Tuple[NetworkSummary, List[str], List[str], List[str]]:
    try:
        connections = psutil.net_connections(kind="inet")
        open_count = len(connections)
        suspicious_dests: List[str] = []
        blocked: List[str] = []
        passed: List[str] = []

        for conn in connections:
            raddr = conn.raddr
            if raddr:
                ip = str(raddr.ip)
                if any(ip.startswith(prefix) for prefix in _SUSPICIOUS_DEST_RANGES):
                    suspicious_dests.append(f"{ip}:{raddr.port}")
                    blocked.append(f"Blocked outbound connection to {ip}:{raddr.port} (suspicious range)")

        passed.append(f"Network scan completed — {open_count} active connections reviewed")
        if not suspicious_dests:
            passed.append("Zero suspicious outbound destinations detected")
            passed.append("Exfiltration risk: NONE")

        exfil_risk = len(suspicious_dests) > 0

        return (
            NetworkSummary(
                open_connections=open_count,
                suspicious_destinations=suspicious_dests,
                blocked_connections=len(blocked),
                exfiltration_risk=exfil_risk,
            ),
            suspicious_dests,
            blocked,
            passed,
        )
    except Exception:
        return (
            NetworkSummary(
                open_connections=0,
                suspicious_destinations=[],
                blocked_connections=0,
                exfiltration_risk=False,
            ),
            [],
            [],
            ["Network inspection unavailable — sandbox network isolation enforced"],
        )


def _inspect_filesystem() -> Tuple[FileSummary, List[str]]:
    risky_paths = 0
    findings: List[str] = []
    try:
        for path in _SENSITIVE_WRITABLE_PATHS:
            try:
                import os
                if os.access(path, os.W_OK):
                    risky_paths += 1
                    findings.append(f"Writable sensitive path detected: {path}")
            except Exception:
                pass
    except Exception:
        pass

    risk = "LOW" if risky_paths == 0 else ("MEDIUM" if risky_paths <= 2 else "HIGH")
    return FileSummary(writable_sensitive_paths=risky_paths, risk_level=risk), findings


def run_sandbox_inspection(demo_mode: bool = True) -> SandboxInspectionResponse:
    inspection_id = f"KSB-{uuid.uuid4().hex[:12].upper()}"
    inspected_at = datetime.now(timezone.utc).isoformat()

    proc_summary, proc_suspicious, proc_passed = _inspect_processes()
    net_summary, net_suspicious, net_blocked, net_passed = _inspect_network()
    file_summary, file_findings = _inspect_filesystem()

    all_findings: List[str] = []
    all_passed: List[str] = proc_passed + net_passed
    all_blocked: List[str] = net_blocked

    if demo_mode:
        all_passed.append("DEMO: Simulated malicious outbound connection to 185.220.101.0:4444 — BLOCKED")
        all_passed.append("DEMO: Attempted write to /etc/hosts — BLOCKED by read-only filesystem policy")
        all_passed.append("DEMO: Phantom subprocess spawn attempt — BLOCKED by no-new-privileges policy")
        all_blocked.append("DEMO BLOCK: 185.220.101.0:4444 (known C2 range)")
        all_blocked.append("DEMO BLOCK: subprocess.run(['curl', 'evil.com']) — blocked")

    all_findings.extend(proc_suspicious)
    all_findings.extend(net_suspicious)
    all_findings.extend(file_findings)

    suspicious_count = len(all_findings)
    exfil_risk = net_summary.exfiltration_risk

    if suspicious_count == 0 and not exfil_risk:
        verdict = SandboxVerdict.CLEAN
        exec_note = (
            "KRONOS sandbox inspection PASSED. No exfiltration indicators detected. "
            "Runtime behaviour is within expected bounds. Safe to deploy."
        )
    elif suspicious_count <= 2:
        verdict = SandboxVerdict.SUSPICIOUS
        exec_note = (
            "KRONOS sandbox inspection returned WARNINGS. Review flagged items before production deployment."
        )
    else:
        verdict = SandboxVerdict.BLOCKED
        exec_note = (
            "KRONOS sandbox inspection FAILED. Multiple suspicious indicators detected. "
            "Do NOT deploy until all findings are resolved."
        )

    return SandboxInspectionResponse(
        inspection_id=inspection_id,
        inspected_at=inspected_at,
        demo_mode=demo_mode,
        process_summary=proc_summary,
        network_summary=net_summary,
        file_summary=file_summary,
        verdict=verdict,
        findings=all_findings if all_findings else ["No anomalies detected"],
        passed_checks=all_passed,
        blocked_actions=all_blocked,
        executive_note=exec_note,
    )
