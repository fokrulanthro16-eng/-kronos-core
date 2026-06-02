"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Shield, ExternalLink, Menu, X } from "lucide-react";
import { useState } from "react";
import { AuthStatus } from "./AuthStatus";

const links = [
  { href: "/", label: "Home" },
  { href: "/dashboard", label: "Dashboard" },
  { href: "/blueprint", label: "Blueprint" },
  { href: "/audit", label: "Audit" },
  { href: "/sandbox", label: "Sandbox" },
  { href: "/enterprise", label: "Enterprise" },
  { href: "/saas", label: "SaaS" },
  { href: "/account", label: "Account" },
];

export function Navbar() {
  const path = usePathname();
  const [open, setOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-50 border-b border-[#21262d] bg-[#050810]/90 backdrop-blur-md">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-14 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 group">
            <div className="relative">
              <Shield className="h-7 w-7 text-[#00ff88] group-hover:drop-shadow-[0_0_8px_rgba(0,255,136,0.8)] transition-all" />
            </div>
            <span className="font-bold text-[#00ff88] tracking-widest text-sm">KRONOS</span>
            <span className="font-bold text-white tracking-widest text-sm">CORE</span>
          </Link>

          {/* Desktop links */}
          <div className="hidden md:flex items-center gap-1">
            {links.map((l) => (
              <Link
                key={l.href}
                href={l.href}
                className={`px-3 py-1.5 rounded-md text-xs font-medium tracking-wide transition-all ${
                  path === l.href
                    ? "bg-[#00ff88]/10 text-[#00ff88] border border-[#00ff88]/30"
                    : "text-[#7d8590] hover:text-white hover:bg-[#161b22]"
                }`}
              >
                {l.label}
              </Link>
            ))}
            <a
              href="http://127.0.0.1:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="ml-2 flex items-center gap-1 px-3 py-1.5 rounded-md text-xs font-medium border border-[#21262d] text-[#7d8590] hover:text-[#00ff88] hover:border-[#00ff88]/40 transition-all"
            >
              API Docs <ExternalLink className="h-3 w-3" />
            </a>
            <div className="ml-3 pl-3 border-l border-[#21262d]">
              <AuthStatus />
            </div>
          </div>

          {/* Mobile toggle */}
          <button
            className="md:hidden text-[#7d8590] hover:text-white"
            onClick={() => setOpen(!open)}
          >
            {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>

        {/* Mobile menu */}
        {open && (
          <div className="md:hidden py-3 border-t border-[#21262d] space-y-1">
            {links.map((l) => (
              <Link
                key={l.href}
                href={l.href}
                onClick={() => setOpen(false)}
                className={`block px-3 py-2 rounded-md text-xs font-medium ${
                  path === l.href ? "text-[#00ff88] bg-[#00ff88]/10" : "text-[#7d8590] hover:text-white"
                }`}
              >
                {l.label}
              </Link>
            ))}
            <a
              href="http://127.0.0.1:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 px-3 py-2 text-xs text-[#7d8590] hover:text-[#00ff88]"
            >
              API Docs <ExternalLink className="h-3 w-3" />
            </a>
          </div>
        )}
      </div>
    </nav>
  );
}
