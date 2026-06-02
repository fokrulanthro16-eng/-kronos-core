import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


VALID_OBJECTIVE = "Build a secure REST API for a fintech payment processing system with JWT authentication"


@pytest.mark.asyncio
async def test_blueprint_generation_success():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/blueprint", json={"objective": VALID_OBJECTIVE})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_blueprint_contains_required_fields():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/blueprint", json={"objective": VALID_OBJECTIVE})
    data = response.json()
    required = [
        "blueprint_id", "generated_at", "objective_summary",
        "directory_architecture", "secure_coding_standards",
        "package_policy", "static_audit_instructions",
        "dynamic_sandbox_instructions", "deployment_checklist",
        "risk_score", "production_readiness_checklist", "claude_execution_prompt",
    ]
    for field in required:
        assert field in data, f"Missing field: {field}"


@pytest.mark.asyncio
async def test_blueprint_id_format():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/blueprint", json={"objective": VALID_OBJECTIVE})
    data = response.json()
    assert data["blueprint_id"].startswith("KBP-")


@pytest.mark.asyncio
async def test_blueprint_package_policy():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/blueprint", json={"objective": VALID_OBJECTIVE})
    policy = response.json()["package_policy"]
    assert "express" in policy["allowed"]
    assert "event-stream" in policy["forbidden"]
    assert len(policy["allowed"]) > 5
    assert len(policy["forbidden"]) > 5


@pytest.mark.asyncio
async def test_blueprint_risk_score_structure():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/blueprint", json={"objective": VALID_OBJECTIVE})
    score = response.json()["risk_score"]
    assert 0 <= score["overall"] <= 100
    assert score["level"] in ("LOW", "MEDIUM", "HIGH", "CRITICAL")


@pytest.mark.asyncio
async def test_blueprint_claude_prompt_contains_objective():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/blueprint",
            json={"objective": VALID_OBJECTIVE, "tech_stack": "Node.js"},
        )
    prompt = response.json()["claude_execution_prompt"]
    assert "KRONOS CORE" in prompt
    assert "INPUT VALIDATION" in prompt


@pytest.mark.asyncio
async def test_blueprint_rejects_short_objective():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/blueprint", json={"objective": "short"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_blueprint_fintech_adds_audit_directory():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/v1/blueprint",
            json={"objective": "Build a fintech payment gateway with PCI-DSS compliance"},
        )
    dirs = [d["path"] for d in response.json()["directory_architecture"]]
    assert any("audit" in d for d in dirs)
