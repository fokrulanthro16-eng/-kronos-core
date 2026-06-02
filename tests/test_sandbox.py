import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_sandbox_returns_200():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/sandbox?demo=true")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_sandbox_contains_required_fields():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/sandbox?demo=true")
    data = response.json()
    required = [
        "inspection_id", "inspected_at", "demo_mode",
        "process_summary", "network_summary", "file_summary",
        "verdict", "findings", "passed_checks", "blocked_actions", "executive_note",
    ]
    for field in required:
        assert field in data, f"Missing field: {field}"


@pytest.mark.asyncio
async def test_sandbox_inspection_id_format():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/sandbox")
    assert response.json()["inspection_id"].startswith("KSB-")


@pytest.mark.asyncio
async def test_sandbox_demo_mode_shows_blocked_actions():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/sandbox?demo=true")
    data = response.json()
    assert data["demo_mode"] is True
    assert len(data["blocked_actions"]) > 0
    assert any("DEMO" in action for action in data["blocked_actions"])


@pytest.mark.asyncio
async def test_sandbox_verdict_is_valid():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/sandbox?demo=true")
    verdict = response.json()["verdict"]
    assert verdict in ("CLEAN", "SUSPICIOUS", "BLOCKED")


@pytest.mark.asyncio
async def test_sandbox_process_summary_structure():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/sandbox?demo=true")
    proc = response.json()["process_summary"]
    assert "total_processes" in proc
    assert "high_cpu_processes" in proc
    assert "suspicious_processes" in proc
    assert isinstance(proc["total_processes"], int)


@pytest.mark.asyncio
async def test_sandbox_network_summary_structure():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/sandbox?demo=true")
    net = response.json()["network_summary"]
    assert "open_connections" in net
    assert "exfiltration_risk" in net
    assert isinstance(net["exfiltration_risk"], bool)


@pytest.mark.asyncio
async def test_sandbox_passed_checks_non_empty():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/sandbox?demo=true")
    data = response.json()
    assert len(data["passed_checks"]) > 0
