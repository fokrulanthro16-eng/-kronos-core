import Link from "next/link";
import {
  Shield, Lock, Package, Cpu, BarChart3, ArrowRight,
  Building2, GraduationCap, Landmark, Globe, Code2, ChevronRight,
} from "lucide-react";

const features = [
  {
    icon: Shield,
    title: "Secure Blueprint Engine",
    desc: "Converts raw project objectives into hardened Claude execution prompts — before a single line of code is written.",
    color: "text-[#00ff88]",
    border: "border-[#00ff88]/20",
    bg: "bg-[#00ff88]/5",
  },
  {
    icon: Package,
    title: "Static NPM Audit",
    desc: "Allowlist-first package scanning with fuzzy typosquat detection. Catches expresss, lodahs, event-stream before install.",
    color: "text-blue-400",
    border: "border-blue-400/20",
    bg: "bg-blue-400/5",
  },
  {
    icon: Cpu,
    title: "Runtime Sandbox",
    desc: "Live process and network inspection via psutil. Blocks exfiltration indicators before they reach production.",
    color: "text-purple-400",
    border: "border-purple-400/20",
    bg: "bg-purple-400/5",
  },
  {
    icon: BarChart3,
    title: "Enterprise Security Score",
    desc: "6-dimension composite score (0–100) with risk level, executive summary, and actionable fix recommendations.",
    color: "text-yellow-400",
    border: "border-yellow-400/20",
    bg: "bg-yellow-400/5",
  },
];

const risks = [
  { num: "01", label: "Unsafe AI Prompts", desc: "AI generates insecure code when given vague, unguarded objectives" },
  { num: "02", label: "Typosquatted Packages", desc: "expresss, lodahs, crossenv silently harvest credentials at install time" },
  { num: "03", label: "Phantom Packages", desc: "LLMs hallucinate package names that don't exist — or that are malicious" },
  { num: "04", label: "Runtime Exfiltration", desc: "Hidden outbound connections harvest data after deployment, unseen" },
];

const customers = [
  { icon: Code2, label: "AI Startups", desc: "Security governance without a dedicated security team" },
  { icon: Building2, label: "Software Companies", desc: "Pre-harden every AI-assisted feature before development begins" },
  { icon: Landmark, label: "Banks & FinTech", desc: "PCI-DSS aligned blueprints and compliance evidence reports" },
  { icon: Globe, label: "Gov Digital Teams", desc: "Documented AI security assessment for procurement requirements" },
  { icon: GraduationCap, label: "Universities", desc: "Enforce secure coding standards on all AI-assisted submissions" },
  { icon: Lock, label: "Security Firms", desc: "White-label AI governance layer for client advisory packages" },
];

export default function HomePage() {
  return (
    <div className="grid-bg">
      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-[#00ff88]/5 via-transparent to-transparent pointer-events-none" />
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-24 pb-20 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[#00ff88]/30 bg-[#00ff88]/5 text-[#00ff88] text-xs font-medium mb-8 tracking-widest">
            <span className="h-1.5 w-1.5 rounded-full bg-[#00ff88] pulse-green" />
            ENTERPRISE AI SECURITY GATEWAY · v1.0
          </div>

          <h1 className="text-5xl sm:text-7xl font-black tracking-tight mb-6">
            <span className="text-[#00ff88] glow-text">KRONOS</span>
            <span className="text-white"> CORE</span>
          </h1>

          <p className="text-xl sm:text-2xl text-[#7d8590] max-w-3xl mx-auto mb-4 leading-relaxed font-light">
            Autonomous Security & Prompt Architecture Gateway
          </p>
          <p className="text-base text-[#7d8590]/70 max-w-2xl mx-auto mb-12">
            Converts raw project objectives into secure Claude execution blueprints — before a single line of code is written.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-[#00ff88] text-black font-bold text-sm hover:bg-[#00cc6a] transition-all glow-green"
            >
              Launch Dashboard <ArrowRight className="h-4 w-4" />
            </Link>
            <Link
              href="/blueprint"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-lg border border-[#21262d] text-[#7d8590] font-medium text-sm hover:border-[#00ff88]/40 hover:text-white transition-all"
            >
              Generate Blueprint <ChevronRight className="h-4 w-4" />
            </Link>
          </div>

          {/* Stats bar */}
          <div className="mt-16 grid grid-cols-2 sm:grid-cols-4 gap-px bg-[#21262d] rounded-xl overflow-hidden border border-[#21262d]">
            {[
              { n: "4", l: "Security Layers" },
              { n: "8", l: "API Endpoints" },
              { n: "6", l: "Score Dimensions" },
              { n: "50", l: "Tests Passing" },
            ].map((s) => (
              <div key={s.l} className="bg-[#0d1117] px-6 py-5 text-center">
                <div className="text-3xl font-black text-[#00ff88]">{s.n}</div>
                <div className="text-[10px] text-[#7d8590] mt-1 tracking-wider uppercase">{s.l}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Problem */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-14">
          <p className="text-xs text-[#7d8590] tracking-widest uppercase mb-3">The Problem</p>
          <h2 className="text-3xl sm:text-4xl font-black text-white">
            4 Invisible Risks in Every AI Coding Team
          </h2>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {risks.map((r) => (
            <div
              key={r.num}
              className="card border-[#21262d] hover:border-red-800/50 transition-all group"
            >
              <div className="text-4xl font-black text-red-900/50 group-hover:text-red-600/70 transition-all mb-3">
                {r.num}
              </div>
              <div className="text-sm font-bold text-red-400 mb-2">{r.label}</div>
              <p className="text-xs text-[#7d8590] leading-relaxed">{r.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Solution / Features */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-14">
          <p className="text-xs text-[#7d8590] tracking-widest uppercase mb-3">The Solution</p>
          <h2 className="text-3xl sm:text-4xl font-black text-white">
            KRONOS CORE — 4 Layers of Protection
          </h2>
          <p className="text-[#7d8590] mt-4 max-w-xl mx-auto text-sm">
            Each layer enforces security before the next phase begins. No layer can be bypassed.
          </p>
        </div>
        <div className="grid sm:grid-cols-2 gap-6">
          {features.map((f) => (
            <div
              key={f.title}
              className={`card border ${f.border} ${f.bg} hover:scale-[1.01] transition-all`}
            >
              <div className="flex items-start gap-4">
                <div className={`p-2 rounded-lg border ${f.border} ${f.bg}`}>
                  <f.icon className={`h-5 w-5 ${f.color}`} />
                </div>
                <div>
                  <h3 className={`font-bold text-sm ${f.color} mb-1`}>{f.title}</h3>
                  <p className="text-xs text-[#7d8590] leading-relaxed">{f.desc}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Architecture flow */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16">
        <div className="card border-[#21262d] overflow-x-auto">
          <p className="text-xs text-[#7d8590] tracking-widest uppercase mb-6">Security Architecture</p>
          <div className="flex items-center gap-2 min-w-max">
            {[
              { label: "Developer Intent", sub: "Raw objective" },
              { label: "Blueprint Engine", sub: "Hardened prompt", accent: true },
              { label: "NPM Auditor", sub: "Package safety", accent: true },
              { label: "Sandbox Inspector", sub: "Runtime check", accent: true },
              { label: "Security Score", sub: "0–100 verdict", accent: true },
              { label: "Deploy Gate", sub: "Go / No-Go" },
            ].map((s, i) => (
              <div key={i} className="flex items-center gap-2">
                <div
                  className={`px-4 py-3 rounded-lg border text-center min-w-[120px] ${
                    s.accent
                      ? "border-[#00ff88]/30 bg-[#00ff88]/5"
                      : "border-[#21262d] bg-[#0d1117]"
                  }`}
                >
                  <div className={`text-xs font-bold ${s.accent ? "text-[#00ff88]" : "text-white"}`}>
                    {s.label}
                  </div>
                  <div className="text-[10px] text-[#7d8590] mt-0.5">{s.sub}</div>
                </div>
                {i < 5 && <ArrowRight className="h-4 w-4 text-[#21262d] flex-shrink-0" />}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Target customers */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-14">
          <p className="text-xs text-[#7d8590] tracking-widest uppercase mb-3">Target Market</p>
          <h2 className="text-3xl font-black text-white">Built For Enterprise Teams</h2>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {customers.map((c) => (
            <div key={c.label} className="card border-[#21262d] hover:border-[#00ff88]/20 transition-all group flex items-start gap-4">
              <div className="p-2 rounded-lg border border-[#21262d] group-hover:border-[#00ff88]/30 bg-[#161b22] transition-all">
                <c.icon className="h-4 w-4 text-[#7d8590] group-hover:text-[#00ff88] transition-all" />
              </div>
              <div>
                <div className="text-sm font-bold text-white mb-1">{c.label}</div>
                <p className="text-xs text-[#7d8590]">{c.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-20">
        <div className="card border-[#00ff88]/20 bg-gradient-to-br from-[#00ff88]/5 to-transparent text-center py-16">
          <h2 className="text-3xl sm:text-4xl font-black text-white mb-4">
            Ready to Secure Your AI Pipeline?
          </h2>
          <p className="text-[#7d8590] mb-8 max-w-lg mx-auto text-sm">
            Every AI-first engineering team needs this layer. Deploy in under 5 minutes.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-2 px-8 py-3 rounded-lg bg-[#00ff88] text-black font-bold text-sm hover:bg-[#00cc6a] transition-all"
            >
              Open Dashboard <ArrowRight className="h-4 w-4" />
            </Link>
            <Link
              href="/enterprise"
              className="inline-flex items-center gap-2 px-8 py-3 rounded-lg border border-[#21262d] text-[#7d8590] font-medium text-sm hover:border-[#00ff88]/40 hover:text-white transition-all"
            >
              View Enterprise Report
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-[#21262d] py-8 text-center text-[#7d8590] text-xs">
        <p>KRONOS CORE v1.0 — Autonomous Security & Prompt Architecture Gateway</p>
        <p className="mt-1 text-[#30363d]">Built for companies, institutions, and startup competitions.</p>
      </footer>
    </div>
  );
}
