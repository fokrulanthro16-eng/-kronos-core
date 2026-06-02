"use client";

import { useEffect, useState } from "react";
import { Clock, FileText, Package, Box, Building2, AlertTriangle, Database, Download } from "lucide-react";

const API = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

type HistoryData = {
  demo_mode: boolean;
  message: string | null;
  blueprints: Record<string, unknown>[];
  audits: Record<string, unknown>[];
  sandbox: Record<string, unknown>[];
  enterprise: Record<string, unknown>[];
};

const TABS = [
  { key: "blueprints", label: "Blueprints", icon: FileText },
  { key: "audits",     label: "NPM Audits", icon: Package },
  { key: "sandbox",    label: "Sandbox",    icon: Box },
  { key: "enterprise", label: "Enterprise", icon: Building2 },
] as const;

type TabKey = (typeof TABS)[number]["key"];

function EmptyState({ label }: { label: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <Database className="h-10 w-10 text-[#30363d] mb-4" />
      <p className="text-[#7d8590] text-sm">No saved {label.toLowerCase()} yet.</p>
      <p className="text-[#484f58] text-xs mt-1">Run a report to see it saved here.</p>
    </div>
  );
}

function str(v: unknown): string | null {
  return v != null ? String(v) : null;
}

function RecordCard({ record }: { record: Record<string, unknown> }) {
  const id        = str(record.id);
  const objective = str(record.objective);
  const verdict   = str(record.overall_verdict ?? record.verdict);
  const riskScore = str(record.risk_score);
  const created   = str(record.created_at)
    ? new Date(str(record.created_at) as string).toLocaleString()
    : null;

  return (
    <div className="border border-[#21262d] rounded-lg p-4 bg-[#0d1117] hover:border-[#00ff88]/30 transition-colors">
      {id         && <p className="text-[#484f58] text-xs font-mono mb-1">{id}</p>}
      {objective  && <p className="text-white text-sm mb-2 line-clamp-2">{objective}</p>}
      {verdict    && (
        <span className="inline-block px-2 py-0.5 rounded text-xs font-medium bg-[#161b22] text-[#00ff88] border border-[#00ff88]/20 mb-2">
          {verdict}
        </span>
      )}
      {riskScore  && (
        <p className="text-[#7d8590] text-xs">Risk score: <span className="text-white">{riskScore}</span></p>
      )}
      {created    && (
        <p className="text-[#484f58] text-xs mt-2 flex items-center gap-1">
          <Clock className="h-3 w-3" /> {created}
        </p>
      )}
    </div>
  );
}

export default function HistoryPage() {
  const [data, setData] = useState<HistoryData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tab, setTab] = useState<TabKey>("blueprints");

  useEffect(() => {
    fetch(`${API}/api/v1/history`)
      .then((r) => r.json())
      .then((d) => { setData(d); setLoading(false); })
      .catch(() => { setError("Could not reach backend."); setLoading(false); });
  }, []);

  const records: Record<string, unknown>[] = data ? (data[tab] ?? []) : [];
  const tabLabel = TABS.find((t) => t.key === tab)?.label ?? tab;

  return (
    <div className="min-h-screen bg-[#050810] text-white">
      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 py-10">

        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <Clock className="h-6 w-6 text-[#00ff88]" />
            <h1 className="text-2xl font-bold tracking-tight">Report History</h1>
          </div>
          <p className="text-[#7d8590] text-sm">
            Saved outputs from blueprints, audits, sandbox inspections, and enterprise reports.
          </p>
        </div>

        {/* Demo mode banner */}
        {data?.demo_mode && (
          <div className="mb-6 flex items-start gap-3 rounded-lg border border-yellow-500/30 bg-yellow-500/5 px-4 py-3">
            <AlertTriangle className="h-4 w-4 text-yellow-400 mt-0.5 flex-shrink-0" />
            <div>
              <p className="text-yellow-400 text-sm font-medium">Demo Mode — Database not configured</p>
              <p className="text-yellow-400/70 text-xs mt-0.5">
                {data.message ?? "Run the Supabase migration to activate saved history."}
              </p>
            </div>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="mb-6 rounded-lg border border-red-500/30 bg-red-500/5 px-4 py-3 text-red-400 text-sm">
            {error} — Is the backend running at {API}?
          </div>
        )}

        {/* Tabs */}
        <div className="flex gap-1 mb-6 border-b border-[#21262d]">
          {TABS.map(({ key, label, icon: Icon }) => (
            <button
              key={key}
              onClick={() => setTab(key)}
              className={`flex items-center gap-1.5 px-4 py-2 text-xs font-medium rounded-t-md transition-all border-b-2 -mb-px ${
                tab === key
                  ? "border-[#00ff88] text-[#00ff88] bg-[#00ff88]/5"
                  : "border-transparent text-[#7d8590] hover:text-white hover:bg-[#161b22]"
              }`}
            >
              <Icon className="h-3.5 w-3.5" />
              {label}
              {data && (
                <span className="ml-1 px-1.5 py-0.5 rounded-full text-[10px] bg-[#21262d] text-[#7d8590]">
                  {data[key]?.length ?? 0}
                </span>
              )}
            </button>
          ))}
        </div>

        {/* Enterprise PDF CTA */}
        {tab === "enterprise" && (
          <div className="mb-4 flex items-center justify-between p-3 rounded-lg border border-[#00ff88]/20 bg-[#00ff88]/5">
            <p className="text-xs text-[#7d8590]">Download the current enterprise report as a branded PDF</p>
            <a
              href={`${API}/api/v1/export/enterprise/pdf`}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-md border border-[#00ff88]/40 text-xs text-[#00ff88] hover:bg-[#00ff88]/10 transition-all flex-shrink-0 ml-4"
            >
              <Download className="h-3 w-3" />
              Download PDF
            </a>
          </div>
        )}

        {/* Content */}
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="h-6 w-6 rounded-full border-2 border-[#00ff88] border-t-transparent animate-spin" />
          </div>
        ) : records.length === 0 ? (
          <EmptyState label={tabLabel} />
        ) : (
          <div className="grid gap-3 sm:grid-cols-2">
            {records.map((rec, i) => (
              <RecordCard key={(rec.id as string) ?? i} record={rec} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
