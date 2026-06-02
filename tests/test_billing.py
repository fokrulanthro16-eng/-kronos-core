"""
Billing endpoint tests.

All tests pass without Stripe configured — every endpoint returns
demo_mode responses when STRIPE_SECRET_KEY is not set.
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ── /billing/status ───────────────────────────────────────────────────────────

def test_billing_status_returns_200():
    resp = client.get("/api/v1/billing/status")
    assert resp.status_code == 200


def test_billing_status_shape():
    resp = client.get("/api/v1/billing/status")
    data = resp.json()
    assert "billing_configured" in data
    assert "demo_mode" in data
    assert "current_plan" in data


def test_billing_status_demo_without_stripe():
    resp = client.get("/api/v1/billing/status")
    data = resp.json()
    assert data["demo_mode"] is True
    assert data["billing_configured"] is False
    assert data["current_plan"] == "free"


# ── /billing/plans ────────────────────────────────────────────────────────────

def test_billing_plans_returns_200():
    resp = client.get("/api/v1/billing/plans")
    assert resp.status_code == 200


def test_billing_plans_shape():
    resp = client.get("/api/v1/billing/plans")
    data = resp.json()
    assert "plans" in data
    assert "demo_mode" in data
    assert isinstance(data["plans"], list)


def test_billing_plans_has_four_tiers():
    resp = client.get("/api/v1/billing/plans")
    plans = resp.json()["plans"]
    assert len(plans) == 4
    ids = [p["id"] for p in plans]
    assert "free" in ids
    assert "starter" in ids
    assert "pro" in ids
    assert "enterprise" in ids


def test_billing_plans_have_required_fields():
    resp = client.get("/api/v1/billing/plans")
    for plan in resp.json()["plans"]:
        assert "id" in plan
        assert "name" in plan
        assert "features" in plan
        assert "cta" in plan
        assert isinstance(plan["features"], list)


def test_billing_plans_pro_is_highlighted():
    resp = client.get("/api/v1/billing/plans")
    pro = next(p for p in resp.json()["plans"] if p["id"] == "pro")
    assert pro["highlight"] is True


# ── /billing/create-checkout-session ─────────────────────────────────────────

def test_checkout_session_demo_mode():
    resp = client.post(
        "/api/v1/billing/create-checkout-session",
        json={"plan": "starter"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("demo_mode") is True
    assert "message" in data


def test_checkout_session_invalid_plan():
    resp = client.post(
        "/api/v1/billing/create-checkout-session",
        json={"plan": "nonexistent"},
    )
    assert resp.status_code == 400


def test_checkout_session_all_valid_plans():
    for plan in ["starter", "pro", "enterprise"]:
        resp = client.post(
            "/api/v1/billing/create-checkout-session",
            json={"plan": plan},
        )
        assert resp.status_code == 200


# ── /billing/webhook ──────────────────────────────────────────────────────────

def test_webhook_demo_mode():
    resp = client.post("/api/v1/billing/webhook")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("demo_mode") is True
