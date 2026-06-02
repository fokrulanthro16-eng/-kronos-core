import type { Metadata } from "next";
import "./globals.css";
import { Navbar } from "@/components/Navbar";

export const metadata: Metadata = {
  title: "KRONOS CORE — Autonomous Security Gateway",
  description:
    "Enterprise-grade AI prompt architecture and security gateway. Secure Claude execution blueprints, npm audit, runtime sandboxing.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen antialiased">
        <div className="scan-line" />
        <Navbar />
        <main className="min-h-screen">{children}</main>
      </body>
    </html>
  );
}
