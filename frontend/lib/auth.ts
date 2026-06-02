/**
 * Auth helper functions.
 *
 * Each function is safe to call when Supabase is not configured — it returns
 * a descriptive error instead of throwing, so pages continue to work in demo
 * mode without any conditional logic at the call site.
 */
import type { User } from "@supabase/supabase-js";
import { supabase, supabaseConfigured } from "./supabase/client";

export { supabaseConfigured };

const NOT_CONFIGURED_MSG =
  "Supabase is not configured. Add NEXT_PUBLIC_SUPABASE_URL and " +
  "NEXT_PUBLIC_SUPABASE_ANON_KEY to frontend/.env.local — " +
  "see docs/SUPABASE_AUTH_SETUP.md for instructions.";

export type AuthOk<T> = { ok: true; data: T };
export type AuthFail = { ok: false; error: string };
export type AuthResult<T> = AuthOk<T> | AuthFail;

/** Return the currently signed-in user, or null. */
export async function getCurrentUser(): Promise<User | null> {
  if (!supabase) return null;
  const { data } = await supabase.auth.getUser();
  return data.user ?? null;
}

/** Sign in with email and password. */
export async function signInWithEmail(
  email: string,
  password: string
): Promise<AuthResult<User>> {
  if (!supabase) return { ok: false, error: NOT_CONFIGURED_MSG };

  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });
  if (error) return { ok: false, error: error.message };
  if (!data.user) return { ok: false, error: "Sign-in succeeded but no user was returned." };
  return { ok: true, data: data.user };
}

/** Register a new account. */
export async function signUpWithEmail(
  email: string,
  password: string
): Promise<AuthResult<{ user: User | null; requiresConfirmation: boolean }>> {
  if (!supabase) return { ok: false, error: NOT_CONFIGURED_MSG };

  const { data, error } = await supabase.auth.signUp({ email, password });
  if (error) return { ok: false, error: error.message };

  // `data.session` is null when email confirmation is required.
  return {
    ok: true,
    data: {
      user: data.user ?? null,
      requiresConfirmation: data.session === null,
    },
  };
}

/** Sign out the current user. */
export async function signOut(): Promise<void> {
  if (!supabase) return;
  await supabase.auth.signOut();
}

/**
 * Subscribe to auth state changes.  Returns the unsubscribe function.
 * Safe no-op when Supabase is not configured.
 */
export function onAuthStateChange(
  callback: (user: User | null) => void
): () => void {
  if (!supabase) return () => {};
  const { data } = supabase.auth.onAuthStateChange((_event, session) => {
    callback(session?.user ?? null);
  });
  return () => data.subscription.unsubscribe();
}
