import structlog
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field

from app.config import settings
from app.middleware.rate_limiter import limiter
from app.services.billing_service import (
    PLANS,
    get_billing_status,
    create_checkout_session,
    stripe_available,
)

log = structlog.get_logger()
router = APIRouter(prefix="/api/v1/billing", tags=["Billing"])


class CheckoutRequest(BaseModel):
    plan: str = Field(..., description="Plan ID: starter | pro | enterprise")
    success_url: str = Field(default="http://localhost:3000/account?upgrade=success")
    cancel_url: str = Field(default="http://localhost:3000/pricing")


@router.get("/status", summary="Billing configuration status")
@limiter.limit("30/minute")
async def billing_status(request: Request):
    log.info("billing_status_request")
    return get_billing_status()


@router.get("/plans", summary="Available subscription plans and features")
@limiter.limit("30/minute")
async def billing_plans(request: Request):
    log.info("billing_plans_request")
    return {
        "plans": PLANS,
        "billing_configured": settings.stripe_configured,
        "demo_mode": not settings.stripe_configured,
    }


@router.post("/create-checkout-session", summary="Create a Stripe checkout session for plan upgrade")
@limiter.limit("10/minute")
async def checkout_session(request: Request, body: CheckoutRequest):
    log.info("checkout_session_request", plan=body.plan)
    valid_plans = {"starter", "pro", "enterprise"}
    if body.plan not in valid_plans:
        raise HTTPException(status_code=400, detail=f"Invalid plan. Choose from: {', '.join(sorted(valid_plans))}")
    result = create_checkout_session(body.plan, body.success_url, body.cancel_url)
    return result


@router.post("/webhook", summary="Stripe webhook event receiver")
@limiter.limit("60/minute")
async def stripe_webhook(request: Request):
    if not settings.stripe_webhook_secret:
        log.info("webhook_demo_mode")
        return {
            "demo_mode": True,
            "message": (
                "Webhook endpoint is active but STRIPE_WEBHOOK_SECRET is not configured. "
                "Add it to .env to enable live webhook processing."
            ),
        }

    if not stripe_available():
        raise HTTPException(status_code=501, detail="stripe package not installed: pip install stripe")

    try:
        import stripe as stripe_lib

        payload = await request.body()
        sig_header = request.headers.get("stripe-signature", "")

        event = stripe_lib.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
        event_type = event.get("type", "unknown")
        log.info("stripe_webhook_received", event_type=event_type)

        if event_type == "checkout.session.completed":
            log.info("stripe_checkout_completed", session_id=event["data"]["object"].get("id"))
        elif event_type == "customer.subscription.deleted":
            log.info("stripe_subscription_cancelled")

        return {"received": True, "event_type": event_type}

    except Exception as exc:
        log.error("stripe_webhook_error", error=str(exc))
        raise HTTPException(status_code=400, detail="Webhook processing failed")
