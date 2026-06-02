"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { CheckCircle, AlertTriangle, Zap, Shield, Building2, Sparkles } from "lucide-react";

const API = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

type Plan = {
  id: string;
  name: string;
  price_label: string;
  description: string;
  features: string[];
  cta: string;
  highlight: boolean;
};

type BillingStatus = {
  demo_mode: boolean;
  message: string | null;
};

const PLAN_ICONS: Record<string, typeof Shield> = {
  free:       Shield,
  starter:    Zap,
  pro:        Sparkles,
  enterprise: Building2,
};

const PLAN_COLORS: Record<string, { border: string; accent: string; bg: string }> = {
  free:       { border: "border-[#21262d]",       accent: "text-[#7d8590]",   bg: "" },
  starter:    { border: "border-blue-800/40",     accent: "text-blue-400",    bg: "bg-blue-950/10" },
  pro:        { border: "border-[#00ff88]/40",    accent: "text-[#00ff88]",   bg: "bg-[#00ff88]/5" },
  enterprise: { border: "border-purple-800/40",  accent: "text-purple-400",  bg: "bg-purple-950/10" },
};

function PlanCard({ plan, onUpgrade }: { plan: Plan; onUpgrade: (id: string) => void }) {
  const Icon  = PLAN_ICONS[plan.id] ?? Shield;
  const color = PLAN_COLORS[plan.id] ?? PLAN_COLORS.free;

  return (
    <div
      className={`relative flex flex-col rounded-xl border p-6 ${color.border} ${color.bg} ${
        plan.highlight ? "ring-1 ring-[#00ff88]/30" : ""
      } transition-all hover:border-opacity-80`}
    >
      {plan.highlight && (
        <div className="absolute -top-3 left-1/2 -translate-x-1/2">
          <span className="px-3 py-1 rounded-full text-[10px] font-bold bg-[#00ff88] text-black tracking-wider">
            MOST POPULAR
          </span>
        </div>
      )}

      <div className="flex items-center gap-2 mb-3">
        <Icon className={`h-5 w-5 ${color.accent}`} />
        <h3 className={`text-base font-bold ${color.accent}`}>{plan.name}</h3>
      </div>

      <div className="mb-3">
        <span className="text-2xl font-black text-white">{plan.price_label}</span>
      </div>

      <p className="text-xs text-[#7d8590] leading-relaxed mb-5">{plan.description}</p>

      <ul className="space-y-2 mb-6 flex-1">
        {plan.features.map((f, i) => (
          <li key={i} className="flex items-start gap-2">
            <CheckCircle className={`h-3.5 w-3.5 ${color.accent} flex-shrink-0 mt-0.5`} />
            <span className="text-xs text-[#7d8590]">{f}</span>
          </li>
        ))}
      </ul>

      {plan.id === "free" ? (
        <Link
          href="/"
          className="block text-center px-4 py-2.5 rounded-lg border border-[#21262d] text-xs font-medium text-[#7d8590] hover:text-white hover:border-[#00ff88]/30 transition-all"
        >
          {plan.cta}
        </Link>
      ) : plan.id === "enterprise" ? (
        <a
          href="mailto:sales@kronos-core.com"
          className={`block text-center px-4 py-2.5 rounded-lg border ${color.border} text-xs font-medium ${color.accent} hover:bg-purple-950/30 transition-all`}
        >
          {plan.cta}
        </a>
      ) : (
        <button
          onClick={() => onUpgrade(plan.id)}
          className={`w-full px-4 py-2.5 rounded-lg text-xs font-bold transition-all ${
            plan.highlight
              ? "bg-[#00ff88] text-black hover:bg-[#00cc6a]"
              : `border ${color.border} ${color.accent} hover:bg-blue-950/30`
          }`}
        >
          {plan.cta}
        </button>
      )}
    </div>
  );
}

export default function PricingPage() {
  const [plans, setPlans]         = useState<Plan[]>([]);
  const [status, setStatus]       = useState<BillingStatus | null>(null);
  const [loading, setLoading]     = useState(true);
  const [upgradeMsg, setUpgradeMsg] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      fetch(`${API}/api/v1/billing/plans`).then((r) => r.json()),
      fetch(`${API}/api/v1/billing/status`).then((r) => r.json()),
    ])
      .then(([plansData, statusData]) => {
        setPlans(plansData.plans ?? []);
        setStatus(statusData);
      })
      .catch(() => setStatus({ demo_mode: true, message: "Could not reach backend." }))
      .finally(() => setLoading(false));
  }, []);

  const handleUpgrade = async (planId: string) => {
    try {
      const resp = await fetch(`${API}/api/v1/billing/create-checkout-session`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ plan: planId }),
      });
      const data = await resp.json();
      if (data.checkout_url) {
        window.location.href = data.checkout_url;
      } else {
        setUpgradeMsg(data.message ?? "Billing not configured yet.");
      }
    } catch {
      setUpgradeMsg("Could not reach backend.");
    }
  };

  return (
    <div className="min-h-screen bg-[#050810] text-white">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 py-12">

        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-3xl font-black tracking-tight text-white mb-3">
            Simple, transparent <span className="text-[#00ff88]">pricing</span>
          </h1>
          <p className="text-sm text-[#7d8590] max-w-xl mx-auto">
            Start free, upgrade when you need saved history, PDF exports, or a full organisation workspace.
          </p>
        </div>

        {/* Demo mode banner */}
        {status?.demo_mode && (
          <div className="mb-8 flex items-start gap-3 rounded-lg border border-yellow-500/30 bg-yellow-500/5 px-4 py-3 max-w-2xl mx-auto">
            <AlertTriangle className="h-4 w-4 text-yellow-400 mt-0.5 flex-shrink-0" />
            <div>
              <p className="text-yellow-400 text-sm font-medium">Demo Mode — Stripe billing not configured</p>
              <p className="text-yellow-400/70 text-xs mt-0.5">
                {status.message ?? "Add STRIPE_SECRET_KEY to .env to activate live checkout."}
              </p>
            </div>
          </div>
        )}

        {/* Upgrade feedback */}
        {upgradeMsg && (
          <div className="mb-6 flex items-start gap-3 rounded-lg border border-yellow-500/30 bg-yellow-500/5 px-4 py-3 max-w-2xl mx-auto">
            <AlertTriangle className="h-4 w-4 text-yellow-400 mt-0.5 flex-shrink-0" />
            <p className="text-yellow-400 text-sm">{upgradeMsg}</p>
          </div>
        )}

        {/* Pricing grid */}
        {loading ? (
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="rounded-xl border border-[#21262d] h-96 bg-[#161b22] animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {plans.map((plan) => (
              <PlanCard key={plan.id} plan={plan} onUpgrade={handleUpgrade} />
            ))}
          </div>
        )}

        {/* Footer note */}
        <p className="text-center text-[#484f58] text-xs mt-10">
          All prices in USD. Subscriptions can be cancelled at any time.{" "}
          <Link href="/account" className="text-[#7d8590] hover:text-[#00ff88] transition-colors">
            View your account
          </Link>
        </p>
      </div>
    </div>
  );
}
