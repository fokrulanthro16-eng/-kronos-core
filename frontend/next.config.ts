import type { NextConfig } from "next";

// Backend URL is read at build/runtime from the environment.
// Default: local development backend.
// Override via BACKEND_URL in .env.local or the platform's env config.
const backendUrl = process.env.BACKEND_URL ?? "http://127.0.0.1:8000";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${backendUrl}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
