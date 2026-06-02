import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


FULL_SECURE_PAYLOAD = {
    "packages_audited": 10,
    "packages_flagged": 0,
    "sandbox_passed": True,
    "blueprint_generated": True,
    "docker_hardened": True,
    "input_validation": True,
    "auth_implemented": True,
    "tls_enabled": True,
}

MINIMAL_PAYLOAD = {
    "packages_audited": 0,
    "packages_flagged": 0,
    "sandbox_passed": False,
    "blueprint_generated": False,
    "docker_hardened": False,
    "input_validation": False,
    "auth_implemented": False,
    "tls_enabled": False,
}


@pytest.mark.asyncio
async def test_score_returns_200():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/security/score", json=FULL_SECURE_PAYLOAD)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_score_contains_required_fields():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/security/score", json=FULL_SECURE_PAYLOAD)
    data = response.json()
    required = [
        "score_id", "scored_at", "total_score", "risk_level",
        "categories", "recommendations", "executive_summary", "enterprise_ready",
    ]
    for field in required:
        assert field in data, f"Missing field: {field}"


@pytest.mark.asyncio
async def test_score_id_format():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/security/score", json=FULL_SECURE_PAYLOAD)
    assert response.json()["score_id"].startswith("KSC-")


@pytest.mark.asyncio
async def test_score_fully_secure_system():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/security/score", json=FULL_SECURE_PAYLOAD)
    data = response.json()
    assert data["total_score"] >= 70
    assert data["risk_level"] in ("LOW", "MEDIUM")
    assert data["enterprise_ready"] is True


@pytest.mark.asyncio
async def test_score_minimal_system_is_high_risk():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/security/score", json=MINIMAL_PAYLOAD)
    data = response.json()
    assert data["total_score"] < 50
    assert data["risk_level"] in ("HIGH", "CRITICAL")
    assert data["enterprise_ready"] is False


@pytest.mark.asyncio
async def test_score_has_six_categories():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/security/score", json=FULL_SECURE_PAYLOAD)
    categories = response.json()["categories"]
    assert len(categories) == 6


@pytest.mark.asyncio
async def test_score_categories_have_findings():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/security/score", json=FULL_SECURE_PAYLOAD)
    for cat in response.json()["categories"]:
        assert len(cat["findings"]) > 0
        assert 0 <= cat["score"] <= cat["max_score"]


@pytest.mark.asyncio
async def test_score_total_bounded():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/security/score", json=FULL_SECURE_PAYLOAD)
    total = response.json()["total_score"]
    assert 0 <= total <= 100


@pytest.mark.asyncio
async def test_score_flagged_packages_reduce_score():
    low_risk = {**FULL_SECURE_PAYLOAD, "packages_flagged": 0}
    high_risk = {**FULL_SECURE_PAYLOAD, "packages_flagged": 9}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r1 = await client.post("/api/v1/security/score", json=low_risk)
        r2 = await client.post("/api/v1/security/score", json=high_risk)
    assert r1.json()["total_score"] > r2.json()["total_score"]
