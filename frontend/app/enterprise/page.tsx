"use client";

import { useEffect, useState } from "react";
import {
  Building2, RefreshCw, CheckCircle, Shield, Server,
  DollarSign, Headphones, BookOpen, Link as LinkIcon,
} from "lucide-react";
import { api, EnterpriseResponse } from "@/lib/api";
import { formatDate, formatTimestamp } from "@/lib/format";

function Section({ icon: Icon, title, color, children }: {
  icon: typeof Shield; title: string; color: string; children: React.ReactNode;
}) {
  return (
    <div className="card border-[#21262d]">
      <div className="flex items-center gap-2 mb-4">
        <Icon className={`h-4 w-4 ${color}`} />
        <span className="text-xs font-bold text-[#7d8590] uppercase tracking-wider">{title}</span>
      </div>
      {children}
    </div>
  );
}

function List({ items, color = "text-[#00ff88]" }: { items: string[]; color?: string }) {
  return (
    <div className="space-y-2">
      {items.map((item, i) => (
        <div key={i} className="flex items-start gap-2.5">
          <CheckCircle className={`h-3.5 w-3.5 ${color} flex-shrink-0 mt-0.5`} />
          <span className="text-xs text-[#7d8590] leading-relaxed">{item}</span>
        </div>
      ))}
    </div>
  );
}

export default function EnterprisePage() {
  const [data, setData] = useState<EnterpriseResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      setData(await api.enterprise());
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Failed to load report");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  if (loading) return (
    <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 py-10">
      <div className="space-y-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="card border-[#21262d] h-32 bg-[#161b22] animate-pulse" />
        ))}
      </div>
    </div>
  );

  return (
    <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 py-10">
      {/* Header */}
      <div className="flex items-start justify-between mb-8 flex-wrap gap-4">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <Building2 className="h-6 w-6 text-[#00ff88]" />
            <h1 className="text-2xl font-black text-white">Enterprise Report</h1>
          </div>
          <p className="text-sm text-[#7d8590]">
            Boardroom-ready security and compliance report for institutional buyers and procurement teams.
          </p>
        </div>
        <button
          onClick={load}
          className="flex items-center gap-2 px-4 py-2 rounded-lg border border-[#21262d] text-xs text-[#7d8590] hover:text-white hover:border-[#00ff88]/40 transition-all"
        >
          <RefreshCw className="h-3.5 w-3.5" />
          Regenerate
        </button>
      </div>

      {error && (
        <div className="card border-red-800/50 bg-red-950/20 text-red-400 text-sm mb-6">{error}</div>
      )}

      {data && (
        <div className="space-y-4 fade-in">
          {/* Report header */}
          <div className="card border-[#00ff88]/20 bg-gradient-to-br from-[#00ff88]/5 to-transparent">
            <div className="flex items-start justify-between flex-wrap gap-4">
              <div>
                <div className="text-[10px] text-[#7d8590] tracking-widest uppercase mb-1">Confidential Enterprise Assessment</div>
                <h2 className="text-xl font-black text-white">{data.product}</h2>
                <div className="text-[10px] text-[#7d8590] mt-1">
                  Report ID: <span className="text-[#00ff88]">{data.report_id}</span>
                  {" · "}{formatDate(data.generated_at)}
                </div>
              </div>
              <div className="flex items-center gap-2 px-4 py-2 rounded-lg border border-[#00ff88]/30 bg-[#00ff88]/10">
                <Shield className="h-4 w-4 text-[#00ff88]" />
                <span className="text-xs font-bold text-[#00ff88]">ENTERPRISE READY</span>
              </div>
            </div>
            <p className="text-sm text-[#7d8590] mt-4 leading-relaxed border-t border-[#21262d] pt-4">
              {data.executive_summary}
            </p>
          </div>

          {/* Capabilities */}
          <Section icon={Shield} title="Capabilities" color="text-[#00ff88]">
            <List items={data.capabilities} />
          </Section>

          {/* Compliance */}
          <Section icon={CheckCircle} title="Compliance Alignment" color="text-blue-400">
            <div className="grid sm:grid-cols-2 gap-2">
              {data.compliance_alignment.map((item, i) => {
                const [framework, ...rest] = item.split("—");
                return (
                  <div key={i} className="p-3 rounded-lg bg-[#161b22] border border-[#21262d]">
                    <div className="text-xs font-bold text-blue-400 mb-1">{framework.trim()}</div>
                    {rest.length > 0 && <p className="text-[10px] text-[#7d8590]">{rest.join("—").trim()}</p>}
                  </div>
                );
              })}
            </div>
          </Section>

          {/* Integration + Deployment */}
          <div className="grid sm:grid-cols-2 gap-4">
            <Section icon={Server} title="Integration Options" color="text-purple-400">
              <List items={data.integration_options} color="text-purple-400" />
            </Section>
            <Section icon={Server} title="Deployment Models" color="text-yellow-400">
              <List items={data.deployment_models} color="text-yellow-400" />
            </Section>
          </div>

          {/* Pricing */}
          <Section icon={DollarSign} title="Pricing Model" color="text-[#00ff88]">
            <div className="grid sm:grid-cols-3 gap-3">
              {data.pricing_model.split(". ").filter(Boolean).map((tier, i) => {
                const [name, ...rest] = tier.split(":");
                const colors = ["border-[#21262d]", "border-blue-800/40 bg-blue-950/10", "border-[#00ff88]/20 bg-[#00ff88]/5"];
                return (
                  <div key={i} className={`p-4 rounded-lg border ${colors[i] ?? "border-[#21262d]"}`}>
                    <div className={`text-sm font-bold mb-2 ${i === 2 ? "text-[#00ff88]" : i === 1 ? "text-blue-400" : "text-white"}`}>
                      {name?.trim()}
                    </div>
                    <p className="text-xs text-[#7d8590] leading-relaxed">{rest.join(":").trim()}</p>
                  </div>
                );
              })}
            </div>
          </Section>

          {/* Support */}
          <Section icon={Headphones} title="Support Model" color="text-blue-400">
            <p className="text-xs text-[#7d8590] leading-relaxed">{data.support_model}</p>
          </Section>

          {/* References */}
          <Section icon={BookOpen} title="References & Standards" color="text-[#7d8590]">
            <div className="grid sm:grid-cols-2 gap-2">
              {data.references.map((ref, i) => {
                const [label, url] = ref.split("—");
                return (
                  <div key={i} className="flex items-center gap-2 p-2 rounded bg-[#161b22]">
                    <LinkIcon className="h-3 w-3 text-[#7d8590] flex-shrink-0" />
                    <span className="text-xs text-[#7d8590]">{label?.trim()}</span>
                    {url && <span className="text-[10px] text-[#30363d]">· {url.trim()}</span>}
                  </div>
                );
              })}
            </div>
          </Section>

          {/* Print note */}
          <div className="card border-[#21262d] bg-[#161b22] text-center py-6">
            <p className="text-xs text-[#7d8590]">
              This report was generated by <span className="text-[#00ff88]">KRONOS CORE v1.0</span> on {formatTimestamp(data.generated_at)}.
              For procurement or partnership enquiries, present this report alongside the live API demonstration.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
