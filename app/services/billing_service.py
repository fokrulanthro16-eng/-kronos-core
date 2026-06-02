"""
Billing service.

In demo mode (STRIPE_SECRET_KEY not set): every method returns a safe
demo-mode response.  No Stripe calls, no charges, no errors.

In SaaS mode (STRIPE_SECRET_KEY set + stripe package installed): real
checkout sessions and webhook processing are available.
"""
from __future__ import annotations

from typing import Optional
import structlog

from app.config import settings

log = structlog.get_logger()

# ── Plan definitions ──────────────────────────────────────────────────────────

PLANS = [
    {
        "id": "free",
        "name": "Free",
        "price_monthly": 0,
        "price_label": "$0 / month",
        "description": "Local demo — explore every KRONOS CORE feature with no commitment.",
        "limits": {
            "reports_per_day": 10,
            "history_saved": False,
            "pdf_export": False,
            "team_members": 1,
        },
        "features": [
            "Blueprint generation",
            "NPM package audit",
            "Sandbox inspection",
            "Enterprise report view",
            "Security score",
            "API access (rate-limited)",
        ],
        "cta": "Start Free",
        "highlight": False,
    },
    {
        "id": "starter",
        "name": "Starter",
        "price_monthly": 49,
        "price_label": "$49 / month",
        "description": "For solo developers and small teams shipping secure AI applications.",
        "limits": {
            "reports_per_day": 100,
            "history_saved": True,
            "pdf_export": True,
            "team_members": 3,
        },
        "features": [
            "Everything in Free",
            "Saved report history",
            "PDF export for all reports",
            "3 team members",
            "Email support",
            "Higher API rate limits",
        ],
        "cta": "Upgrade to Starter",
        "highlight": False,
    },
    {
        "id": "pro",
        "name": "Pro",
        "price_monthly": 149,
        "price_label": "$149 / month",
        "description": "For growing teams that need organisation workspaces and priority support.",
        "limits": {
            "reports_per_day": -1,
            "history_saved": True,
            "pdf_export": True,
            "team_members": 25,
        },
        "features": [
            "Everything in Starter",
            "Unlimited reports",
            "Organisation workspace",
            "25 team members",
            "Role-based access control",
            "Priority support (< 4 hr response)",
            "Custom report branding",
        ],
        "cta": "Upgrade to Pro",
        "highlight": True,
    },
    {
        "id": "enterprise",
        "name": "Enterprise",
        "price_monthly": None,
        "price_label": "Custom pricing",
        "description": "For banks, government teams, and institutions that need self-hosted deployment and SLA.",
        "limits": {
            "reports_per_day": -1,
            "history_saved": True,
            "pdf_export": True,
            "team_members": -1,
        },
        "features": [
            "Everything in Pro",
            "Self-hosted deployment",
            "Unlimited team members",
            "99.9 % uptime SLA",
            "Dedicated support engineer",
            "Custom integrations",
            "Compliance reporting (SOC 2, ISO 27001)",
            "On-premise option",
        ],
        "cta": "Contact Sales",
        "highlight": False,
    },
]

_PRICE_ID_MAP = {
    "starter":    lambda: settings.stripe_price_starter,
    "pro":        lambda: settings.stripe_price_pro,
    "enterprise": lambda: settings.stripe_price_enterprise,
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def stripe_available() -> bool:
    """True only when STRIPE_SECRET_KEY is set AND the stripe package is installed."""
    if not settings.stripe_configured:
        return False
    try:
        import stripe  # noqa: F401
        return True
    except ImportError:
        return False


def get_billing_status() -> dict:
    return {
        "billing_configured": settings.stripe_configured,
        "stripe_package_installed": stripe_available(),
        "webhook_configured": bool(settings.stripe_webhook_secret),
        "demo_mode": not settings.stripe_configured,
        "current_plan": "free",
        "message": (
            None if settings.stripe_configured
            else "Stripe is not configured — running in demo mode. "
                 "Add STRIPE_SECRET_KEY to .env to activate billing."
        ),
        "plans_count": len(PLANS),
    }


def create_checkout_session(plan_id: str, success_url: str, cancel_url: str) -> dict:
    """
    Create a Stripe Checkout session for the given plan.
    Returns demo-mode dict if Stripe is not configured.
    """
    if not settings.stripe_configured:
        return {
            "demo_mode": True,
            "message": (
                "Stripe billing is not configured. "
                "Set STRIPE_SECRET_KEY, STRIPE_PRICE_<PLAN>, and STRIPE_WEBHOOK_SECRET "
                "in your .env file to activate checkout."
            ),
            "setup_docs": "docs/BILLING_AND_SUBSCRIPTIONS.md",
        }

    price_id_fn = _PRICE_ID_MAP.get(plan_id)
    if price_id_fn is None:
        return {"error": f"Unknown plan: {plan_id}"}

    price_id = price_id_fn()
    if not price_id:
        return {
            "demo_mode": True,
            "message": f"Price ID for plan '{plan_id}' is not configured (STRIPE_PRICE_{plan_id.upper()} is empty).",
        }

    try:
        import stripe as stripe_lib
        stripe_lib.api_key = settings.stripe_secret_key
        session = stripe_lib.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": 1}],
            mode="subscription",
            success_url=success_url,
            cancel_url=cancel_url,
        )
        log.info("stripe_checkout_created", plan=plan_id, session_id=session.id)
        return {"checkout_url": session.url, "session_id": session.id}
    except ImportError:
        return {
            "demo_mode": True,
            "message": "The 'stripe' Python package is not installed. Run: pip install stripe",
        }
    except Exception as exc:
        log.error("stripe_checkout_error", plan=plan_id, error=str(exc))
        return {"error": "Checkout session creation failed — check Stripe configuration."}
