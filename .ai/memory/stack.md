# Stack

## Decided

- Backend language/runtime: **Python 3.12**.
- Backend framework: **Flask** — exposes a JSON API and owns all Claude calls.
- Frontend: **React**, scaffolded with **Vite**, JS package manager **npm**.
- AI provider: **Anthropic Claude** via the official Anthropic Python SDK
  (`anthropic`), called only from the Flask backend. Default to the latest Claude
  models. API key is read from `ANTHROPIC_API_KEY` in `.env` (gitignored — never
  commit or print it) and stays server-side (never exposed to the browser).
- Python dependencies: **pip + venv** (`requirements.txt`).
- Atlas (`@blazity-atlas/core`) manages the AI workspace:
  `npx --yes @blazity-atlas/core@latest doctor`.

## Conventions / defaults (open to change)

- Project layout: `backend/` (Flask app, `venv/`, `requirements.txt`) and
  `frontend/` (React + Vite).
- Local dev: Flask dev server + Vite dev server; Vite proxies API calls to Flask.
  Add `flask-cors` if cross-origin requests need it.
- Backend loads secrets with `python-dotenv`.

## Not yet established

- Exact build / test / run commands (fill once the apps are scaffolded).
- Test frameworks (e.g. `pytest` for backend, React testing for frontend).
- Deployment target.

## Notes

- This is a **polyglot** repo: Python backend + Node/React frontend. The Node
  entries in `.gitignore` apply to `frontend/`.
