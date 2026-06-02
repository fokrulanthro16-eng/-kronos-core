import { createClient, SupabaseClient } from "@supabase/supabase-js";

const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

/** True when both Supabase env vars are present. */
export const supabaseConfigured: boolean = Boolean(url && anonKey);

/**
 * Browser Supabase client.
 *
 * `null` when credentials are not configured — every caller must guard:
 *   if (!supabase) { ... handle demo mode ... }
 *
 * Never used server-side; always called from "use client" components.
 */
export const supabase: SupabaseClient | null = supabaseConfigured
  ? createClient(url!, anonKey!)
  : null;
