# Architecture

Planned as a two-tier web app. No application code is scaffolded yet — this
records the intended shape (see `stack.md` for concrete tech).

## Planned shape

- **Frontend** — React (Vite) single-page app. Handles content input/upload and
  renders the AI output. No API keys or Claude calls live here.
- **Backend** — Flask JSON API. Owns all Claude calls via the `anthropic` SDK and
  keeps `ANTHROPIC_API_KEY` server-side.
- Frontend ↔ backend over HTTP/JSON. In dev, Vite proxies API calls to the Flask
  server; use `flask-cors` if cross-origin requests are needed.

## Planned API (MVP)

- `POST /analyze` — body: `{ draft, platform, context? }`. The backend sends a
  single structured Claude call and returns one JSON readiness report:
  `{ risks[], fit{ verdict, dimensions[] }, rewrite }`. See `product.md` for what
  each part means. Stateless; no storage.

## Current layout

- `.ai/` — Atlas AI workspace (config, memory, vocabulary, plans, research,
  decisions, results, skills). `.ai/config.json` is the source of truth for
  artifact locations.
- `AGENTS.md` / `CLAUDE.md` — agent instructions. `CLAUDE.md` imports `AGENTS.md`.
- `.agents/`, `.claude/`, `.cursor/` — generated agent surfaces.

## Unknowns (fill as code lands)

- `backend/` and `frontend/` internal structure and module boundaries.
- Where content/assets are stored and how they are ingested and processed.
- Auth/session needs, if any.
