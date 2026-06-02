import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_health_returns_200():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_contains_required_fields():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/health")
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "KRONOS CORE"
    assert "version" in data
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_root_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/")
    assert response.status_code == 200
    data = response.json()
    assert "endpoints" in data
    assert data["product"] == "KRONOS CORE"


@pytest.mark.asyncio
async def test_security_headers_present():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/health")
    assert "x-content-type-options" in response.headers
    assert "x-frame-options" in response.headers
    assert "strict-transport-security" in response.headers
    assert response.headers["x-frame-options"] == "DENY"


@pytest.mark.asyncio
async def test_404_returns_json():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
