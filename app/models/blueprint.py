from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class BlueprintRequest(BaseModel):
    objective: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Raw project objective to convert into a secure execution blueprint",
        examples=["Build a REST API for a fintech payment processing system with JWT auth"],
    )
    tech_stack: Optional[str] = Field(
        default="Node.js",
        max_length=200,
        description="Target technology stack",
    )
    sensitivity_level: Optional[str] = Field(
        default="HIGH",
        description="Data sensitivity level: LOW, MEDIUM, HIGH, CRITICAL",
    )


class DirectoryNode(BaseModel):
    path: str
    purpose: str


class PackagePolicy(BaseModel):
    allowed: List[str]
    forbidden: List[str]
    audit_command: str


class RiskScore(BaseModel):
    overall: int = Field(..., ge=0, le=100)
    level: RiskLevel
    prompt_safety: int
    package_safety: int
    runtime_isolation: int
    data_exfiltration_protection: int


class BlueprintResponse(BaseModel):
    blueprint_id: str
    generated_at: str
    objective_summary: str
    directory_architecture: List[DirectoryNode]
    secure_coding_standards: List[str]
    package_policy: PackagePolicy
    static_audit_instructions: List[str]
    dynamic_sandbox_instructions: List[str]
    deployment_checklist: List[str]
    business_demo_explanation: str
    risk_score: RiskScore
    production_readiness_checklist: List[str]
    claude_execution_prompt: str
