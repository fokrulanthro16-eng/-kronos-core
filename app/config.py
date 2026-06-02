from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    # ── Core ──────────────────────────────────────────────────────────────────
    app_name: str = "KRONOS CORE"
    app_version: str = "1.0.0"
    app_env: str = "production"
    secret_key: str = "kronos-core-default-key-change-in-production-32ch"
    rate_limit_per_minute: int = 60
    log_level: str = "INFO"
    port: int = 8000

    # Legacy field name kept for backwards compatibility.
    allowed_origins: str = "http://localhost:3000,http://localhost:8080"
    # New canonical name used by .env.example — maps to the same list.
    cors_allowed_origins: Optional[str] = None

    @property
    def origins_list(self) -> List[str]:
        raw = self.cors_allowed_origins or self.allowed_origins
        return [o.strip() for o in raw.split(",") if o.strip()]

    # ── SaaS Phase 1 — Supabase (all optional) ───────────────────────────────
    # Leave unset for demo/local mode. The application starts and all existing
    # endpoints work without these. They are only required for database
    # persistence features added in SaaS Phase 2+.
    supabase_url: Optional[str] = None
    supabase_service_role_key: Optional[str] = None
    supabase_anon_key: Optional[str] = None
    jwt_secret: Optional[str] = None

    @property
    def supabase_configured(self) -> bool:
        return bool(self.supabase_url and self.supabase_service_role_key)

    @property
    def auth_configured(self) -> bool:
        return bool(self.jwt_secret)

    # ── SaaS Phase 5 — Stripe billing (all optional) ─────────────────────────
    stripe_secret_key: Optional[str] = None
    stripe_webhook_secret: Optional[str] = None
    stripe_price_starter: Optional[str] = None
    stripe_price_pro: Optional[str] = None
    stripe_price_enterprise: Optional[str] = None

    @property
    def stripe_configured(self) -> bool:
        return bool(self.stripe_secret_key)

    model_config = {"env_file": ".env", "case_sensitive": False}


settings = Settings()
