from pydantic import BaseModel
from typing import List


class TargetCustomer(BaseModel):
    segment: str
    pain_point: str
    value_delivered: str


class TechLayer(BaseModel):
    layer: str
    component: str
    security_role: str


class RoadmapItem(BaseModel):
    phase: str
    feature: str
    business_impact: str


class CompetitionDemoResponse(BaseModel):
    product_name: str
    tagline: str
    problem_statement: str
    solution: str
    target_customers: List[TargetCustomer]
    market_use_cases: List[str]
    technical_innovation: List[str]
    security_architecture: List[TechLayer]
    demo_flow: List[str]
    commercial_value: str
    competition_advantage: str
    future_roadmap: List[RoadmapItem]
    pitch_closing: str


class EnterpriseReportResponse(BaseModel):
    report_id: str
    generated_at: str
    product: str
    executive_summary: str
    capabilities: List[str]
    compliance_alignment: List[str]
    integration_options: List[str]
    deployment_models: List[str]
    pricing_model: str
    support_model: str
    references: List[str]
