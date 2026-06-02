# KRONOS CORE — GitHub Push Checklist

Run through this checklist every time before pushing to GitHub.

---

## Pre-Push Validation

### Step 1: Run backend tests

```powershell
cd C:\Users\WALTON\kronos-core
python -m pytest -q
```

Expected: `50 passed, 0 failed`

If any test fails, fix the issue before pushing.

---

### Step 2: Run frontend build

```powershell
cd C:\Users\WALTON\kronos-core\frontend
npm run build
```

Expected: `✓ Compiled successfully` with all pages listed.

If the build fails, fix the issue before pushing.

---

### Step 3: Run `git status` and verify the file list

```powershell
cd C:\Users\WALTON\kronos-core
git status
```

#### Files that must NOT appear (secrets / build artifacts)

| File | Why it must NOT be present |
|------|---------------------------|
| `.env` | Contains real SECRET_KEY, JWT_SECRET, Supabase keys |
| `frontend/.env.local` | Contains real Supabase keys |
| `.venv/` | Local Python virtual environment |
| `node_modules/` | Installed packages (frontend) |
| `frontend/node_modules/` | Installed packages |
| `frontend/.next/` | Next.js build cache |
| `__pycache__/` | Python bytecode |
| `.pytest_cache/` | Test cache |

If any of these appear, **do not push**. Check `.gitignore` and fix the issue first.

#### Files that MUST appear (safe to push)

| File | Notes |
|------|-------|
| `README.md` | Product documentation |
| `.env.example` | Placeholder template — no real values |
| `frontend/.env.example` | Placeholder template — no real values |
| `.gitignore` | Protects secrets |
| `app/` (directory) | Backend source code |
| `frontend/app/` | Frontend pages |
| `frontend/components/` | Frontend components |
| `frontend/lib/` | Frontend utilities and auth helpers |
| `supabase/migrations/001_initial_schema.sql` | Database schema — no secrets |
| `docs/` (directory) | All documentation files |
| `pitch/` (directory) | Competition and sales materials |
| `tests/` (directory) | Backend test suite |
| `requirements.txt` | Python dependencies |
| `frontend/package.json` | Node.js dependencies |
| `Dockerfile` | Container build file |
| `docker-compose.yml` | Container orchestration |
| `pytest.ini` | Test configuration |
| `nginx/nginx.conf` | Reverse proxy config |
| `data/` | Static data files |

---

## First-Time Push to GitHub

### Create the repository on GitHub

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `kronos-core`
3. Description: `Autonomous Security & Prompt Architecture Gateway`
4. Visibility: Public or Private (your choice)
5. **Do not** initialise with README, .gitignore, or licence — the project has all of these
6. Click **Create repository**
7. Copy the repository URL (looks like `https://github.com/yourusername/kronos-core.git`)

### Stage and commit

Use explicit file names — never `git add .` or `git add -A` which can accidentally stage `.env`:

```powershell
cd C:\Users\WALTON\kronos-core

git add README.md
git add .env.example
git add .gitignore
git add Dockerfile
git add docker-compose.yml
git add pytest.ini
git add requirements.txt
git add app
git add data
git add docs
git add frontend
git add nginx
git add pitch
git add supabase
git add tests
```

### Verify only safe files are staged

```powershell
git status
```

Confirm again that `.env`, `frontend/.env.local`, `node_modules/`, `.venv/` are not in the staged list.

### Commit

```powershell
git commit -m "Release KRONOS CORE SaaS-ready security gateway v1"
```

### Connect remote and push

```powershell
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

Replace `YOUR_GITHUB_REPO_URL` with the URL you copied from GitHub (e.g. `https://github.com/yourusername/kronos-core.git`).

---

## Subsequent Pushes

After the first push, use:

```powershell
cd C:\Users\WALTON\kronos-core
git add -p    # stage changes interactively, reviewing each one
# OR stage specific files explicitly:
git add app/some-file.py frontend/app/some-page.tsx
git commit -m "Your commit message"
git push
```

---

## Emergency: If You Accidentally Committed a Secret

If a real key was committed:

1. **Immediately revoke the key** in your Supabase dashboard before anything else.
2. Generate new keys in Supabase.
3. Remove the secret from git history:
   ```powershell
   git rm --cached .env
   git commit -m "Remove accidentally committed .env"
   git push
   ```
4. If the commit has already been pushed, contact GitHub Support to purge the history, as the key may be cached.
5. Update `.gitignore` to prevent it happening again.
6. Update your `.env` with the new keys.

The only safe assumption after a key is pushed publicly is that it has been compromised — always revoke and regenerate.
