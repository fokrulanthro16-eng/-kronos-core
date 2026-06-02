"use client";

import { useState } from "react";
import { Shield, Zap, FolderTree, Package, CheckSquare, AlertTriangle } from "lucide-react";
import { api, BlueprintResponse } from "@/lib/api";
import { StatusBadge } from "@/components/StatusBadge";
import { CopyButton } from "@/components/CopyButton";

const EXAMPLES = [
  "Build a secure REST API for a fintech payment processing system with JWT auth and role-based access control",
  "Create a healthcare patient data management system with HIPAA compliance and encrypted storage",
  "Build an e-commerce platform with Stripe payments, inventory management, and admin dashboard",
];

export default function BlueprintPage() {
  const [objective, setObjective] = useState("");
  const [techStack, setTechStack] = useState("Node.js");
  const [sensitivity, setSensitivity] = useState("HIGH");
  const [result, setResult] = useState<BlueprintResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const generate = async () => {
    if (objective.trim().length < 10) {
      setError("Objective must be at least 10 characters.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const r = await api.blueprint({ objective: objective.trim(), tech_stack: techStack, sensitivity_level: sensitivity });
      setResult(r);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Request failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 py-10">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <Shield className="h-6 w-6 text-[#00ff88]" />
          <h1 className="text-2xl font-black text-white">Blueprint Generator</h1>
        </div>
        <p className="text-sm text-[#7d8590]">
          Enter a raw project objective. KRONOS CORE returns a hardened Claude execution blueprint with secure coding standards, directory architecture, package policies, and a ready-to-paste prompt.
        </p>
      </div>

      {/* Input card */}
      <div className="card border-[#21262d] mb-6">
        <div className="mb-4">
          <label className="text-xs font-bold text-[#7d8590] uppercase tracking-wider block mb-2">
            Project Objective
          </label>
          <textarea
            value={objective}
            onChange={(e) => setObjective(e.target.value)}
            placeholder="Describe your project in plain English..."
            rows={5}
            className="w-full bg-[#161b22] border border-[#21262d] rounded-lg px-4 py-3 text-sm text-white placeholder-[#7d8590] focus:outline-none focus:border-[#00ff88]/50 resize-none"
          />
          <div className="flex gap-2 mt-2 flex-wrap">
            {EXAMPLES.map((ex, i) => (
              <button
                key={i}
                onClick={() => setObjective(ex)}
                className="text-[10px] px-2 py-1 rounded border border-[#21262d] text-[#7d8590] hover:text-[#00ff88] hover:border-[#00ff88]/40 transition-all"
              >
                Example {i + 1}
              </button>
            ))}
          </div>
        </div>

        <div className="grid sm:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="text-xs font-bold text-[#7d8590] uppercase tracking-wider block mb-2">Tech Stack</label>
            <select
              value={techStack}
              onChange={(e) => setTechStack(e.target.value)}
              className="w-full bg-[#161b22] border border-[#21262d] rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-[#00ff88]/50"
            >
              {["Node.js", "Python / FastAPI", "Go", "Java / Spring", "TypeScript / Deno"].map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-xs font-bold text-[#7d8590] uppercase tracking-wider block mb-2">Sensitivity Level</label>
            <select
              value={sensitivity}
              onChange={(e) => setSensitivity(e.target.value)}
              className="w-full bg-[#161b22] border border-[#21262d] rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-[#00ff88]/50"
            >
              {["LOW", "MEDIUM", "HIGH", "CRITICAL"].map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>
        </div>

        {error && (
          <div className="flex items-center gap-2 text-red-400 text-xs mb-4">
            <AlertTriangle className="h-3.5 w-3.5" />
            {error}
          </div>
        )}

        <button
          onClick={generate}
          disabled={loading}
          className="w-full flex items-center justify-center gap-2 py-3 rounded-lg bg-[#00ff88] text-black font-bold text-sm hover:bg-[#00cc6a] transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <>
              <div className="h-4 w-4 border-2 border-black/30 border-t-black rounded-full animate-spin" />
              Generating Blueprint...
            </>
          ) : (
            <>
              <Zap className="h-4 w-4" />
              Generate Secure Claude Blueprint
            </>
          )}
        </button>
      </div>

      {/* Result */}
      {result && (
        <div className="space-y-4 fade-in">
          {/* Header */}
          <div className="card border-[#00ff88]/20 bg-[#00ff88]/5">
            <div className="flex items-center justify-between flex-wrap gap-3">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-[10px] font-bold text-[#00ff88] tracking-widest">{result.blueprint_id}</span>
                </div>
                <p className="text-sm text-white font-medium">{result.objective_summary}</p>
              </div>
              <div className="text-center">
                <div className="text-3xl font-black text-[#00ff88]">{result.risk_score.overall}<span className="text-sm text-[#7d8590]">/100</span></div>
                <StatusBadge level={result.risk_score.level} />
              </div>
            </div>
          </div>

          {/* Directory architecture */}
          <div className="card border-[#21262d]">
            <div className="flex items-center gap-2 mb-3">
              <FolderTree className="h-4 w-4 text-blue-400" />
              <span className="text-xs font-bold text-[#7d8590] uppercase tracking-wider">Directory Architecture</span>
            </div>
            <div className="space-y-1.5">
              {result.directory_architecture.map((d) => (
                <div key={d.path} className="flex items-start gap-3 py-1">
                  <code className="text-xs text-[#00ff88] w-36 flex-shrink-0">{d.path}</code>
                  <span className="text-xs text-[#7d8590]">{d.purpose}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Package policy */}
          <div className="card border-[#21262d]">
            <div className="flex items-center gap-2 mb-3">
              <Package className="h-4 w-4 text-yellow-400" />
              <span className="text-xs font-bold text-[#7d8590] uppercase tracking-wider">Package Policy</span>
            </div>
            <div className="grid sm:grid-cols-2 gap-4">
              <div>
                <p className="text-[10px] text-[#00ff88] font-bold tracking-wider mb-2">ALLOWED</p>
                <div className="flex flex-wrap gap-1.5">
                  {result.package_policy.allowed.map((p) => (
                    <span key={p} className="text-[10px] px-2 py-0.5 rounded bg-green-950/50 text-green-400 border border-green-800/40">{p}</span>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-[10px] text-red-400 font-bold tracking-wider mb-2">FORBIDDEN</p>
                <div className="flex flex-wrap gap-1.5">
                  {result.package_policy.forbidden.map((p) => (
                    <span key={p} className="text-[10px] px-2 py-0.5 rounded bg-red-950/50 text-red-400 border border-red-800/40">{p}</span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Production checklist */}
          <div className="card border-[#21262d]">
            <div className="flex items-center gap-2 mb-3">
              <CheckSquare className="h-4 w-4 text-[#00ff88]" />
              <span className="text-xs font-bold text-[#7d8590] uppercase tracking-wider">Production Readiness Checklist</span>
            </div>
            <div className="grid sm:grid-cols-2 gap-x-6 gap-y-1.5">
              {result.production_readiness_checklist.map((item, i) => (
                <div key={i} className="flex items-start gap-2">
                  <span className="text-[#00ff88] text-xs mt-0.5">✓</span>
                  <span className="text-xs text-[#7d8590]">{item}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Claude execution prompt */}
          <div className="card border-[#21262d]">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <Zap className="h-4 w-4 text-[#00ff88]" />
                <span className="text-xs font-bold text-[#7d8590] uppercase tracking-wider">Claude Execution Prompt</span>
              </div>
              <CopyButton text={result.claude_execution_prompt} />
            </div>
            <pre className="text-xs text-[#7d8590] bg-[#161b22] rounded-lg p-4 overflow-auto max-h-96 whitespace-pre-wrap leading-relaxed">
              {result.claude_execution_prompt}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
