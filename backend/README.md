# Post Preflight — Backend (B1: API & Integration)

Flask JSON API for the Post Preflight readiness check. Owns the
`POST /api/analyze` route, validation, CORS, and error handling. The AI analysis
lives in `backend/analysis/` (B2) and is reached through one seam:
`analyze_post(draft, platform, context) -> dict`.

## Run (Windows / PowerShell)

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # then add your ANTHROPIC_API_KEY (needed in Phase 2)
python app.py            # serves http://localhost:5000
```

On macOS/Linux use `source venv/bin/activate` and `cp .env.example .env`.

## Modes

`USE_STUB` is auto-detected when unset:

- **Live (default once `backend/analysis/` exists):** delegates to B2's
  `analyze_post`. Requires `ANTHROPIC_API_KEY` to be set.
- **Stub (auto fallback before B2 lands, or forced with `USE_STUB=1`):**
  `POST /api/analyze` returns the frozen example response from
  `../shared/contract.example.json`. No API key required — lets F1 integrate
  immediately.

Force either mode with `USE_STUB=1` (always stub) or `USE_STUB=0` (always live).

## API

`POST /api/analyze` — request/response shape is the frozen contract in
`../shared/contract.example.json`.

- **Request:** `{ draft: string, platform: "linkedin"|"x"|"facebook"|"instagram", context?: { audience?, goal?, brandTone? } }`
- **Success:** `200` with `{ platform, risks[], fit{ verdict, overallScore, dimensions[] }, rewrite{ text, summary } }`
- **Errors:** `{ error: string }` with `400` (bad input) or `500` (analysis failure)

`GET /api/health` — `{ status, mode, hasApiKey, platforms[] }` for quick checks.

### Smoke test (stub)

```powershell
curl -X POST http://localhost:5000/api/analyze `
  -H "Content-Type: application/json" `
  -d '{\"draft\":\"Just shipped our AI tool, guaranteed 10x overnight.\",\"platform\":\"linkedin\"}'
```

## Boundaries (build plan)

B1 owns `app.py`, `config.py`, `requirements.txt`, `.env.example`, this README.
Do **not** edit `backend/analysis/` (B2) or `frontend/` (F1).
