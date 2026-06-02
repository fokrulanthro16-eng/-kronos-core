"use client";

import { useEffect, useState } from "react";
import {
  Database, Shield, Users, FileText, CreditCard,
  LayoutDashboard, Globe, CheckCircle, Clock, AlertTriangle,
  RefreshCw, Server,
} from "lucide-react";
import { api, AuthStatusResponse } from "@/lib/api";
import { supabaseConfigured } from "@/lib/auth";

// ── Types ─────────────────────────────────────────────────────────────────────

interface FeatureStatus {
  feature: string;
  status: "configured" | "not_configured" | "planned" | "active";
  description: string;
  phase: string;
}

interface SaasStatus {
  saas_mode: boolean;
  database_configured: boolean;
  auth_configured: boolean;
  supabase_url_set: boolean;
  supabase_keys_set: boolean;
  jwt_secret_set: boolean;
  features: FeatureStatus[];
  message: string;
}

// ── Phase roadmap (static, always shown) ─────────────────────────────────────

const PHASES = [
  {
    phase: "Phase 1",
    title: "Auth + Database Foundation",
    icon: Database,
    color: "text-[#00ff88]",
    border: "border-[#00ff88]/20",
    bg: "bg-[#00ff88]/5",
    status: "complete",
    items: [
      "Supabase project configuration",
      "PostgreSQL schema (8 tables)",
      "Row-level security policies",
      "Supabase client adapter",
      "JWT auth dependency (passthrough mode)",
      "SaaS status API endpoints",
      "Report store service stubs",
      "Organisation service stubs",
    ],
  },
  {
    phase: "Phase 2",
    title: "User Login & Registration",
    icon: Shield,
    color: "text-blue-400",
    border: "border-blue-400/20",
    bg: "bg-blue-400/5",
    status: "planned",
    items: [
      "Email/password sign-up and login",
      "Supabase Auth integration",
      "Protected endpoints with JWT",
      "User profile management",
      "Organisation creation flow",
      "Session persistence in Next.js",
    ],
  },
  {
    phase: "Phase 3",
    title: "Saved Audit History",
    icon: FileText,
    color: "text-purple-400",
    border: "border-purple-400/20",
    bg: "bg-purple-400/5",
    status: "planned",
    items: [
      "Persist blueprint results to database",
      "Persist npm audit results",
      "Persist sandbox inspection results",
      "Persist enterprise report results",
      "History page with paginated records",
      "Re-view any saved report",
    ],
  },
  {
    phase: "Phase 4",
    title: "PDF Export",
    icon: FileText,
    color: "text-yellow-400",
    border: "border-yellow-400/20",
    bg: "bg-yellow-400/5",
    status: "planned",
    items: [
      "Download enterprise report as branded PDF",
      "Report includes compliance alignment tables",
      "Signed with unique report ID",
      "Retrievable from history by ID",
    ],
  },
  {
    phase: "Phase 5",
    title: "Stripe Subscription Billing",
    icon: CreditCard,
    color: "text-pink-400",
    border: "border-pink-400/20",
    bg: "bg-pink-400/5",
    status: "planned",
    items: [
      "Starter / Team / Enterprise pricing tiers",
      "Stripe Checkout integration",
      "Stripe Customer Portal",
      "Webhook handler for subscription events",
      "Plan-based rate limits",
    ],
  },
  {
    phase: "Phase 6",
    title: "Organisation Workspace",
    icon: Users,
    color: "text-orange-400",
    border: "border-orange-400/20",
    bg: "bg-orange-400/5",
    status: "planned",
    items: [
      "Invite team members by email",
      "Role-based access: Owner / Admin / Member / Viewer",
      "Custom package allowlist per organisation",
      "Usage metrics dashboard",
      "Monthly audit / blueprint consumption stats",
    ],
  },
  {
    phase: "Phase 7",
    title: "Production Deployment",
    icon: Globe,
    color: "text-cyan-400",
    border: "border-cyan-400/20",
    bg: "bg-cyan-400/5",
    status: "planned",
    items: [
      "Custom domain + HTTPS (Certbot)",
      "nginx reverse proxy",
      "GitHub Actions CI/CD pipeline",
      "Sentry error monitoring",
      "Production Supabase project",
      "Staging environment",
    ],
  },
];

// ── Status badge ──────────────────────────────────────────────────────────────

function FeatureBadge({ status }: { status: FeatureStatus["status"] }) {
  if (status === "active")
    return (
      <span className="badge border bg-green-950/60 text-green-400 border-green-800/50">
        <CheckCircle className="h-3 w-3" /> Active
      </span>
    );
  if (status === "configured")
    return (
      <span className="badge border bg-blue-950/60 text-blue-400 border-blue-800/50">
        <CheckCircle className="h-3 w-3" /> Configured
      </span>
    );
  if (status === "not_configured")
    return (
      <span className="badge border bg-yellow-950/60 text-yellow-400 border-yellow-800/50">
        <AlertTriangle className="h-3 w-3" /> Not Set
      </span>
    );
  return (
    <span className="badge border bg-[#161b22] text-[#7d8590] border-[#21262d]">
      <Clock className="h-3 w-3" /> Planned
    </span>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function SaasPage() {
  const [status, setStatus] = useState<SaasStatus | null>(null);
  const [authStatus, setAuthStatus] = useState<AuthStatusResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  // Prevent hydration mismatch on supabaseConfigured
  const [mounted, setMounted] = useState(false);

  const loadStatus = async () => {
    setLoading(true);
    setError(null);
    try {
      const [saas, authStat] = await Promise.allSettled([
        api.saasStatus(),
        api.authStatus(),
      ]);
      if (saas.status === "fulfilled") setStatus(saas.value);
      if (authStat.status === "fulfilled") setAuthStatus(authStat.value);
      if (saas.status === "rejected") setError("Could not reach backend");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setMounted(true);
    loadStatus();
  }, []);

  return (
    <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 py-10">
      {/* Header */}
      <div className="flex items-start justify-between mb-8 flex-wrap gap-4">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <LayoutDashboard className="h-6 w-6 text-[#00ff88]" />
            <h1 className="text-2xl font-black text-white">SaaS Roadmap</h1>
          </div>
          <p className="text-sm text-[#7d8590] max-w-xl">
            KRONOS CORE is evolving from a local demo into a full multi-tenant SaaS platform.
            This page shows the current configuration state and the planned feature phases.
          </p>
        </div>
        <button
          onClick={loadStatus}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 rounded-lg border border-[#21262d] text-xs text-[#7d8590] hover:text-white hover:border-[#00ff88]/40 transition-all disabled:opacity-50"
        >
          <RefreshCw className={`h-3.5 w-3.5 ${loading ? "animate-spin" : ""}`} />
          Refresh
        </button>
      </div>

      {/* Live config status */}
      <div className="card border-[#21262d] mb-8">
        <div className="flex items-center gap-2 mb-4">
          <Server className="h-4 w-4 text-[#00ff88]" />
          <span className="text-xs font-bold text-[#7d8590] uppercase tracking-wider">
            Live Configuration Status
          </span>
        </div>

        {error && (
          <div className="flex items-center gap-2 text-yellow-400 text-xs p-3 bg-yellow-950/20 rounded-lg border border-yellow-800/30 mb-4">
            <AlertTriangle className="h-3.5 w-3.5 flex-shrink-0" />
            {error} — showing static roadmap only
          </div>
        )}

        {loading && !error && (
          <div className="space-y-2">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-6 bg-[#161b22] rounded animate-pulse" />
            ))}
          </div>
        )}

        {status && (
          <>
            <div className="mb-3 flex items-center gap-2">
              {status.saas_mode ? (
                <span className="badge border bg-green-950/60 text-green-400 border-green-800/50">
                  <CheckCircle className="h-3 w-3" /> SaaS Mode
                </span>
              ) : (
                <span className="badge border bg-[#161b22] text-[#7d8590] border-[#21262d]">
                  <Clock className="h-3 w-3" /> Demo Mode
                </span>
              )}
              <p className="text-xs text-[#7d8590]">{status.message}</p>
            </div>

            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-2">
              {status.features.map((f) => (
                <div
                  key={f.feature}
                  className="flex items-start justify-between gap-2 p-3 rounded-lg bg-[#161b22] border border-[#21262d]"
                >
                  <div>
                    <p className="text-xs font-medium text-white">{f.feature}</p>
                    <p className="text-[10px] text-[#7d8590] mt-0.5">{f.description}</p>
                  </div>
                  <div className="flex-shrink-0">
                    <FeatureBadge status={f.status} />
                  </div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>

      {/* Auth status card */}
      {(authStatus || mounted) && (
        <div className="card border-[#21262d] mb-8">
          <div className="flex items-center gap-2 mb-4">
            <Shield className="h-4 w-4 text-blue-400" />
            <span className="text-xs font-bold text-[#7d8590] uppercase tracking-wider">
              Auth Configuration
            </span>
          </div>
          <div className="grid sm:grid-cols-2 gap-4">
            {/* Backend */}
            <div className="bg-[#161b22] rounded-lg p-3">
              <p className="text-[10px] font-bold text-[#7d8590] uppercase tracking-wider mb-2">
                Backend (FastAPI)
              </p>
              {authStatus ? (
                <div className="space-y-1.5">
                  {[
                    { label: "SUPABASE_URL", ok: authStatus.supabase_url_configured },
                    { label: "SUPABASE_ANON_KEY", ok: authStatus.anon_key_configured },
                    { label: "SUPABASE_SERVICE_ROLE_KEY", ok: authStatus.service_role_configured },
                    { label: "JWT_SECRET", ok: authStatus.jwt_secret_configured },
                  ].map(({ label, ok }) => (
                    <div key={label} className="flex items-center justify-between">
                      <code className="text-[10px] text-[#7d8590]">{label}</code>
                      {ok ? (
                        <CheckCircle className="h-3 w-3 text-[#00ff88]" />
                      ) : (
                        <AlertTriangle className="h-3 w-3 text-yellow-400" />
                      )}
                    </div>
                  ))}
                  <p className="text-[10px] text-[#7d8590] mt-2 pt-2 border-t border-[#21262d]">
                    Mode: <span className={authStatus.mode === "configured" ? "text-[#00ff88]" : "text-yellow-400"}>{authStatus.mode}</span>
                  </p>
                </div>
              ) : (
                <p className="text-[10px] text-[#7d8590]">Backend unreachable</p>
              )}
            </div>
            {/* Frontend */}
            <div className="bg-[#161b22] rounded-lg p-3">
              <p className="text-[10px] font-bold text-[#7d8590] uppercase tracking-wider mb-2">
                Frontend (Next.js)
              </p>
              {mounted && (
                <div className="space-y-1.5">
                  {[
                    { label: "NEXT_PUBLIC_SUPABASE_URL", ok: supabaseConfigured },
                    { label: "NEXT_PUBLIC_SUPABASE_ANON_KEY", ok: supabaseConfigured },
                  ].map(({ label, ok }) => (
                    <div key={label} className="flex items-center justify-between">
                      <code className="text-[10px] text-[#7d8590]">{label}</code>
                      {ok ? (
                        <CheckCircle className="h-3 w-3 text-[#00ff88]" />
                      ) : (
                        <AlertTriangle className="h-3 w-3 text-yellow-400" />
                      )}
                    </div>
                  ))}
                  <p className="text-[10px] text-[#7d8590] mt-2 pt-2 border-t border-[#21262d]">
                    Mode: <span className={supabaseConfigured ? "text-[#00ff88]" : "text-yellow-400"}>{supabaseConfigured ? "configured" : "demo"}</span>
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Phase cards */}
      <div className="mb-6">
        <p className="text-xs font-bold text-[#7d8590] uppercase tracking-wider mb-4">
          Implementation Phases
        </p>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {PHASES.map((p) => (
            <div
              key={p.phase}
              className={`card border ${p.border} ${p.bg} hover:scale-[1.01] transition-all`}
            >
              <div className="flex items-start gap-3 mb-3">
                <div className={`p-2 rounded-lg border ${p.border}`}>
                  <p.icon className={`h-4 w-4 ${p.color}`} />
                </div>
                <div>
                  <p className={`text-[10px] font-bold tracking-widest ${p.color}`}>
                    {p.phase}
                  </p>
                  <p className="text-sm font-bold text-white">{p.title}</p>
                </div>
              </div>
              <ul className="space-y-1">
                {p.items.map((item, i) => (
                  <li key={i} className="flex items-start gap-1.5">
                    {p.status === "complete" ? (
                      <CheckCircle className={`h-3 w-3 ${p.color} flex-shrink-0 mt-0.5`} />
                    ) : (
                      <Clock className="h-3 w-3 text-[#7d8590] flex-shrink-0 mt-0.5" />
                    )}
                    <span className="text-[10px] text-[#7d8590] leading-relaxed">{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>

      {/* Activate instructions */}
      {status && !status.saas_mode && (
        <div className="card border-[#21262d] bg-[#0d1117]">
          <p className="text-xs font-bold text-[#7d8590] uppercase tracking-wider mb-3">
            Activate Phase 1 — Add These Variables to Your .env
          </p>
          <pre className="text-xs text-[#00ff88] bg-[#161b22] rounded-lg p-4 overflow-x-auto">
{`SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_ANON_KEY=your-anon-key
JWT_SECRET=your-jwt-secret

# Then install the client:
pip install supabase

# And run the migration:
psql $DATABASE_URL -f supabase/migrations/001_initial_schema.sql`}
          </pre>
          <p className="text-[10px] text-[#7d8590] mt-3">
            All existing endpoints continue to work in demo mode without these variables.
          </p>
        </div>
      )}
    </div>
  );
}
