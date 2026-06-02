# KRONOS CORE — PDF Export

## What PDF export does

Generates clean, branded PDF reports from live KRONOS CORE data.
No external services, no network calls, no secrets in output.
Built with reportlab — pure Python, zero browser dependencies.

## Endpoints

| Endpoint | Description | Filename |
|---|---|---|
| `GET /api/v1/export/enterprise/pdf` | Current enterprise readiness report | `kronos-enterprise-report.pdf` |
| `GET /api/v1/export/demo/pdf` | Competition / investor pitch summary PDF | `kronos-demo-report.pdf` |
| `GET /api/v1/history/enterprise/{id}/pdf` | Per-record export (returns 501 — not yet implemented) | — |

All PDF endpoints return `Content-Type: application/pdf` with `Content-Disposition: attachment`.

## How to test

1. Start backend: `python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
2. Open in browser or curl:

```bash
curl -o enterprise.pdf http://127.0.0.1:8000/api/v1/export/enterprise/pdf
curl -o demo.pdf http://127.0.0.1:8000/api/v1/export/demo/pdf
```

3. Or click **Download PDF** on `http://localhost:3000/enterprise`
4. Or switch to **Enterprise** tab on `http://localhost:3000/history`

## Security notes

- PDFs are generated in-memory (no disk writes)
- No secrets, env values, or keys are included in any PDF
- Rate limited to 10 requests/minute per IP
- No external fonts or assets fetched at runtime

## PDF library

`reportlab>=4.2.0` — pure Python, no system dependencies.

Install: `pip install reportlab`

## What remains for paid SaaS PDF exports

- Per-record PDF download from history (`/history/enterprise/{id}/pdf`)
- Blueprint PDF with full Claude execution prompt
- Audit PDF with full package table
- Branded cover page with customer logo (Phase 5+ — premium tier)
- Watermark removal for paid plans
- Stripe-gated PDF download (Phase 6)
