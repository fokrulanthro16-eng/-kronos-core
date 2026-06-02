"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import type { User } from "@supabase/supabase-js";
import {
  User as UserIcon, Mail, Calendar, LogOut, Lock,
  Loader2, Shield, AlertTriangle,
} from "lucide-react";
import { getCurrentUser, signOut, onAuthStateChange, supabaseConfigured } from "@/lib/auth";
import { formatDate } from "@/lib/format";

export default function AccountPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [authState, setAuthState] = useState<"loading" | "demo" | "authenticated" | "unauthenticated">("loading");
  const [signingOut, setSigningOut] = useState(false);

  useEffect(() => {
    if (!supabaseConfigured) {
      setAuthState("demo");
      return;
    }
    getCurrentUser().then((u) => {
      setUser(u);
      setAuthState(u ? "authenticated" : "unauthenticated");
    });
    const unsubscribe = onAuthStateChange((u) => {
      setUser(u);
      setAuthState(u ? "authenticated" : "unauthenticated");
    });
    return unsubscribe;
  }, []);

  const handleSignOut = async () => {
    setSigningOut(true);
    await signOut();
    router.push("/");
  };

  // ── Loading ─────────────────────────────────────────────────────────────────
  if (authState === "loading") {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="h-8 w-8 text-[#00ff88] animate-spin" />
      </div>
    );
  }

  // ── Demo mode ───────────────────────────────────────────────────────────────
  if (authState === "demo") {
    return (
      <div className="mx-auto max-w-xl px-4 sm:px-6 py-10">
        <div className="flex items-center gap-3 mb-8">
          <Shield className="h-6 w-6 text-[#00ff88]" />
          <h1 className="text-2xl font-black text-white">Account</h1>
        </div>
        <div className="card border-yellow-800/40 bg-yellow-950/10">
          <div className="flex items-start gap-3">
            <AlertTriangle className="h-5 w-5 text-yellow-400 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-bold text-yellow-400 mb-2">Supabase not configured</p>
              <p className="text-xs text-[#7d8590] leading-relaxed mb-3">
                The account page requires Supabase Auth. Add the following variables to{" "}
                <code className="text-[#00ff88]">frontend/.env.local</code>:
              </p>
              <pre className="text-[10px] text-[#00ff88] bg-[#161b22] rounded-lg p-3 overflow-x-auto mb-3">
{`NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key`}
              </pre>
              <p className="text-[10px] text-[#7d8590]">
                See{" "}
                <code className="text-[#00ff88]">docs/SUPABASE_AUTH_SETUP.md</code> for
                step-by-step instructions.
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ── Unauthenticated ─────────────────────────────────────────────────────────
  if (authState === "unauthenticated") {
    return (
      <div className="flex items-center justify-center min-h-[60vh] px-4">
        <div className="w-full max-w-md text-center">
          <div className="card border-[#21262d] py-12">
            <Lock className="h-12 w-12 text-[#7d8590] mx-auto mb-4" />
            <h2 className="text-xl font-black text-white mb-2">Sign in required</h2>
            <p className="text-sm text-[#7d8590] mb-6">
              You need to be signed in to view your account.
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

  // ── Authenticated ───────────────────────────────────────────────────────────
  const createdAt = user?.created_at;

  return (
    <div className="mx-auto max-w-xl px-4 sm:px-6 py-10">
      <div className="flex items-center gap-3 mb-8">
        <Shield className="h-6 w-6 text-[#00ff88]" />
        <h1 className="text-2xl font-black text-white">Account</h1>
      </div>

      <div className="space-y-4">
        {/* Profile card */}
        <div className="card border-[#21262d]">
          <div className="flex items-center gap-3 mb-4">
            <div className="h-12 w-12 rounded-full bg-[#00ff88]/10 border border-[#00ff88]/20 flex items-center justify-center">
              <UserIcon className="h-5 w-5 text-[#00ff88]" />
            </div>
            <div>
              <p className="text-sm font-bold text-white">{user?.email}</p>
              <p className="text-[10px] text-[#7d8590]">KRONOS CORE User</p>
            </div>
          </div>

          <div className="space-y-3 border-t border-[#21262d] pt-4">
            <div className="flex items-center gap-3">
              <Mail className="h-3.5 w-3.5 text-[#7d8590] flex-shrink-0" />
              <div>
                <p className="text-[10px] text-[#7d8590] uppercase tracking-wider">Email</p>
                <p className="text-xs text-white">{user?.email}</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <UserIcon className="h-3.5 w-3.5 text-[#7d8590] flex-shrink-0" />
              <div>
                <p className="text-[10px] text-[#7d8590] uppercase tracking-wider">User ID</p>
                <p className="text-xs text-white font-mono truncate">{user?.id}</p>
              </div>
            </div>

            {createdAt && (
              <div className="flex items-center gap-3">
                <Calendar className="h-3.5 w-3.5 text-[#7d8590] flex-shrink-0" />
                <div>
                  <p className="text-[10px] text-[#7d8590] uppercase tracking-wider">
                    Account created
                  </p>
                  <p className="text-xs text-white">{formatDate(createdAt)}</p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Sign out */}
        <div className="card border-[#21262d]">
          <p className="text-xs font-bold text-[#7d8590] uppercase tracking-wider mb-3">
            Session
          </p>
          <button
            onClick={handleSignOut}
            disabled={signingOut}
            className="flex items-center gap-2 px-4 py-2.5 rounded-lg border border-red-900/40 bg-red-950/20 text-red-400 text-xs font-medium hover:border-red-700/60 hover:bg-red-950/40 transition-all disabled:opacity-50"
          >
            {signingOut ? (
              <Loader2 className="h-3.5 w-3.5 animate-spin" />
            ) : (
              <LogOut className="h-3.5 w-3.5" />
            )}
            {signingOut ? "Signing out..." : "Sign out"}
          </button>
        </div>
      </div>
    </div>
  );
}
