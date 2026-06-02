from pydantic import BaseModel, Field
from typing import List
from enum import Enum


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ScoreCategory(BaseModel):
    name: str
    score: int = Field(..., ge=0, le=20)
    max_score: int = 20
    status: str
    findings: List[str]


class SecurityScoreRequest(BaseModel):
    packages_audited: int = Field(default=0, ge=0)
    packages_flagged: int = Field(default=0, ge=0)
    sandbox_passed: bool = Field(default=True)
    blueprint_generated: bool = Field(default=True)
    docker_hardened: bool = Field(default=True)
    input_validation: bool = Field(default=True)
    auth_implemented: bool = Field(default=False)
    tls_enabled: bool = Field(default=False)


class SecurityScoreResponse(BaseModel):
    score_id: str
    scored_at: str
    total_score: int = Field(..., ge=0, le=100)
    risk_level: RiskLevel
    categories: List[ScoreCategory]
    recommendations: List[str]
    executive_summary: str
    enterprise_ready: bool
