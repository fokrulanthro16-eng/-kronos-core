# KRONOS CORE — Local Environment Setup

This guide explains how to configure your local environment variables so the backend and frontend run correctly, with or without Supabase auth enabled.

> **Security rule:** `.env` and `.env.local` are listed in `.gitignore` and will never be committed to GitHub. Only the `.env.example` templates are committed.

---

## Part 1 — Frontend Environment (Next.js)

### Step 1: Copy the example file

**PowerShell:**
```powershell
cd C:\Users\WALTON\kronos-core\frontend
copy .env.example .env.local
notepad .env.local
```

**macOS / Linux:**
```bash
cd kronos-core/frontend
cp .env.example .env.local
```

### Step 2: Fill in the values

Open `frontend/.env.local` and set:

| Variable | Where to find it | Required? |
|----------|-----------------|-----------|
| `NEXT_PUBLIC_API_BASE_URL` | Leave as `http://127.0.0.1:8000` for local dev | Yes |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase Dashboard → Settings → API → Project URL | Only for auth |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase Dashboard → Settings → API → anon public key | Only for auth |

**For demo mode** (no auth): leave `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` blank. The frontend will display "Demo mode" and login/register pages will show a setup notice.

**For real auth**: fill in both Supabase values. See `docs/SUPABASE_AUTH_SETUP.md`.

### What the completed file looks like

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
NEXT_PUBLIC_SUPABASE_URL=https://abcdefghijklmnop.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Part 2 — Backend Environment (FastAPI)

### Step 1: Copy the example file

**PowerShell:**
```powershell
cd C:\Users\WALTON\kronos-core
copy .env.example .env
notepad .env
```

**macOS / Linux:**
```bash
cd kronos-core
cp .env.example .env
```

### Step 2: Fill in the values

| Variable | Value | Required? |
|----------|-------|-----------|
| `APP_ENV` | `development` | Yes |
| `SECRET_KEY` | Generate below | Yes |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:3000` for local dev | Yes |
| `SUPABASE_URL` | Same as `NEXT_PUBLIC_SUPABASE_URL` | Only for auth |
| `SUPABASE_ANON_KEY` | Same as `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Only for auth |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase → Settings → API → service_role key | Only for auth |
| `JWT_SECRET` | Supabase → Settings → API → JWT Settings → JWT Secret | Only for auth |

### Generate a SECRET_KEY

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output into `.env` as `SECRET_KEY=<output>`.

### What the completed file looks like

```env
APP_NAME=KRONOS CORE
APP_VERSION=1.0.0
APP_ENV=development
SECRET_KEY=a3f8c2d1e9b4...  (64 hex chars)

CORS_ALLOWED_ORIGINS=http://localhost:3000
RATE_LIMIT_PER_MINUTE=60
LOG_LEVEL=INFO
PORT=8000

SUPABASE_URL=https://abcdefghijklmnop.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
JWT_SECRET=your-supabase-jwt-secret
```

---

## Security Rules — Never Break These

| Rule | Why |
|------|-----|
| Never put `SUPABASE_SERVICE_ROLE_KEY` in `frontend/.env.local` | It bypasses all Row-Level Security — any user who views your JS bundle gets full database access |
| Never commit `.env` | Contains real secrets |
| Never commit `frontend/.env.local` | Contains real keys |
| Never paste `service_role` key into Supabase SQL Editor | The editor log could expose it |
| `NEXT_PUBLIC_*` variables are visible in the browser | Only put the anon/public key here |

---

## Verify Everything is Safe

Run these checks before committing:

```powershell
# From project root
git status
```

You should see `.env` and `frontend/.env.local` are **NOT** listed — they're protected by `.gitignore`.

You **should** see these in `git status`:
- `.env.example` (safe — placeholder values only)
- `frontend/.env.example` (safe — placeholder values only)

---

## Start the Application

Once both `.env` files are in place:

```powershell
# Terminal 1 — Backend
cd C:\Users\WALTON\kronos-core
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2 — Frontend
cd C:\Users\WALTON\kronos-core\frontend
npm run dev
```

Visit:
- `http://localhost:3000` — frontend
- `http://127.0.0.1:8000/docs` — API documentation
- `http://localhost:3000/saas` — SaaS configuration status page
