from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class PackageRisk(str, Enum):
    SAFE = "SAFE"
    UNKNOWN = "UNKNOWN"
    SUSPICIOUS = "SUSPICIOUS"
    DANGEROUS = "DANGEROUS"
    TYPOSQUAT = "TYPOSQUAT"
    PHANTOM = "PHANTOM"
    DEPRECATED = "DEPRECATED"


class PackageAuditRequest(BaseModel):
    packages: List[str] = Field(
        ...,
        min_length=1,
        max_length=50,
        description="List of npm package names to audit",
        examples=[["express", "helmet", "expresss", "lodahs"]],
    )


class PackageResult(BaseModel):
    name: str
    risk: PackageRisk
    reason: str
    safe_alternative: Optional[str] = None
    confidence: float = Field(..., ge=0.0, le=1.0)


class AuditSummary(BaseModel):
    total: int
    safe: int
    flagged: int
    dangerous: int
    overall_verdict: str


class PackageAuditResponse(BaseModel):
    audit_id: str
    audited_at: str
    results: List[PackageResult]
    summary: AuditSummary
    recommendations: List[str]
