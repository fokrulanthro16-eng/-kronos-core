"""PDF export endpoint tests."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_enterprise_pdf_returns_200():
    resp = client.get("/api/v1/export/enterprise/pdf")
    assert resp.status_code == 200


def test_enterprise_pdf_content_type():
    resp = client.get("/api/v1/export/enterprise/pdf")
    assert "application/pdf" in resp.headers["content-type"]


def test_enterprise_pdf_body_is_pdf():
    resp = client.get("/api/v1/export/enterprise/pdf")
    assert resp.content[:4] == b"%PDF"


def test_enterprise_pdf_has_attachment_header():
    resp = client.get("/api/v1/export/enterprise/pdf")
    assert "attachment" in resp.headers.get("content-disposition", "")
    assert ".pdf" in resp.headers.get("content-disposition", "")


def test_demo_pdf_returns_200():
    resp = client.get("/api/v1/export/demo/pdf")
    assert resp.status_code == 200


def test_demo_pdf_content_type():
    resp = client.get("/api/v1/export/demo/pdf")
    assert "application/pdf" in resp.headers["content-type"]


def test_demo_pdf_body_is_pdf():
    resp = client.get("/api/v1/export/demo/pdf")
    assert resp.content[:4] == b"%PDF"


def test_history_enterprise_pdf_stub_returns_501():
    resp = client.get("/api/v1/history/enterprise/some-id-123/pdf")
    assert resp.status_code == 501
    assert "not yet implemented" in resp.json()["detail"].lower()
