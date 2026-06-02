"use client";

import { useState } from "react";
import { Package, Search, AlertTriangle, Info, CheckCircle } from "lucide-react";
import { api, AuditResponse } from "@/lib/api";
import { formatTimestamp } from "@/lib/format";
import { StatusBadge } from "@/components/StatusBadge";

const DEFAULT_PACKAGES = "express, expresss, event-stream, helmet, lodahs, jsonwebtoken, colors.js, uuid";

const RISK_INFO: Record<string, string> = {
  SAFE: "Package is on the KRONOS trusted allowlist.",
  UNKNOWN: "Not on the trusted list — not forbidden but unverified. Review before use.",
  SUSPICIOUS: "Naming pattern matches suspicious packages. Manual review required.",
  DEPRECATED: "Package is deprecated. Do not use in new projects.",
  DANGEROUS: "Explicitly forbidden — supply chain attack or sabotage history.",
  TYPOSQUAT: "Highly similar to a trusted package name. Likely credential-harvesting typosquat.",
  PHANTOM: "Hallucinated or non-existent package name.",
};

export default function AuditPage() {
  const [input, setInput] = useState(DEFAULT_PACKAGES);
  const [result, setResult] = useState<AuditResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const runAudit = async () => {
    const pkgs = input.split(/[,\n\s]+/).map((s) => s.trim()).filter(Boolean);
    if (pkgs.length === 0) { setError("Enter at least one package name."); return; }
    if (pkgs.length > 50) { setError("Maximum 50 packages per audit."); return; }
    setLoading(true);
    setError(null);
    try {
      setResult(await api.audit(pkgs));
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Audit failed");
    } finally {
      setLoading(false);
    }
  };

  const verdictColor = result?.summary.overall_verdict.startsWith("FAIL")
    ? "border-red-800/50 bg-red-950/20 text-red-400"
    : result?.summary.overall_verdict.startsWith("WARN")
    ? "border-yellow-800/50 bg-yellow-950/20 text-yellow-400"
    : "border-green-800/50 bg-green-950/20 text-[#00ff88]";

  return (
    <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-10">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <Package className="h-6 w-6 text-blue-400" />
          <h1 className="text-2xl font-black text-white">NPM Package Audit</h1>
        </div>
        <p className="text-sm text-[#7d8590]">
          Allowlist-first static analysis. Detects typosquats, forbidden packages, deprecated dependencies, and suspicious naming patterns before installation.
        </p>
      </div>

      {/* Input */}
      <div className="card border-[#21262d] mb-6">
        <label className="text-xs font-bold text-[#7d8590] uppercase tracking-wider block mb-2">
          Package Names <span className="text-[#30363d] font-normal normal-case">(comma or line separated)</span>
        </label>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          rows={4}
          placeholder="express, helmet, zod..."
          className="w-full bg-[#161b22] border border-[#21262d] rounded-lg px-4 py-3 text-sm text-white placeholder-[#7d8590] focus:outline-none focus:border-[#00ff88]/50 resize-none font-mono"
        />
        <div className="flex items-center justify-between mt-3">
          <button
            onClick={() => setInput(DEFAULT_PACKAGES)}
            className="text-xs text-[#7d8590] hover:text-[#00ff88] transition-all"
          >
            Load example packages
          </button>
          {error && (
            <div className="flex items-center gap-1.5 text-red-400 text-xs">
              <AlertTriangle className="h-3.5 w-3.5" /> {error}
            </div>
          )}
        </div>
        <button
          onClick={runAudit}
          disabled={loading}
          className="mt-3 w-full flex items-center justify-center gap-2 py-3 rounded-lg bg-blue-600 text-white font-bold text-sm hover:bg-blue-500 transition-all disabled:opacity-50"
        >
          {loading ? (
            <><div className="h-4 w-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />Auditing...</>
          ) : (
            <><Search className="h-4 w-4" />Run KRONOS Audit</>
          )}
        </button>
      </div>

      {/* Results */}
      {result && (
        <div className="space-y-4 fade-in">
          {/* Summary */}
          <div className={`card border ${verdictColor}`}>
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <p className="text-xs font-bold tracking-wider uppercase mb-1">Audit Summary</p>
                <p className="text-sm font-medium">{result.summary.overall_verdict}</p>
                <p className="text-[10px] text-[#7d8590] mt-1">ID: {result.audit_id} · {formatTimestamp(result.audited_at)}</p>
              </div>
              <div className="flex gap-4 text-center">
                <div>
                  <div className="text-2xl font-black text-[#00ff88]">{result.summary.safe}</div>
                  <div className="text-[10px] text-[#7d8590]">SAFE</div>
                </div>
                <div>
                  <div className="text-2xl font-black text-yellow-400">{result.summary.flagged - result.summary.dangerous}</div>
                  <div className="text-[10px] text-[#7d8590]">FLAGGED</div>
                </div>
                <div>
                  <div className="text-2xl font-black text-red-400">{result.summary.dangerous}</div>
                  <div className="text-[10px] text-[#7d8590]">DANGEROUS</div>
                </div>
                <div>
                  <div className="text-2xl font-black text-white">{result.summary.total}</div>
                  <div className="text-[10px] text-[#7d8590]">TOTAL</div>
                </div>
              </div>
            </div>
          </div>

          {/* Per-package results */}
          <div className="card border-[#21262d]">
            <p className="text-xs font-bold text-[#7d8590] uppercase tracking-wider mb-3">Package Results</p>
            <div className="space-y-2">
              {result.results.map((r) => (
                <div
                  key={r.name}
                  className="p-3 rounded-lg bg-[#161b22] border border-[#21262d] hover:border-[#30363d] transition-all"
                >
                  <div className="flex items-start justify-between gap-3 flex-wrap">
                    <div className="flex items-center gap-3">
                      <code className="text-sm text-white font-bold">{r.name}</code>
                      {r.safe_alternative && (
                        <span className="text-[10px] text-[#7d8590]">
                          → use <code className="text-[#00ff88]">{r.safe_alternative}</code>
                        </span>
                      )}
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] text-[#7d8590]">{(r.confidence * 100).toFixed(0)}% confidence</span>
                      <StatusBadge level={r.risk} />
                    </div>
                  </div>
                  <p className="text-xs text-[#7d8590] mt-1.5">{r.reason}</p>
                  {RISK_INFO[r.risk] && (
                    <div className="flex items-start gap-1.5 mt-1.5">
                      <Info className="h-3 w-3 text-[#30363d] flex-shrink-0 mt-0.5" />
                      <p className="text-[10px] text-[#30363d]">{RISK_INFO[r.risk]}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Recommendations */}
          {result.recommendations.length > 0 && (
            <div className="card border-[#21262d]">
              <p className="text-xs font-bold text-[#7d8590] uppercase tracking-wider mb-3">Recommendations</p>
              <div className="space-y-1.5">
                {result.recommendations.map((rec, i) => (
                  <div key={i} className="flex items-start gap-2">
                    <CheckCircle className="h-3.5 w-3.5 text-[#00ff88] flex-shrink-0 mt-0.5" />
                    <span className="text-xs text-[#7d8590]">{rec}</span>
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
