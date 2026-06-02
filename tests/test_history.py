"""
History endpoint tests.

All tests must pass without Supabase configured — every endpoint returns
demo_mode=True and empty lists when the database is not available.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_history_root_returns_200():
    resp = client.get("/api/v1/history")
    assert resp.status_code == 200


def test_history_root_shape():
    resp = client.get("/api/v1/history")
    data = resp.json()
    assert "demo_mode" in data
    assert "blueprints" in data
    assert "audits" in data
    assert "sandbox" in data
    assert "enterprise" in data


def test_history_root_demo_mode_without_supabase():
    resp = client.get("/api/v1/history")
    data = resp.json()
    assert data["demo_mode"] is True
    assert isinstance(data["blueprints"], list)
    assert isinstance(data["audits"], list)
    assert isinstance(data["sandbox"], list)
    assert isinstance(data["enterprise"], list)


def test_history_blueprints_returns_200():
    resp = client.get("/api/v1/history/blueprints")
    assert resp.status_code == 200


def test_history_blueprints_shape():
    resp = client.get("/api/v1/history/blueprints")
    data = resp.json()
    assert "demo_mode" in data
    assert "records" in data
    assert "count" in data
    assert isinstance(data["records"], list)
    assert data["count"] == len(data["records"])


def test_history_audits_returns_200():
    resp = client.get("/api/v1/history/audits")
    assert resp.status_code == 200


def test_history_audits_shape():
    resp = client.get("/api/v1/history/audits")
    data = resp.json()
    assert "demo_mode" in data
    assert "records" in data
    assert "count" in data


def test_history_sandbox_returns_200():
    resp = client.get("/api/v1/history/sandbox")
    assert resp.status_code == 200


def test_history_sandbox_shape():
    resp = client.get("/api/v1/history/sandbox")
    data = resp.json()
    assert "demo_mode" in data
    assert "records" in data
    assert "count" in data


def test_history_enterprise_returns_200():
    resp = client.get("/api/v1/history/enterprise")
    assert resp.status_code == 200


def test_history_enterprise_shape():
    resp = client.get("/api/v1/history/enterprise")
    data = resp.json()
    assert "demo_mode" in data
    assert "records" in data
    assert "count" in data


def test_all_history_endpoints_empty_without_db():
    for path in ["/blueprints", "/audits", "/sandbox", "/enterprise"]:
        resp = client.get(f"/api/v1/history{path}")
        data = resp.json()
        assert data["count"] == 0
        assert data["records"] == []
