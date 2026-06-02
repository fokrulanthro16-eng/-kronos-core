"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Shield, Lock, Mail, AlertTriangle, Loader2, UserPlus, CheckCircle } from "lucide-react";
import { signUpWithEmail, supabaseConfigured } from "@/lib/auth";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [requiresConfirmation, setRequiresConfirmation] = useState(false);
  const [loading, setLoading] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!email.trim() || !password || !confirmPassword) {
      setError("All fields are required.");
      return;
    }
    if (password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }
    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);
    const result = await signUpWithEmail(email.trim(), password);
    setLoading(false);

    if (!result.ok) {
      setError(result.error);
      return;
    }
    setSuccess(true);
    setRequiresConfirmation(result.data.requiresConfirmation);
  };

  if (success) {
    return (
      <div className="min-h-screen grid-bg flex items-center justify-center px-4">
        <div className="w-full max-w-md">
          <div className="flex items-center justify-center gap-2 mb-8">
            <Shield className="h-8 w-8 text-[#00ff88]" />
            <span className="font-black text-[#00ff88] tracking-widest">KRONOS</span>
            <span className="font-black text-white tracking-widest">CORE</span>
          </div>
          <div className="card border-[#00ff88]/30 bg-[#00ff88]/5 text-center py-10">
            <CheckCircle className="h-12 w-12 text-[#00ff88] mx-auto mb-4" />
            <h2 className="text-lg font-black text-white mb-2">Account created</h2>
            <p className="text-sm text-[#7d8590] mb-6">
              {requiresConfirmation
                ? "Check your email inbox for a confirmation link. Once confirmed, you can sign in."
                : "Your account is ready. Sign in to access your dashboard."}
            </p>
            <Link
              href="/login"
              className="inline-flex items-center gap-2 px-6 py-2.5 rounded-lg bg-[#00ff88] text-black font-bold text-sm hover:bg-[#00cc6a] transition-all"
            >
              Go to Sign in
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen grid-bg flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="flex items-center justify-center gap-2 mb-8">
          <Shield className="h-8 w-8 text-[#00ff88]" />
          <span className="font-black text-[#00ff88] tracking-widest">KRONOS</span>
          <span className="font-black text-white tracking-widest">CORE</span>
        </div>

        <div className="card border-[#21262d]">
          <h1 className="text-xl font-black text-white mb-1">Create account</h1>
          <p className="text-xs text-[#7d8590] mb-6">
            Start securing your AI development pipeline.
          </p>

          {/* Not configured notice */}
          {mounted && !supabaseConfigured && (
            <div className="mb-5 p-3 rounded-lg border border-yellow-800/40 bg-yellow-950/20 flex items-start gap-2">
              <AlertTriangle className="h-4 w-4 text-yellow-400 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-xs font-bold text-yellow-400 mb-1">
                  Supabase credentials are not configured
                </p>
                <p className="text-[10px] text-[#7d8590] leading-relaxed">
                  Add{" "}
                  <code className="text-[#00ff88]">NEXT_PUBLIC_SUPABASE_URL</code> and{" "}
                  <code className="text-[#00ff88]">NEXT_PUBLIC_SUPABASE_ANON_KEY</code> to{" "}
                  <code className="text-[#00ff88]">frontend/.env.local</code>.{" "}
                  See{" "}
                  <code className="text-[#00ff88]">docs/SUPABASE_AUTH_SETUP.md</code>.
                </p>
              </div>
            </div>
          )}

          <form onSubmit={handleRegister} className="space-y-4">
            <div>
              <label className="text-xs font-bold text-[#7d8590] uppercase tracking-wider block mb-1.5">
                Email
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-[#7d8590]" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@company.com"
                  autoComplete="email"
                  className="w-full bg-[#161b22] border border-[#21262d] rounded-lg pl-9 pr-4 py-2.5 text-sm text-white placeholder-[#7d8590] focus:outline-none focus:border-[#00ff88]/50 transition-colors"
                />
              </div>
            </div>

            <div>
              <label className="text-xs font-bold text-[#7d8590] uppercase tracking-wider block mb-1.5">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-[#7d8590]" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Minimum 6 characters"
                  autoComplete="new-password"
                  className="w-full bg-[#161b22] border border-[#21262d] rounded-lg pl-9 pr-4 py-2.5 text-sm text-white placeholder-[#7d8590] focus:outline-none focus:border-[#00ff88]/50 transition-colors"
                />
              </div>
            </div>

            <div>
              <label className="text-xs font-bold text-[#7d8590] uppercase tracking-wider block mb-1.5">
                Confirm Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-[#7d8590]" />
                <input
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="Repeat your password"
                  autoComplete="new-password"
                  className="w-full bg-[#161b22] border border-[#21262d] rounded-lg pl-9 pr-4 py-2.5 text-sm text-white placeholder-[#7d8590] focus:outline-none focus:border-[#00ff88]/50 transition-colors"
                />
              </div>
            </div>

            {error && (
              <div className="flex items-start gap-2 p-3 rounded-lg border border-red-800/40 bg-red-950/20">
                <AlertTriangle className="h-3.5 w-3.5 text-red-400 flex-shrink-0 mt-0.5" />
                <p className="text-xs text-red-400">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={loading || (mounted && !supabaseConfigured)}
              className="w-full flex items-center justify-center gap-2 py-3 rounded-lg bg-[#00ff88] text-black font-bold text-sm hover:bg-[#00cc6a] transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <UserPlus className="h-4 w-4" />
              )}
              {loading ? "Creating account..." : "Create account"}
            </button>
          </form>

          <div className="mt-5 pt-5 border-t border-[#21262d] text-center">
            <p className="text-xs text-[#7d8590]">
              Already have an account?{" "}
              <Link href="/login" className="text-[#00ff88] hover:underline font-medium">
                Sign in
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
