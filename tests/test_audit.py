import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_audit_safe_packages():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/audit",
            json={"packages": ["express", "helmet", "zod", "pino"]},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["summary"]["safe"] == 4
    assert data["summary"]["dangerous"] == 0


@pytest.mark.asyncio
async def test_audit_detects_forbidden_package():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/audit",
            json={"packages": ["event-stream"]},
        )
    assert response.status_code == 200
    result = response.json()["results"][0]
    assert result["risk"] == "DANGEROUS"
    assert result["safe_alternative"] is not None


@pytest.mark.asyncio
async def test_audit_detects_typosquat_expresss():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/audit",
            json={"packages": ["expresss"]},
        )
    assert response.status_code == 200
    result = response.json()["results"][0]
    assert result["risk"] == "TYPOSQUAT"
    assert result["safe_alternative"] == "express"


@pytest.mark.asyncio
async def test_audit_detects_typosquat_lodahs():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/audit",
            json={"packages": ["lodahs"]},
        )
    result = response.json()["results"][0]
    assert result["risk"] == "DANGEROUS"


@pytest.mark.asyncio
async def test_audit_mixed_packages():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/audit",
            json={"packages": ["express", "expresss", "event-stream", "helmet"]},
        )
    data = response.json()
    assert data["summary"]["total"] == 4
    assert data["summary"]["safe"] == 2
    assert data["summary"]["dangerous"] >= 1
    assert "FAIL" in data["summary"]["overall_verdict"]


@pytest.mark.asyncio
async def test_audit_id_format():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/audit",
            json={"packages": ["express"]},
        )
    assert response.json()["audit_id"].startswith("KAU-")


@pytest.mark.asyncio
async def test_audit_unknown_package():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/audit",
            json={"packages": ["some-totally-unknown-xyz-package"]},
        )
    result = response.json()["results"][0]
    assert result["risk"] in ("UNKNOWN", "SUSPICIOUS")


@pytest.mark.asyncio
async def test_audit_rejects_empty_list():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/audit",
            json={"packages": []},
        )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_audit_colors_js_flagged():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/audit",
            json={"packages": ["colors.js"]},
        )
    result = response.json()["results"][0]
    assert result["risk"] == "DANGEROUS"


@pytest.mark.asyncio
async def test_audit_crossenv_typosquat():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/audit",
            json={"packages": ["crossenv"]},
        )
    result = response.json()["results"][0]
    assert result["risk"] == "DANGEROUS"
