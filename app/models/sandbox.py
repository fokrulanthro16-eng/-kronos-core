from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class SandboxVerdict(str, Enum):
    CLEAN = "CLEAN"
    SUSPICIOUS = "SUSPICIOUS"
    BLOCKED = "BLOCKED"


class ProcessSummary(BaseModel):
    total_processes: int
    high_cpu_processes: int
    suspicious_processes: List[str]


class NetworkSummary(BaseModel):
    open_connections: int
    suspicious_destinations: List[str]
    blocked_connections: int
    exfiltration_risk: bool


class FileSummary(BaseModel):
    writable_sensitive_paths: int
    risk_level: str


class SandboxInspectionResponse(BaseModel):
    inspection_id: str
    inspected_at: str
    demo_mode: bool
    process_summary: ProcessSummary
    network_summary: NetworkSummary
    file_summary: FileSummary
    verdict: SandboxVerdict
    findings: List[str]
    passed_checks: List[str]
    blocked_actions: List[str]
    executive_note: str
