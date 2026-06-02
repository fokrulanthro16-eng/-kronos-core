"""
SaaS data models — request/response schemas for Phase 1 status endpoints
and the data shapes that will be persisted in Phase 2+.
"""
from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel


# ── Status / introspection ────────────────────────────────────────────────────

class SaasFeatureStatus(BaseModel):
    feature: str
    status: str           # "configured" | "not_configured" | "planned" | "active"
    description: str
    phase: str


class SaasStatusResponse(BaseModel):
    saas_mode: bool
    database_configured: bool
    auth_configured: bool
    supabase_url_set: bool
    supabase_keys_set: bool
    jwt_secret_set: bool
    features: List[SaasFeatureStatus]
    message: str


class SaasSchemaTable(BaseModel):
    table: str
    description: str
    key_columns: List[str]
    phase: str


class SaasSchemaResponse(BaseModel):
    schema_version: str
    database: str
    tables: List[SaasSchemaTable]
    rls_enabled: bool
    migration_file: str


# ── Stored-report shapes (used in Phase 2+ persistence) ──────────────────────

class StoredBlueprintRecord(BaseModel):
    id: Optional[str] = None
    organization_id: Optional[str] = None
    user_id: Optional[str] = None
    objective: str
    generated_blueprint: dict
    risk_score: int
    risk_level: str


class StoredAuditRecord(BaseModel):
    id: Optional[str] = None
    organization_id: Optional[str] = None
    user_id: Optional[str] = None
    package_names: List[str]
    audit_result_json: dict
    overall_verdict: str
    flagged_count: int
    dangerous_count: int


class StoredSandboxRecord(BaseModel):
    id: Optional[str] = None
    organization_id: Optional[str] = None
    user_id: Optional[str] = None
    sandbox_result_json: dict
    verdict: str
    demo_mode: bool


class StoredEnterpriseReportRecord(BaseModel):
    id: Optional[str] = None
    organization_id: Optional[str] = None
    user_id: Optional[str] = None
    report_json: dict
    security_score: int
    risk_level: str
    enterprise_ready: bool
