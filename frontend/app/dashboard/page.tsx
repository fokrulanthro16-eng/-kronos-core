"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  Shield, Activity, Package, Cpu, BarChart3, FileText,
  RefreshCw, ExternalLink, CheckCircle, AlertTriangle, XCircle,
  Lock, Loader2,
} from "lucide-react";
import { api, HealthResponse, SandboxResponse, ScoreResponse } from "@/lib/api";
import { StatusBadge } from "@/components/StatusBadge";
import { getCurrentUser, supabaseConfigured, onAuthStateChange } from "@/lib/auth";
import type { User } from "@supabase/supabase-js";

type AuthState = "loading" | "demo" | "authenticated" | "unauthenticated";

const SCORE_REQ = {
  packages_audited: 6,
  packages_flagged: 2,
  sandbox_passed: true,
  blueprint_generated: true,
  docker_hardened: true,
  input_validation: true,
  auth_implemented: false,
  tls_enabled: false,
};

const endpoints = [
  { method: "GET",  path: "/api/v1/health",           label: "Health Check" },
  { method: "POST", path: "/api/v1/blueprint",         label: "Blueprint Engine" },
  { method: "POST", path: "/api/v1/audit",             label: "NPM Auditor" },
  { method: "GET",  path: "/api/v1/sandbox",           label: "Sandbox Inspector" },
  { method: "POST", path: "/api/v1/security/score",    label: "Security Scorer" },
  { method: "GET",  path: "/api/v1/demo",              label: "Competition Demo" },
  { method: "GET",  path: "/api/v1/enterprise/report", label: "Enterprise Report" },
];

function MethodBadge({ method }: { method: string }) {
  const color = method === "GET" ? "text-blue-400 border-blue-800/40 bg-blue-950/40"
                                 : "text-purple-400 border-purple-800/40 bg-purple-950/40";
  return <span className={`badge border ${color}`}>{method}</span>;
}

export default function DashboardPage() {
  const [authState, setAuthState] = useState<AuthState>("loading");
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [sandbox, setSandbox] = useState<SandboxResponse | null>(null);
  const [score, setScore] = useState<ScoreResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [time, setTime] = useState("");

  // Resolve auth state once on mount
  useEffect(() => {
    if (!supabaseConfigured) {
      setAuthState("demo");
      return;
    }
    getCurrentUser().then((u) => {
      setCurrentUser(u);
      setAuthState(u ? "authenticated" : "unauthenticated");
    });
    const unsubscribe = onAuthStateChange((u) => {
      setCurrentUser(u);
      setAuthState(u ? "authenticated" : "unauthenticated");
    });
    return unsubscribe;
  }, []);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const [h, sb, sc] = await Promise.all([
        api.health(),
        api.sandbox(true),
        api.securityScore(SCORE_REQ),
      ]);
      setHealth(h);
      setSandbox(sb);
      setScore(sc);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setLoading(false);
      setTime(new Date().toLocaleTimeString());
    }
  };

  // Only load live data once we know the user is allowed to see the dashboard
  useEffect(() => {
    if (authState === "demo" || authState === "authenticated") {
      load();
    }
  }, [authState]); // eslint-disable-line react-hooks/exhaustive-deps

  const scoreColor = score
    ? score.risk_level === "LOW" ? "text-[#00ff88]"
    : score.risk_level === "MEDIUM" ? "text-yellow-400"
    : "text-red-400"
    : "text-[#7d8590]";

  // ── Auth guard screens ──────────────────────────────────────────────────────

  if (authState === "loading") {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <Loader2 className="h-8 w-8 text-[#00ff88] animate-spin mx-auto mb-3" />
          <p className="text-xs text-[#7d8590]">Checking auth...</p>
        </div>
      </div>
    );
  }

  if (authState === "unauthenticated") {
    return (
      <div className="flex items-center justify-center min-h-[60vh] px-4">
        <div className="w-full max-w-md text-center">
          <div className="card border-[#21262d] py-12">
            <Lock className="h-12 w-12 text-[#7d8590] mx-auto mb-4" />
            <h2 className="text-xl font-black text-white mb-2">Protected Page</h2>
            <p className="text-sm text-[#7d8590] mb-6">
              Sign in to access your security dashboard.
            </p>
            <div className="flex gap-3 justify-center">
              <Link
                href="/login"
                className="px-6 py-2.5 rounded-lg bg-[#00ff88] text-black font-bold text-sm hover:bg-[#00cc6a] transition-all"
              >
                Sign in
              </Link>
              <Link
                href="/register"
                className="px-6 py-2.5 rounded-lg border border-[#21262d] text-[#7d8590] font-medium text-sm hover:border-[#00ff88]/40 hover:text-white transition-all"
              >
                Register
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-10">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-black text-white tracking-wide">Security Dashboard</h1>
          <div className="flex items-center gap-2 mt-1">
            <p className="text-xs text-[#7d8590]">Last refreshed: {time || "syncing..."}</p>
            {authState === "demo" && (
              <span className="badge border border-yellow-800/40 bg-yellow-950/20 text-yellow-400 text-[9px]">
                <AlertTriangle className="h-2.5 w-2.5" />
                Demo mode — Supabase auth not configured
              </span>
            )}
            {authState === "authenticated" && currentUser && (
              <span className="badge border border-[#00ff88]/20 bg-[#00ff88]/5 text-[#00ff88] text-[9px]">
                <CheckCircle className="h-2.5 w-2.5" />
                {currentUser.email}
              </span>
            )}
          </div>
        </div>
        <button
          onClick={load}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 rounded-lg border border-[#21262d] text-xs text-[#7d8590] hover:text-white hover:border-[#00ff88]/40 transition-all disabled:opacity-50"
        >
          <RefreshCw className={`h-3.5 w-3.5 ${loading ? "animate-spin" : ""}`} />
          Refresh
        </button>
      </div>

      {error && (
        <div className="mb-6 card border-red-800/50 bg-red-950/20 flex items-center gap-3">
          <XCircle className="h-5 w-5 text-red-400 flex-shrink-0" />
          <div>
            <p className="text-sm font-bold text-red-400">Backend Unreachable</p>
            <p className="text-xs text-[#7d8590] mt-0.5">{error}</p>
            <p className="text-xs text-[#7d8590] mt-1">
              Start the backend: <code className="text-[#00ff88]">uvicorn app.main:app --port 8000</code>
            </p>
          </div>
        </div>
      )}

      {/* Top cards */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        {/* Health */}
        <div className="card border-[#21262d]">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Activity className="h-4 w-4 text-[#00ff88]" />
              <span className="text-xs font-bold text-[#7d8590] uppercase tracking-wider">Backend Health</span>
            </div>
            {health && <StatusBadge level="SAFE" label="HEALTHY" />}
          </div>
          {health ? (
            <div className="space-y-2">
              <div className="flex justify-between text-xs">
                <span className="text-[#7d8590]">Service</span>
                <span className="text-white font-medium">{health.service}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-[#7d8590]">Version</span>
                <span className="text-[#00ff88]">{health.version}</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-[#7d8590]">Environment</span>
                <span className="text-white capitalize">{health.environment}</span>
              </div>
            </div>
          ) : (
            <div className="h-12 bg-[#161b22] rounded animate-pulse" />
          )}
        </div>

        {/* Security Score */}
        <div className="card border-[#21262d]">
          <div className="flex items-center gap-2 mb-4">
            <BarChart3 className="h-4 w-4 text-yellow-400" />
            <span className="text-xs font-bold text-[#7d8590] uppercase tracking-wider">Security Score</span>
          </div>
          {score ? (
            <div>
              <div className={`text-5xl font-black mb-1 ${scoreColor}`}>
                {score.total_score}<span className="text-xl text-[#7d8590]">/100</span>
              </div>
              <StatusBadge level={score.risk_level} />
              <div className="mt-3 space-y-1.5">
                {score.categories.slice(0, 3).map((c) => (
                  <div key={c.name} className="flex items-center gap-2">
                    <div className="flex-1 bg-[#161b22] rounded-full h-1">
                      <div
                        className={`h-1 rounded-full ${c.status === "PASS" ? "bg-[#00ff88]" : c.status === "WARN" ? "bg-yellow-400" : "bg-red-400"}`}
                        style={{ width: `${(c.score / c.max_score) * 100}%` }}
                      />
                    </div>
                    <span className="text-[10px] text-[#7d8590] w-20 truncate">{c.name}</span>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="h-20 bg-[#161b22] rounded animate-pulse" />
          )}
        </div>

        {/* Sandbox */}
        <div className="card border-[#21262d]">
          <div className="flex items-center gap-2 mb-4">
            <Cpu className="h-4 w-4 text-purple-400" />
            <span className="text-xs font-bold text-[#7d8590] uppercase tracking-wider">Sandbox Verdict</span>
          </div>
          {sandbox ? (
            <div>
              <div className="mb-3">
                <StatusBadge level={sandbox.verdict} />
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-[#7d8590]">Processes</span>
                  <span className="text-white">{sandbox.process_summary.total_processes}</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-[#7d8590]">Open Connections</span>
                  <span className="text-white">{sandbox.network_summary.open_connections}</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-[#7d8590]">Exfiltration Risk</span>
                  {sandbox.network_summary.exfiltration_risk
                    ? <StatusBadge level="HIGH" label="YES" />
                    : <StatusBadge level="SAFE" label="NONE" />
                  }
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-[#7d8590]">Blocked Actions</span>
                  <span className="text-[#00ff88] font-bold">{sandbox.blocked_actions.length}</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="h-20 bg-[#161b22] rounded animate-pulse" />
          )}
        </div>
      </div>

      {/* Audit + Demo cards */}
      <div className="grid lg:grid-cols-2 gap-4 mb-6">
        {/* Quick audit demo */}
        <div className="card border-[#21262d]">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Package className="h-4 w-4 text-blue-400" />
              <span className="text-xs font-bold text-[#7d8590] uppercase tracking-wider">NPM Audit Demo</span>
            </div>
            <Link href="/audit" className="text-xs text-[#00ff88] hover:underline flex items-center gap-1">
              Full audit <ExternalLink className="h-3 w-3" />
            </Link>
          </div>
          <div className="space-y-2">
            {[
              { name: "express", risk: "SAFE" },
              { name: "expresss", risk: "TYPOSQUAT" },
              { name: "event-stream", risk: "DANGEROUS" },
              { name: "helmet", risk: "SAFE" },
            ].map((p) => (
              <div key={p.name} className="flex items-center justify-between py-1.5 border-b border-[#21262d] last:border-0">
                <code className="text-xs text-white">{p.name}</code>
                <StatusBadge level={p.risk} />
              </div>
            ))}
          </div>
        </div>

        {/* Passed checks from sandbox */}
        <div className="card border-[#21262d]">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Shield className="h-4 w-4 text-[#00ff88]" />
              <span className="text-xs font-bold text-[#7d8590] uppercase tracking-wider">Passed Security Checks</span>
            </div>
            <Link href="/sandbox" className="text-xs text-[#00ff88] hover:underline flex items-center gap-1">
              Full report <ExternalLink className="h-3 w-3" />
            </Link>
          </div>
          {sandbox ? (
            <div className="space-y-1.5 max-h-44 overflow-y-auto">
              {sandbox.passed_checks.map((c, i) => (
                <div key={i} className="flex items-start gap-2">
                  <CheckCircle className="h-3.5 w-3.5 text-[#00ff88] flex-shrink-0 mt-0.5" />
                  <span className="text-xs text-[#7d8590] leading-relaxed">{c}</span>
                </div>
              ))}
            </div>
          ) : (
            <div className="h-32 bg-[#161b22] rounded animate-pulse" />
          )}
        </div>
      </div>

      {/* Score categories */}
      {score && (
        <div className="card border-[#21262d] mb-6">
          <div className="flex items-center gap-2 mb-4">
            <BarChart3 className="h-4 w-4 text-yellow-400" />
            <span className="text-xs font-bold text-[#7d8590] uppercase tracking-wider">Security Score Breakdown</span>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {score.categories.map((c) => (
              <div key={c.name} className="bg-[#161b22] rounded-lg p-3">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-medium text-white">{c.name}</span>
                  <StatusBadge level={c.status} />
                </div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 bg-[#0d1117] rounded-full h-1.5">
                    <div
                      className={`h-1.5 rounded-full transition-all ${
                        c.status === "PASS" ? "bg-[#00ff88]" : c.status === "WARN" ? "bg-yellow-400" : "bg-red-400"
                      }`}
                      style={{ width: `${(c.score / c.max_score) * 100}%` }}
                    />
                  </div>
                  <span className="text-xs text-[#7d8590] w-10 text-right">{c.score}/{c.max_score}</span>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-4 p-3 bg-[#161b22] rounded-lg">
            <p className="text-xs text-[#7d8590]">{score.executive_summary}</p>
          </div>
        </div>
      )}

      {/* API endpoint status */}
      <div className="card border-[#21262d]">
        <div className="flex items-center gap-2 mb-4">
          <FileText className="h-4 w-4 text-[#7d8590]" />
          <span className="text-xs font-bold text-[#7d8590] uppercase tracking-wider">API Endpoints</span>
        </div>
        <div className="space-y-2">
          {endpoints.map((e) => (
            <div
              key={e.path}
              className="flex items-center justify-between py-2 border-b border-[#21262d] last:border-0"
            >
              <div className="flex items-center gap-3">
                <MethodBadge method={e.method} />
                <code className="text-xs text-[#7d8590]">{e.path}</code>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-xs text-[#7d8590] hidden sm:block">{e.label}</span>
                {health ? (
                  <CheckCircle className="h-3.5 w-3.5 text-[#00ff88]" />
                ) : (
                  <AlertTriangle className="h-3.5 w-3.5 text-yellow-400" />
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
