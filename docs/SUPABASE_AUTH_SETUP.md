# KRONOS CORE — Supabase Auth Setup Guide

This guide walks you through creating a Supabase project and wiring the credentials into KRONOS CORE so real login/register works.

---

## Prerequisites

- A free account at [supabase.com](https://supabase.com)
- KRONOS CORE backend and frontend running locally
- Node.js 18+ and Python 3.10+

---

## Step 1: Create a Supabase Project

1. Go to [app.supabase.com](https://app.supabase.com) and sign in.
2. Click **New project**.
3. Choose your organisation (or create one).
4. Fill in:
   - **Name:** `kronos-core` (or any name you like)
   - **Database Password:** Generate a strong password and save it somewhere safe.
   - **Region:** Choose the region closest to your users.
5. Click **Create new project**.
6. Wait 1–2 minutes for the project to initialise.

---

## Step 2: Find Your Project URL

1. In your Supabase project, go to **Settings → API** (left sidebar).
2. Under **Project URL**, copy the URL that looks like:
   ```
   https://abcdefghijklmnop.supabase.co
   ```
   This is your `SUPABASE_URL` / `NEXT_PUBLIC_SUPABASE_URL`.

---

## Step 3: Find Your API Keys

Still on **Settings → API**, scroll to **Project API Keys**.

You will see two keys:

### anon (public) key
- Labelled `anon public`
- Safe to use in the browser
- Goes in: **frontend** `NEXT_PUBLIC_SUPABASE_ANON_KEY` AND **backend** `SUPABASE_ANON_KEY`

### service_role key
- Labelled `service_role`
- Has full database access — **NEVER expose to the browser or commit to git**
- Goes in: **backend only** `SUPABASE_SERVICE_ROLE_KEY`

---

## Step 4: Find Your JWT Secret

1. Still on **Settings**, go to **API → JWT Settings**.
2. Copy the **JWT Secret** string.
3. This goes in: **backend only** `JWT_SECRET`

---

## Step 5: Configure the Backend (.env)

In the **project root** (`kronos-core/`), open or create `.env`:

```env
APP_ENV=development
SECRET_KEY=generate-with-python-c-import-secrets-print-secrets-token-hex-32

# Supabase
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-public-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
JWT_SECRET=your-jwt-secret

CORS_ALLOWED_ORIGINS=http://localhost:3000
```

> The `SECRET_KEY` is for internal KRONOS CORE signing — it is NOT the Supabase JWT secret.
> Generate one with: `python -c "import secrets; print(secrets.token_hex(32))"`

---

## Step 6: Configure the Frontend (.env.local)

In `kronos-core/frontend/`, create `.env.local`:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
NEXT_PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-public-key
```

> Only the **anon key** goes here — NEVER the `service_role` key.
> Variables prefixed `NEXT_PUBLIC_` are visible in the browser bundle.

---

## Why the service_role Key Must Never Go in the Frontend

The `service_role` key **bypasses all Row-Level Security policies** — it can read, write, and delete any data in your database without restriction. If it is exposed in the browser:

- Any user who inspects your JS bundle or network requests can extract it.
- They can read every user's data, delete records, or drop tables.
- Supabase will detect the exposure and immediately revoke the key.

**Rule:** `service_role` key → backend `.env` only. Never in `frontend/.env.local`. Never in `NEXT_PUBLIC_*` variables.

---

## Step 7: Run the Database Migration

The KRONOS CORE schema must be applied to your Supabase database.

### Option A: Supabase Dashboard SQL Editor (easiest)

1. Go to **SQL Editor** in the Supabase dashboard.
2. Click **New query**.
3. Paste the contents of `supabase/migrations/001_initial_schema.sql`.
4. Click **Run**.

### Option B: Supabase CLI

```bash
# Install Supabase CLI
npm install -g supabase

# Link your project
supabase login
supabase link --project-ref your-project-id

# Apply migration
supabase db push
```

### Option C: Direct psql

```bash
# Get your database connection string from: Settings → Database → Connection string
psql "postgresql://postgres:password@db.your-project-id.supabase.co:5432/postgres" \
  -f supabase/migrations/001_initial_schema.sql
```

---

## Step 8: Enable Email Authentication

1. In Supabase Dashboard, go to **Authentication → Providers**.
2. Confirm that **Email** is enabled (it is by default).
3. Under **Authentication → Email Templates**, you can customise the confirmation email.

### Disable email confirmation for local testing (optional)

1. Go to **Authentication → Settings**.
2. Under **Email Auth**, toggle **off** "Confirm email".
3. This lets users log in immediately without clicking a confirmation link.

> For production, keep email confirmation enabled.

---

## Step 9: Install the Python Supabase Client (optional for Phase 2+)

Database persistence (Phase 3) requires the Supabase Python client:

```bash
cd kronos-core
pip install supabase PyJWT
```

> The application runs in demo mode without this. You only need it when you want
> blueprints/audits/sandbox results to be saved to the database.

---

## Step 10: Test Register and Login

### Start the backend

```bash
cd kronos-core
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Start the frontend

```bash
cd kronos-core/frontend
npm run dev
```

### Test the auth status

```bash
curl http://127.0.0.1:8000/api/v1/auth/status
```

Expected when configured:
```json
{
  "auth_configured": true,
  "supabase_url_configured": true,
  "anon_key_configured": true,
  "service_role_configured": true,
  "jwt_secret_configured": true,
  "mode": "configured",
  "message": "All auth environment variables are set..."
}
```

### Test the SaaS status page

Open `http://localhost:3000/saas` — the Auth Configuration section should show all green checkmarks.

### Register a user

1. Open `http://localhost:3000/register`.
2. Enter an email and password (min 6 characters).
3. Click **Create account**.
4. If email confirmation is disabled → see success screen → click **Go to Sign in**.
5. If email confirmation is enabled → check your inbox.

### Log in

1. Open `http://localhost:3000/login`.
2. Enter your email and password.
3. Click **Sign in**.
4. You should be redirected to `/dashboard` and see your email in the top-right corner.

---

## Common Errors and Fixes

### "Invalid API key"

Your `NEXT_PUBLIC_SUPABASE_ANON_KEY` or `SUPABASE_ANON_KEY` is wrong. Double-check it in **Settings → API → anon public** — it starts with `eyJ`.

### "Failed to fetch" on login page

The frontend cannot reach the backend. Make sure `uvicorn` is running on port 8000.

### "Email address is already registered"

The email already exists in Supabase. Use a different email or delete the existing user in **Authentication → Users**.

### "Email not confirmed"

Supabase sent a confirmation email. Check your inbox and click the confirmation link, or disable email confirmation in **Authentication → Settings** for local testing.

### "Supabase not configured" warning on login/register page

`NEXT_PUBLIC_SUPABASE_URL` or `NEXT_PUBLIC_SUPABASE_ANON_KEY` is missing from `frontend/.env.local`. Check the file and restart `npm run dev`.

### Dashboard shows "Demo mode" after login

The dashboard shows demo mode when `NEXT_PUBLIC_SUPABASE_URL` is not set. After setting it, restart `npm run dev` to pick up the new env variables.

### "Token has expired" from backend

The Supabase session token has expired. Sign out and sign back in. For production, configure Supabase to auto-refresh tokens.

### Migration SQL fails with "relation auth.users does not exist"

The `auth.users` table is managed by Supabase Auth and exists in all Supabase projects. If you're running against a local PostgreSQL (not Supabase), you'll need to create the `auth` schema and `users` table manually — or use Supabase Local Dev with `supabase start`.

---

## Security Checklist After Setup

- [ ] `.env` is in `.gitignore` — confirmed not tracked by git
- [ ] `frontend/.env.local` is in `.gitignore` — confirmed not tracked
- [ ] `SUPABASE_SERVICE_ROLE_KEY` is NOT in any `frontend/` file
- [ ] `NEXT_PUBLIC_` variables contain only the anon key, not the service role key
- [ ] Email confirmation is enabled in production Supabase settings
- [ ] JWT Secret is at least 32 characters (Supabase generates a 64-char hex secret by default)
- [ ] RLS policies applied via migration — test that users cannot read each other's data
