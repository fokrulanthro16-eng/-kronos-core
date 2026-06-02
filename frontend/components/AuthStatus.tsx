"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import type { User } from "@supabase/supabase-js";
import { LogIn, UserPlus, LogOut, User as UserIcon, Loader2 } from "lucide-react";
import { getCurrentUser, signOut, onAuthStateChange, supabaseConfigured } from "@/lib/auth";

export function AuthStatus() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!supabaseConfigured) {
      setLoading(false);
      return;
    }

    // Initial check
    getCurrentUser().then((u) => {
      setUser(u);
      setLoading(false);
    });

    // Subscribe to live auth state changes (login / logout / token refresh)
    const unsubscribe = onAuthStateChange((u) => {
      setUser(u);
      setLoading(false);
    });

    return unsubscribe;
  }, []);

  const handleSignOut = async () => {
    await signOut();
    setUser(null);
    router.push("/");
  };

  // While loading, show nothing to avoid layout shift
  if (loading) {
    return <Loader2 className="h-3.5 w-3.5 text-[#30363d] animate-spin" />;
  }

  // Supabase not configured — show login/register links so users know they exist
  if (!supabaseConfigured) {
    return (
      <div className="flex items-center gap-1">
        <Link
          href="/login"
          className="px-2.5 py-1.5 rounded-md text-xs font-medium text-[#7d8590] hover:text-white hover:bg-[#161b22] transition-all"
        >
          Login
        </Link>
        <Link
          href="/register"
          className="px-2.5 py-1.5 rounded-md text-xs font-medium border border-[#21262d] text-[#7d8590] hover:text-[#00ff88] hover:border-[#00ff88]/40 transition-all"
        >
          Register
        </Link>
      </div>
    );
  }

  if (user) {
    return (
      <div className="flex items-center gap-2">
        <Link
          href="/account"
          className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-xs font-medium text-[#7d8590] hover:text-white hover:bg-[#161b22] transition-all max-w-[140px]"
        >
          <UserIcon className="h-3 w-3 flex-shrink-0" />
          <span className="truncate">{user.email}</span>
        </Link>
        <button
          onClick={handleSignOut}
          className="flex items-center gap-1 px-2.5 py-1.5 rounded-md text-xs font-medium text-[#7d8590] hover:text-red-400 hover:bg-red-950/20 transition-all"
        >
          <LogOut className="h-3 w-3" />
          Sign out
        </button>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-1">
      <Link
        href="/login"
        className="flex items-center gap-1 px-2.5 py-1.5 rounded-md text-xs font-medium text-[#7d8590] hover:text-white hover:bg-[#161b22] transition-all"
      >
        <LogIn className="h-3 w-3" />
        Login
      </Link>
      <Link
        href="/register"
        className="flex items-center gap-1 px-2.5 py-1.5 rounded-md text-xs font-medium border border-[#21262d] text-[#7d8590] hover:text-[#00ff88] hover:border-[#00ff88]/40 transition-all"
      >
        <UserPlus className="h-3 w-3" />
        Register
      </Link>
    </div>
  );
}
