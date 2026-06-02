import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_demo_returns_200():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/demo")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_demo_contains_required_fields():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/demo")
    data = response.json()
    required = [
        "product_name", "tagline", "problem_statement", "solution",
        "target_customers", "market_use_cases", "technical_innovation",
        "security_architecture", "demo_flow", "commercial_value",
        "competition_advantage", "future_roadmap", "pitch_closing",
    ]
    for field in required:
        assert field in data, f"Missing field: {field}"


@pytest.mark.asyncio
async def test_demo_product_name():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/demo")
    assert response.json()["product_name"] == "KRONOS CORE"


@pytest.mark.asyncio
async def test_demo_target_customers_populated():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/demo")
    customers = response.json()["target_customers"]
    assert len(customers) >= 5
    segments = [c["segment"] for c in customers]
    assert any("Bank" in s or "Financial" in s for s in segments)


@pytest.mark.asyncio
async def test_demo_security_architecture_layers():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/demo")
    layers = response.json()["security_architecture"]
    assert len(layers) >= 4
    for layer in layers:
        assert "layer" in layer
        assert "component" in layer
        assert "security_role" in layer


@pytest.mark.asyncio
async def test_demo_flow_steps():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/demo")
    flow = response.json()["demo_flow"]
    assert len(flow) >= 5


@pytest.mark.asyncio
async def test_enterprise_report_returns_200():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/enterprise/report")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_enterprise_report_required_fields():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/enterprise/report")
    data = response.json()
    required = [
        "report_id", "generated_at", "product", "executive_summary",
        "capabilities", "compliance_alignment", "integration_options",
        "deployment_models", "pricing_model", "support_model",
    ]
    for field in required:
        assert field in data, f"Missing field: {field}"


@pytest.mark.asyncio
async def test_enterprise_report_id_format():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/enterprise/report")
    assert response.json()["report_id"].startswith("KER-")


@pytest.mark.asyncio
async def test_enterprise_compliance_alignment():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/enterprise/report")
    compliance = response.json()["compliance_alignment"]
    assert len(compliance) >= 4
    full_text = " ".join(compliance)
    assert "OWASP" in full_text
