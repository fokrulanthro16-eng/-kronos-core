const BASE = "/api/v1";

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${BASE}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...init,
    });
  } catch {
    throw new ApiError(0, "Cannot reach KRONOS CORE backend (is it running on port 8000?)");
  }
  if (!res.ok) {
    const body = await res.json().catch(() => ({ error: res.statusText }));
    throw new ApiError(res.status, body.error ?? res.statusText);
  }
  return res.json() as Promise<T>;
}

export const api = {
  health: () => req<HealthResponse>("/health"),
  demo: () => req<DemoResponse>("/demo"),
  enterprise: () => req<EnterpriseResponse>("/enterprise/report"),
  sandbox: (demo = true) => req<SandboxResponse>(`/sandbox?demo=${demo}`),
  blueprint: (body: BlueprintRequest) =>
    req<BlueprintResponse>("/blueprint", { method: "POST", body: JSON.stringify(body) }),
  audit: (packages: string[]) =>
    req<AuditResponse>("/audit", { method: "POST", body: JSON.stringify({ packages }) }),
  securityScore: (body: ScoreRequest) =>
    req<ScoreResponse>("/security/score", { method: "POST", body: JSON.stringify(body) }),
  saasStatus: () => req<SaasStatusResponse>("/saas/status"),
  saasSchema: () => req<SaasSchemaResponse>("/saas/schema"),
  authStatus: () => req<AuthStatusResponse>("/auth/status"),
};

// ── Types ────────────────────────────────────────────────────────────────────

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  environment: string;
  timestamp: string;
}

export interface DemoResponse {
  product_name: string;
  tagline: string;
  problem_statement: string;
  solution: string;
  target_customers: { segment: string; pain_point: string; value_delivered: string }[];
  market_use_cases: string[];
  technical_innovation: string[];
  security_architecture: { layer: string; component: string; security_role: string }[];
  demo_flow: string[];
  commercial_value: string;
  competition_advantage: string;
  future_roadmap: { phase: string; feature: string; business_impact: string }[];
  pitch_closing: string;
}

export interface EnterpriseResponse {
  report_id: string;
  generated_at: string;
  product: string;
  executive_summary: string;
  capabilities: string[];
  compliance_alignment: string[];
  integration_options: string[];
  deployment_models: string[];
  pricing_model: string;
  support_model: string;
  references: string[];
}

export interface SandboxResponse {
  inspection_id: string;
  inspected_at: string;
  demo_mode: boolean;
  process_summary: { total_processes: number; high_cpu_processes: number; suspicious_processes: string[] };
  network_summary: { open_connections: number; suspicious_destinations: string[]; blocked_connections: number; exfiltration_risk: boolean };
  file_summary: { writable_sensitive_paths: number; risk_level: string };
  verdict: "CLEAN" | "SUSPICIOUS" | "BLOCKED";
  findings: string[];
  passed_checks: string[];
  blocked_actions: string[];
  executive_note: string;
}

export interface BlueprintRequest {
  objective: string;
  tech_stack?: string;
  sensitivity_level?: string;
}

export interface BlueprintResponse {
  blueprint_id: string;
  generated_at: string;
  objective_summary: string;
  directory_architecture: { path: string; purpose: string }[];
  secure_coding_standards: string[];
  package_policy: { allowed: string[]; forbidden: string[]; audit_command: string };
  static_audit_instructions: string[];
  dynamic_sandbox_instructions: string[];
  deployment_checklist: string[];
  business_demo_explanation: string;
  risk_score: { overall: number; level: string; prompt_safety: number; package_safety: number; runtime_isolation: number; data_exfiltration_protection: number };
  production_readiness_checklist: string[];
  claude_execution_prompt: string;
}

export interface AuditResponse {
  audit_id: string;
  audited_at: string;
  results: { name: string; risk: string; reason: string; safe_alternative: string | null; confidence: number }[];
  summary: { total: number; safe: number; flagged: number; dangerous: number; overall_verdict: string };
  recommendations: string[];
}

export interface ScoreRequest {
  packages_audited: number;
  packages_flagged: number;
  sandbox_passed: boolean;
  blueprint_generated: boolean;
  docker_hardened: boolean;
  input_validation: boolean;
  auth_implemented: boolean;
  tls_enabled: boolean;
}

export interface ScoreResponse {
  score_id: string;
  scored_at: string;
  total_score: number;
  risk_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  categories: { name: string; score: number; max_score: number; status: string; findings: string[] }[];
  recommendations: string[];
  executive_summary: string;
  enterprise_ready: boolean;
}

export interface SaasFeatureStatus {
  feature: string;
  status: "configured" | "not_configured" | "planned" | "active";
  description: string;
  phase: string;
}

export interface SaasStatusResponse {
  saas_mode: boolean;
  database_configured: boolean;
  auth_configured: boolean;
  supabase_url_set: boolean;
  supabase_keys_set: boolean;
  jwt_secret_set: boolean;
  features: SaasFeatureStatus[];
  message: string;
}

export interface SaasSchemaTable {
  table: string;
  description: string;
  key_columns: string[];
  phase: string;
}

export interface SaasSchemaResponse {
  schema_version: string;
  database: string;
  tables: SaasSchemaTable[];
  rls_enabled: boolean;
  migration_file: string;
}

export interface AuthStatusResponse {
  auth_configured: boolean;
  supabase_url_configured: boolean;
  anon_key_configured: boolean;
  service_role_configured: boolean;
  jwt_secret_configured: boolean;
  mode: "configured" | "demo";
  message: string;
}
