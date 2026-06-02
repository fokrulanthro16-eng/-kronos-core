-- ─────────────────────────────────────────────────────────────────────────────
-- KRONOS CORE — Initial SaaS Schema
-- Migration: 001_initial_schema.sql
-- Target:    Supabase (PostgreSQL 15+)
--
-- Run via:
--   supabase db push          (using Supabase CLI)
--   psql $DATABASE_URL -f supabase/migrations/001_initial_schema.sql
--
-- All tables use:
--   • UUID primary keys (gen_random_uuid())
--   • created_at / updated_at timestamps
--   • Row-Level Security enabled (policies added separately per auth strategy)
-- ─────────────────────────────────────────────────────────────────────────────

-- ── Extensions ────────────────────────────────────────────────────────────────
-- gen_random_uuid() is built into Supabase; pgcrypto adds it for plain Postgres.
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ─────────────────────────────────────────────────────────────────────────────
-- 1. users_profile
--    Extended profile — mirrors auth.users provided by Supabase Auth.
--    id = auth.users.id  (set by the auth trigger below)
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.users_profile (
    id            UUID        PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email         TEXT        NOT NULL,
    full_name     TEXT,
    avatar_url    TEXT,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Auto-create profile row when a new Supabase Auth user registers.
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER LANGUAGE plpgsql SECURITY DEFINER AS $$
BEGIN
    INSERT INTO public.users_profile (id, email)
    VALUES (NEW.id, NEW.email)
    ON CONFLICT (id) DO NOTHING;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ─────────────────────────────────────────────────────────────────────────────
-- 2. organizations
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.organizations (
    id         UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    name       TEXT        NOT NULL,
    slug       TEXT        NOT NULL UNIQUE,
    owner_id   UUID        NOT NULL REFERENCES public.users_profile(id) ON DELETE RESTRICT,
    plan       TEXT        NOT NULL DEFAULT 'starter'
                           CHECK (plan IN ('starter', 'team', 'enterprise')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_organizations_owner   ON public.organizations(owner_id);
CREATE INDEX IF NOT EXISTS idx_organizations_slug    ON public.organizations(slug);

-- ─────────────────────────────────────────────────────────────────────────────
-- 3. organization_members
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.organization_members (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID        NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
    user_id         UUID        NOT NULL REFERENCES public.users_profile(id) ON DELETE CASCADE,
    role            TEXT        NOT NULL DEFAULT 'member'
                                CHECK (role IN ('owner', 'admin', 'member', 'viewer')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (organization_id, user_id)
);

CREATE INDEX IF NOT EXISTS idx_org_members_org  ON public.organization_members(organization_id);
CREATE INDEX IF NOT EXISTS idx_org_members_user ON public.organization_members(user_id);

-- ─────────────────────────────────────────────────────────────────────────────
-- 4. blueprint_requests
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.blueprint_requests (
    id                  UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id     UUID        REFERENCES public.organizations(id) ON DELETE SET NULL,
    user_id             UUID        REFERENCES public.users_profile(id) ON DELETE SET NULL,
    objective           TEXT        NOT NULL,
    generated_blueprint JSONB       NOT NULL,
    risk_score          SMALLINT    NOT NULL CHECK (risk_score BETWEEN 0 AND 100),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_blueprints_org  ON public.blueprint_requests(organization_id);
CREATE INDEX IF NOT EXISTS idx_blueprints_user ON public.blueprint_requests(user_id);
CREATE INDEX IF NOT EXISTS idx_blueprints_time ON public.blueprint_requests(created_at DESC);

-- ─────────────────────────────────────────────────────────────────────────────
-- 5. npm_audit_reports
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.npm_audit_reports (
    id                UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id   UUID        REFERENCES public.organizations(id) ON DELETE SET NULL,
    user_id           UUID        REFERENCES public.users_profile(id) ON DELETE SET NULL,
    package_names     TEXT[]      NOT NULL,
    audit_result_json JSONB       NOT NULL,
    overall_verdict   TEXT        NOT NULL,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audits_org    ON public.npm_audit_reports(organization_id);
CREATE INDEX IF NOT EXISTS idx_audits_user   ON public.npm_audit_reports(user_id);
CREATE INDEX IF NOT EXISTS idx_audits_time   ON public.npm_audit_reports(created_at DESC);

-- ─────────────────────────────────────────────────────────────────────────────
-- 6. sandbox_reports
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.sandbox_reports (
    id                  UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id     UUID        REFERENCES public.organizations(id) ON DELETE SET NULL,
    user_id             UUID        REFERENCES public.users_profile(id) ON DELETE SET NULL,
    sandbox_result_json JSONB       NOT NULL,
    verdict             TEXT        NOT NULL CHECK (verdict IN ('CLEAN', 'SUSPICIOUS', 'BLOCKED')),
    demo_mode           BOOLEAN     NOT NULL DEFAULT FALSE,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sandbox_org  ON public.sandbox_reports(organization_id);
CREATE INDEX IF NOT EXISTS idx_sandbox_user ON public.sandbox_reports(user_id);
CREATE INDEX IF NOT EXISTS idx_sandbox_time ON public.sandbox_reports(created_at DESC);

-- ─────────────────────────────────────────────────────────────────────────────
-- 7. enterprise_reports
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.enterprise_reports (
    id                UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id   UUID        REFERENCES public.organizations(id) ON DELETE SET NULL,
    user_id           UUID        REFERENCES public.users_profile(id) ON DELETE SET NULL,
    report_json       JSONB       NOT NULL,
    security_score    SMALLINT    NOT NULL CHECK (security_score BETWEEN 0 AND 100),
    enterprise_ready  BOOLEAN     NOT NULL DEFAULT FALSE,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_enterprise_org   ON public.enterprise_reports(organization_id);
CREATE INDEX IF NOT EXISTS idx_enterprise_score ON public.enterprise_reports(security_score DESC);
CREATE INDEX IF NOT EXISTS idx_enterprise_time  ON public.enterprise_reports(created_at DESC);

-- ─────────────────────────────────────────────────────────────────────────────
-- 8. subscription_status
-- ─────────────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.subscription_status (
    id                      UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id         UUID        NOT NULL UNIQUE
                                        REFERENCES public.organizations(id) ON DELETE CASCADE,
    plan                    TEXT        NOT NULL DEFAULT 'starter'
                                        CHECK (plan IN ('starter', 'team', 'enterprise')),
    status                  TEXT        NOT NULL DEFAULT 'trialing'
                                        CHECK (status IN ('trialing', 'active', 'past_due', 'canceled', 'unpaid')),
    stripe_customer_id      TEXT        UNIQUE,
    stripe_subscription_id  TEXT        UNIQUE,
    current_period_end      TIMESTAMPTZ,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sub_org    ON public.subscription_status(organization_id);
CREATE INDEX IF NOT EXISTS idx_sub_stripe ON public.subscription_status(stripe_customer_id);

-- ─────────────────────────────────────────────────────────────────────────────
-- updated_at trigger (shared)
-- ─────────────────────────────────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

DO $$
DECLARE
    t TEXT;
BEGIN
    FOREACH t IN ARRAY ARRAY['users_profile', 'organizations', 'subscription_status']
    LOOP
        EXECUTE format(
            'DROP TRIGGER IF EXISTS trg_updated_at ON public.%I;
             CREATE TRIGGER trg_updated_at
                 BEFORE UPDATE ON public.%I
                 FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();',
            t, t
        );
    END LOOP;
END;
$$;

-- ─────────────────────────────────────────────────────────────────────────────
-- Row-Level Security
-- Enable RLS on every table.  Policies are defined below as a starting point;
-- tighten them once authentication is fully wired in Phase 2.
-- ─────────────────────────────────────────────────────────────────────────────
ALTER TABLE public.users_profile         ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.organizations         ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.organization_members  ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.blueprint_requests    ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.npm_audit_reports     ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sandbox_reports       ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.enterprise_reports    ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.subscription_status   ENABLE ROW LEVEL SECURITY;

-- ── Users can read and update their own profile ───────────────────────────────
CREATE POLICY "users_profile: own row" ON public.users_profile
    FOR ALL USING (auth.uid() = id);

-- ── Org members can read their organisation ───────────────────────────────────
CREATE POLICY "organizations: member read" ON public.organizations
    FOR SELECT USING (
        id IN (
            SELECT organization_id FROM public.organization_members
            WHERE user_id = auth.uid()
        )
    );

-- ── Org owners/admins can update the org ──────────────────────────────────────
CREATE POLICY "organizations: admin write" ON public.organizations
    FOR UPDATE USING (
        id IN (
            SELECT organization_id FROM public.organization_members
            WHERE user_id = auth.uid() AND role IN ('owner', 'admin')
        )
    );

-- ── Members can see their own org memberships ────────────────────────────────
CREATE POLICY "org_members: own rows" ON public.organization_members
    FOR SELECT USING (user_id = auth.uid());

-- ── Audit tables: members of the org can read; service role can write ────────
-- (Phase 2: refine per-operation as auth is wired in)

CREATE POLICY "blueprints: org member read" ON public.blueprint_requests
    FOR SELECT USING (
        organization_id IN (
            SELECT organization_id FROM public.organization_members
            WHERE user_id = auth.uid()
        )
        OR user_id = auth.uid()
    );

CREATE POLICY "audits: org member read" ON public.npm_audit_reports
    FOR SELECT USING (
        organization_id IN (
            SELECT organization_id FROM public.organization_members
            WHERE user_id = auth.uid()
        )
        OR user_id = auth.uid()
    );

CREATE POLICY "sandbox: org member read" ON public.sandbox_reports
    FOR SELECT USING (
        organization_id IN (
            SELECT organization_id FROM public.organization_members
            WHERE user_id = auth.uid()
        )
        OR user_id = auth.uid()
    );

CREATE POLICY "enterprise: org member read" ON public.enterprise_reports
    FOR SELECT USING (
        organization_id IN (
            SELECT organization_id FROM public.organization_members
            WHERE user_id = auth.uid()
        )
        OR user_id = auth.uid()
    );

CREATE POLICY "subscription: org member read" ON public.subscription_status
    FOR SELECT USING (
        organization_id IN (
            SELECT organization_id FROM public.organization_members
            WHERE user_id = auth.uid()
        )
    );

-- ─────────────────────────────────────────────────────────────────────────────
-- End of migration 001
-- ─────────────────────────────────────────────────────────────────────────────
