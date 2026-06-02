"use client";

import { useState } from "react";
import {
  Cpu, Play, CheckCircle, XCircle, AlertTriangle,
  Activity, Wifi, HardDrive, Shield,
} from "lucide-react";
import { api, SandboxResponse } from "@/lib/api";
import { formatTimestamp } from "@/lib/format";
import { StatusBadge } from "@/components/StatusBadge";

export default function SandboxPage() {
  const [result, setResult] = useState<SandboxResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const run = async () => {
    setLoading(true);
    setError(null);
    try {
      setResult(await api.sandbox(true));
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Inspection failed");
    } finally {
      setLoading(false);
    }
  };

  const verdictBorder =
    result?.verdict === "CLEAN" ? "border-[#00ff88]/30 bg-[#00ff88]/5" :
    result?.verdict === "SUSPICIOUS" ? "border-yellow-600/30 bg-yellow-950/10" :
    "border-red-600/30 bg-red-950/10";

  return (
    <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-10">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <Cpu className="h-6 w-6 text-purple-400" />
          <h1 className="text-2xl font-black text-white">Sandbox Inspector</h1>
        </div>
        <p className="text-sm text-[#7d8590]">
          Live runtime behavioural analysis using psutil. Inspects processes, network connections, and filesystem access. Demo mode simulates and blocks malicious patterns.
        </p>
      </div>

      {/* Launch card */}
      <div className="card border-[#21262d] mb-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="h-2 w-2 rounded-full bg-purple-400 pulse-green" />
          <span className="text-xs font-bold text-[#7d8590] uppercase tracking-wider">KRONOS Sandbox — Demo Mode Active</span>
        </div>
        <p className="text-xs text-[#7d8590] mb-5 leading-relaxed">
          Demo mode simulates three blocked attack patterns: an outbound connection to a known C2 IP range (185.220.101.0:4444), an attempt to write to /etc/hosts, and a subprocess spawn attempt — all blocked by KRONOS runtime policy.
        </p>
        {error && (
          <div className="flex items-center gap-2 text-red-400 text-xs mb-4 p-3 bg-red-950/20 rounded-lg border border-red-800/40">
            <AlertTriangle className="h-3.5 w-3.5 flex-shrink-0" />
            {error}
          </div>
        )}
        <button
          onClick={run}
          disabled={loading}
          className="w-full flex items-center justify-center gap-2 py-3 rounded-lg bg-purple-600 text-white font-bold text-sm hover:bg-purple-500 transition-all disabled:opacity-50"
        >
          {loading ? (
            <><div className="h-4 w-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />Inspecting Runtime...</>
          ) : (
            <><Play className="h-4 w-4" />Run Sandbox Inspection</>
          )}
        </button>
      </div>

      {result && (
        <div className="space-y-4 fade-in">
          {/* Verdict banner */}
          <div className={`card border ${verdictBorder}`}>
            <div className="flex items-center justify-between flex-wrap gap-4">
              <div className="flex items-center gap-3">
                <Shield className={`h-8 w-8 ${result.verdict === "CLEAN" ? "text-[#00ff88]" : result.verdict === "SUSPICIOUS" ? "text-yellow-400" : "text-red-400"}`} />
                <div>
                  <div className="text-xs text-[#7d8590] mb-1">Sandbox Verdict</div>
                  <StatusBadge level={result.verdict} />
                </div>
              </div>
              <div className="text-right">
                <div className="text-[10px] text-[#7d8590]">{result.inspection_id}</div>
                <div className="text-[10px] text-[#7d8590]">{formatTimestamp(result.inspected_at)}</div>
              </div>
            </div>
            <p className="text-xs text-[#7d8590] mt-4 leading-relaxed">{result.executive_note}</p>
          </div>

          {/* Metrics grid */}
          <div className="grid sm:grid-cols-3 gap-4">
            {/* Processes */}
            <div className="card border-[#21262d]">
              <div className="flex items-center gap-2 mb-3">
                <Activity className="h-4 w-4 text-blue-400" />
                <span className="text-xs font-bold text-[#7d8590] uppercase tracking-wider">Processes</span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-[#7d8590]">Total</span>
                  <span className="text-white font-bold">{result.process_summary.total_processes}</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-[#7d8590]">High CPU</span>
                  <span className={result.process_summary.high_cpu_processes > 0 ? "text-yellow-400 font-bold" : "text-[#00ff88] font-bold"}>
                    {result.process_summary.high_cpu_processes}
                  </span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-[#7d8590]">Suspicious</span>
                  <span className={result.process_summary.suspicious_processes.length > 0 ? "text-red-400 font-bold" : "text-[#00ff88] font-bold"}>
                    {result.process_summary.suspicious_processes.length}
                  </span>
                </div>
              </div>
            </div>

            {/* Network */}
            <div className="card border-[#21262d]">
              <div className="flex items-center gap-2 mb-3">
                <Wifi className="h-4 w-4 text-purple-400" />
                <span className="text-xs font-bold text-[#7d8590] uppercase tracking-wider">Network</span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-[#7d8590]">Connections</span>
                  <span className="text-white font-bold">{result.network_summary.open_connections}</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-[#7d8590]">Blocked</span>
                  <span className="text-[#00ff88] font-bold">{result.network_summary.blocked_connections + (result.demo_mode ? 2 : 0)}</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-[#7d8590]">Exfil Risk</span>
                  {result.network_summary.exfiltration_risk
                    ? <StatusBadge level="HIGH" label="YES" />
                    : <StatusBadge level="SAFE" label="NONE" />
                  }
                </div>
              </div>
            </div>

            {/* Filesystem */}
            <div className="card border-[#21262d]">
              <div className="flex items-center gap-2 mb-3">
                <HardDrive className="h-4 w-4 text-yellow-400" />
                <span className="text-xs font-bold text-[#7d8590] uppercase tracking-wider">Filesystem</span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-[#7d8590]">Risky Writable Paths</span>
                  <span className={result.file_summary.writable_sensitive_paths > 0 ? "text-yellow-400 font-bold" : "text-[#00ff88] font-bold"}>
                    {result.file_summary.writable_sensitive_paths}
                  </span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-[#7d8590]">Risk Level</span>
                  <StatusBadge level={result.file_summary.risk_level} />
                </div>
              </div>
            </div>
          </div>

          {/* Passed checks */}
          <div className="card border-[#21262d]">
            <div className="flex items-center gap-2 mb-3">
              <CheckCircle className="h-4 w-4 text-[#00ff88]" />
              <span className="text-xs font-bold text-[#7d8590] uppercase tracking-wider">Passed Checks</span>
            </div>
            <div className="space-y-1.5">
              {result.passed_checks.map((c, i) => (
                <div key={i} className="flex items-start gap-2">
                  <CheckCircle className="h-3.5 w-3.5 text-[#00ff88] flex-shrink-0 mt-0.5" />
                  <span className="text-xs text-[#7d8590] leading-relaxed">{c}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Blocked actions */}
          {result.blocked_actions.length > 0 && (
            <div className="card border-red-800/30 bg-red-950/10">
              <div className="flex items-center gap-2 mb-3">
                <XCircle className="h-4 w-4 text-red-400" />
                <span className="text-xs font-bold text-red-400 uppercase tracking-wider">Blocked Actions</span>
                <span className="text-[10px] text-[#7d8590]">(KRONOS runtime policy enforced)</span>
              </div>
              <div className="space-y-1.5">
                {result.blocked_actions.map((a, i) => (
                  <div key={i} className="flex items-start gap-2 p-2 rounded bg-red-950/30 border border-red-900/30">
                    <XCircle className="h-3.5 w-3.5 text-red-400 flex-shrink-0 mt-0.5" />
                    <span className="text-xs text-red-300 leading-relaxed">{a}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
