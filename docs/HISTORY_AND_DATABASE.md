# KRONOS CORE — History & Database

## How saved reports work

When Supabase is configured, every successful API call to the following endpoints automatically saves its result to the database:

| Endpoint | Table |
|---|---|
| `POST /api/v1/blueprint` | `blueprint_requests` |
| `POST /api/v1/audit` | `npm_audit_reports` |
| `GET /api/v1/sandbox` | `sandbox_reports` |
| `GET /api/v1/enterprise/report` | `enterprise_reports` |

If Supabase is **not** configured, saving is skipped silently — the API response is unaffected.

## Tables used

| Table | Key columns |
|---|---|
| `blueprint_requests` | `id`, `objective`, `generated_blueprint` (jsonb), `risk_score`, `created_at` |
| `npm_audit_reports` | `id`, `package_names` (jsonb), `audit_result_json` (jsonb), `overall_verdict`, `created_at` |
| `sandbox_reports` | `id`, `sandbox_result_json` (jsonb), `verdict`, `demo_mode`, `created_at` |
| `enterprise_reports` | `id`, `report_json` (jsonb), `enterprise_ready`, `created_at` |

All tables have Row-Level Security (RLS) enabled.

## How to run the Supabase migration manually

1. Open [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project
3. Go to **SQL Editor → New Query**
4. Paste the full contents of `supabase/migrations/001_initial_schema.sql`
5. Click **Run**

This creates all tables, RLS policies, indexes, and the user profile trigger.

## How to test

1. Start the backend: `python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
2. Start the frontend: `cd frontend && npm run dev`
3. Generate a report via any of:
   - `http://localhost:3000/blueprint`
   - `http://localhost:3000/audit`
   - `http://localhost:3000/sandbox`
   - `http://localhost:3000/enterprise`
4. Open `http://localhost:3000/history` to see saved reports
5. Or call the API directly: `http://127.0.0.1:8000/api/v1/history`

## History API endpoints

| Endpoint | Description |
|---|---|
| `GET /api/v1/history` | All recent reports grouped by type |
| `GET /api/v1/history/blueprints` | Saved blueprint reports |
| `GET /api/v1/history/audits` | Saved NPM audit reports |
| `GET /api/v1/history/sandbox` | Saved sandbox inspection reports |
| `GET /api/v1/history/enterprise` | Saved enterprise readiness reports |

All endpoints return `demo_mode: true` when Supabase is not configured.

## What remains for PDF export

- Phase 5 (next): Add a `GET /api/v1/history/blueprints/{id}/pdf` endpoint
- Use `weasyprint` or `reportlab` to render the stored `generated_blueprint` JSON as a styled PDF
- Add download button to the History page record cards
