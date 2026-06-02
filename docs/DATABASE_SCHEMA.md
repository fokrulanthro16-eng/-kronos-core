# KRONOS CORE — Database Schema

This document describes the planned PostgreSQL schema for the KRONOS CORE SaaS platform, hosted on Supabase.

The full SQL migration is at: `supabase/migrations/001_initial_schema.sql`

---

## Database: PostgreSQL 15+ via Supabase

**Key conventions:**
- All primary keys are `UUID`, generated with `gen_random_uuid()`
- All tables have `created_at TIMESTAMPTZ DEFAULT NOW()`
- Tables with mutable state have `updated_at` maintained by a trigger
- Row-Level Security (RLS) is enabled on every table
- `organization_id` and `user_id` on audit tables are nullable — records can be created without auth in demo mode and linked later

---

## Table: `users_profile`

Extended profile for each authenticated user. The `id` field mirrors `auth.users.id` from Supabase Auth and is populated automatically by a database trigger on user registration.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK, FK → auth.users | Matches Supabase Auth user ID |
| `email` | TEXT | NOT NULL | User's email address |
| `full_name` | TEXT | | Display name |
| `avatar_url` | TEXT | | Profile picture URL |
| `created_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Account creation time |
| `updated_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last profile update |

**RLS Policy:** Users can only read and update their own row (`auth.uid() = id`).

---

## Table: `organizations`

A workspace that groups users and their audit history. One user can belong to multiple organisations; one organisation has exactly one owner.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | |
| `name` | TEXT | NOT NULL | Display name (e.g. "Acme Engineering") |
| `slug` | TEXT | NOT NULL, UNIQUE | URL-safe identifier (e.g. "acme-engineering") |
| `owner_id` | UUID | NOT NULL, FK → users_profile | The org creator |
| `plan` | TEXT | DEFAULT 'starter', CHECK | One of: `starter`, `team`, `enterprise` |
| `created_at` | TIMESTAMPTZ | NOT NULL | |
| `updated_at` | TIMESTAMPTZ | NOT NULL | |

**Indexes:** `owner_id`, `slug`
**RLS Policy:** Any org member can read; owners/admins can update.

---

## Table: `organization_members`

Many-to-many join between users and organisations. A user's role determines what actions they can perform.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | |
| `organization_id` | UUID | NOT NULL, FK → organizations | |
| `user_id` | UUID | NOT NULL, FK → users_profile | |
| `role` | TEXT | DEFAULT 'member', CHECK | One of: `owner`, `admin`, `member`, `viewer` |
| `created_at` | TIMESTAMPTZ | NOT NULL | |

**Unique constraint:** `(organization_id, user_id)` — a user can hold only one role per org.
**Indexes:** `organization_id`, `user_id`

**Role permissions:**
| Role | Read Reports | Run Audits | Manage Members | Change Plan |
|------|-------------|-----------|---------------|------------|
| `viewer` | ✅ | ❌ | ❌ | ❌ |
| `member` | ✅ | ✅ | ❌ | ❌ |
| `admin` | ✅ | ✅ | ✅ | ❌ |
| `owner` | ✅ | ✅ | ✅ | ✅ |

---

## Table: `blueprint_requests`

Saved output from `POST /api/v1/blueprint`. Stores the full generated blueprint as JSONB for queryability.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | |
| `organization_id` | UUID | FK → organizations, nullable | Null for anonymous/demo requests |
| `user_id` | UUID | FK → users_profile, nullable | Null for unauthenticated requests |
| `objective` | TEXT | NOT NULL | The original plain-English objective |
| `generated_blueprint` | JSONB | NOT NULL | Full blueprint response object |
| `risk_score` | SMALLINT | 0–100 | Overall risk score |
| `created_at` | TIMESTAMPTZ | NOT NULL | |

**Indexes:** `organization_id`, `user_id`, `created_at DESC`

---

## Table: `npm_audit_reports`

Saved output from `POST /api/v1/audit`.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | |
| `organization_id` | UUID | FK → organizations, nullable | |
| `user_id` | UUID | FK → users_profile, nullable | |
| `package_names` | TEXT[] | NOT NULL | Array of submitted package names |
| `audit_result_json` | JSONB | NOT NULL | Full audit response object |
| `overall_verdict` | TEXT | NOT NULL | e.g. "FAIL — dangerous packages detected" |
| `created_at` | TIMESTAMPTZ | NOT NULL | |

**Indexes:** `organization_id`, `user_id`, `created_at DESC`

---

## Table: `sandbox_reports`

Saved output from `GET /api/v1/sandbox`.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | |
| `organization_id` | UUID | FK → organizations, nullable | |
| `user_id` | UUID | FK → users_profile, nullable | |
| `sandbox_result_json` | JSONB | NOT NULL | Full sandbox response |
| `verdict` | TEXT | CHECK | One of: `CLEAN`, `SUSPICIOUS`, `BLOCKED` |
| `demo_mode` | BOOLEAN | DEFAULT FALSE | Whether this was a simulated inspection |
| `created_at` | TIMESTAMPTZ | NOT NULL | |

**Indexes:** `organization_id`, `user_id`, `created_at DESC`

---

## Table: `enterprise_reports`

Saved output from `GET /api/v1/enterprise/report`.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | |
| `organization_id` | UUID | FK → organizations, nullable | |
| `user_id` | UUID | FK → users_profile, nullable | |
| `report_json` | JSONB | NOT NULL | Full enterprise report response |
| `security_score` | SMALLINT | 0–100 | Score at time of generation |
| `enterprise_ready` | BOOLEAN | NOT NULL | Whether score met enterprise threshold |
| `created_at` | TIMESTAMPTZ | NOT NULL | |

**Indexes:** `organization_id`, `security_score DESC`, `created_at DESC`

---

## Table: `subscription_status`

Stripe subscription state per organisation. One row per org (enforced by UNIQUE constraint).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PK | |
| `organization_id` | UUID | NOT NULL, UNIQUE, FK → organizations | |
| `plan` | TEXT | CHECK | `starter`, `team`, `enterprise` |
| `status` | TEXT | CHECK | `trialing`, `active`, `past_due`, `canceled`, `unpaid` |
| `stripe_customer_id` | TEXT | UNIQUE | Stripe customer object ID |
| `stripe_subscription_id` | TEXT | UNIQUE | Stripe subscription object ID |
| `current_period_end` | TIMESTAMPTZ | | Next billing date |
| `created_at` | TIMESTAMPTZ | NOT NULL | |
| `updated_at` | TIMESTAMPTZ | NOT NULL | |

---

## Row-Level Security Summary

All tables have RLS enabled. The RLS policies ensure:

1. **Users** only see their own profile row
2. **Org members** can read reports belonging to their organisation
3. **Owners/admins** can update org settings and manage members
4. **Service role** (used by the FastAPI backend) bypasses RLS for writes
5. **Anonymous users** cannot read any table (policies require `auth.uid()`)

The FastAPI backend uses the **service role key** for database writes (bypasses RLS) and the **anon key** is reserved for future client-side Supabase calls.

---

## Entity Relationship Diagram (Text)

```
auth.users (Supabase managed)
    ↓ (trigger creates profile)
users_profile
    ├── organization_members → organizations
    │                              ├── blueprint_requests
    │                              ├── npm_audit_reports
    │                              ├── sandbox_reports
    │                              ├── enterprise_reports
    │                              └── subscription_status
    ├── blueprint_requests (direct user link)
    ├── npm_audit_reports
    ├── sandbox_reports
    └── enterprise_reports
```

---

## Running the Migration

```bash
# Option 1: Supabase CLI
supabase db push

# Option 2: Direct psql
psql "$DATABASE_URL" -f supabase/migrations/001_initial_schema.sql

# Option 3: Supabase Dashboard → SQL Editor
# Paste the contents of 001_initial_schema.sql and run
```
