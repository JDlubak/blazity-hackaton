# Build Plan — Post Preflight (3-agent parallel)

**Product:** a web app that answers *"Is this post ready to publish on this
platform?"* The user pastes a draft + picks a platform (+ optional context) and
gets a **readiness report**: 🚦 risk flags, 📊 platform-fit score, ✍️ rewrite.
Full concept in `.ai/memory/product.md`. Stack in `.ai/memory/stack.md`
(Flask API + React/Vite + Anthropic Claude).

## The one rule that makes parallel work safe

The API contract is **FROZEN** in `shared/contract.example.json`. All three agents
build against it and nobody changes its shape without re-syncing the other two.
File ownership is disjoint (below), so branches merge cleanly.

### Contract summary — `POST /api/analyze`
- **Request:** `{ draft: string, platform: enum, context?: { audience?, goal?, brandTone? } }`
- **Response:** `{ platform, risks[], fit{ verdict, overallScore, dimensions[] }, rewrite{ text, summary } }`
- **Errors:** `{ error: string }` with HTTP 400 (bad input) / 500 (analysis failure).
- Enums + a worked example live in `shared/contract.example.json`.
- **Rewrite highlighting** is computed **client-side** (F1 diffs `rewrite.text`
  against the original `draft`). Backend returns plain `rewrite.text` + a
  one-line `rewrite.summary`. Keeps backend/frontend decoupled.

---

## Agents — read your own section; you ARE this agent

### 🟦 B1 — Backend: API & Integration
- **You are** the web-plumbing owner. You make the server run and speak the contract.
- **Own (only these files):** `backend/app.py`, `backend/config.py`,
  `backend/requirements.txt`, `backend/run` instructions, Flask route
  `POST /api/analyze`, request validation, CORS (`flask-cors`), env loading
  (`python-dotenv`), error handling, response assembly.
- **The seam:** call `from analysis import analyze_post` and return its dict as
  JSON. **Ship a stub first** — return `shared/contract.example.json`'s
  `response` so the frontend can integrate on day one. B2 replaces the stub.
- **Do NOT touch:** anything under `backend/analysis/` (B2's), `frontend/` (F1's).
- **requirements.txt must include from the start:** `flask`, `flask-cors`,
  `python-dotenv`, `anthropic` (so B2 needs no new deps).
- **Done when:** `python app.py` serves `POST /api/analyze`, validates input,
  handles errors, and returns contract-shaped JSON (stub, then real via the seam).

### 🟩 B2 — Backend: AI Logic & Prompts  *(this is the agent in THIS session)*
- **You are** the brain. You turn a draft into the readiness report via Claude.
- **Own (only these files):** `backend/analysis/` package — `analyze_post(draft,
  platform, context) -> dict`, the Claude structured-output schema (tool use),
  risk taxonomy + detection prompt, **per-platform rubrics** (LinkedIn, X,
  Facebook, Instagram) + scoring, rewrite generation, prompt tuning, a small
  standalone test script so you can iterate without the Flask layer.
- **Use** the Anthropic Python SDK directly inside `analysis/` (reads
  `ANTHROPIC_API_KEY` from env). Default to the latest Claude model.
- **The seam:** expose exactly `analyze_post(draft, platform, context) -> dict`
  returning the contract `response` shape. That's all B1 depends on.
- **Do NOT touch:** `backend/app.py`/config/requirements (B1's), `frontend/` (F1's).
- **Done when:** `analyze_post` returns real, contract-valid output for all 4
  platforms, with risk flags + per-dimension scores + a platform-tuned rewrite.

### 🟨 F1 — Frontend: UI & UX
- **You are** the interface owner. You make the report understandable and demoable.
- **Own (only these files):** everything under `frontend/` (React + Vite app):
  input form (draft textarea + platform selector + optional context fields), the
  `POST /api/analyze` call, the readiness dashboard (verdict badge, per-dimension
  score bars, risk-flag list with category/severity/reason/suggestion), and a
  **separate rewrite panel** showing `rewrite.text` with changed parts
  highlighted (word-level diff vs the original draft; e.g. `diff` npm lib).
- **Unblock yourself:** develop against `shared/contract.example.json` as a mock
  until B1's endpoint is live; configure Vite to proxy `/api` → `localhost:5000`.
- **Do NOT touch:** anything under `backend/`.
- **Done when:** a user can paste a draft, pick a platform, hit Analyze, and see
  the full report + highlighted rewrite, wired to the real backend.

---

## Sequencing

- **Phase 0 (this commit):** plan + frozen contract committed. Directory skeleton
  is each agent's first task in their own area (no shared scaffolding to collide).
- **Phase 1 (parallel, on branches):**
  - B1 → Flask skeleton + route + stub returning the example response.
  - B2 → real `analyze_post` against the frozen shape (iterate via the test script).
  - F1 → full UI against the mock JSON.
- **Phase 2 (integration):** B1 swaps stub for B2's `analyze_post`; F1 points at
  the live backend; end-to-end smoke test with the example draft.

## Branching & run

- **Work directly on `main`.** File ownership is disjoint (B1 → `backend/app.py`
  + `requirements.txt`, B2 → `backend/analysis/`, F1 → `frontend/`), so conflicts
  are near-zero; and agents sharing one working directory share one HEAD anyway.
  Commit your own area with a clear message. If pushing to a shared remote,
  `git pull --rebase` before pushing (rebases stay clean since paths don't overlap).
- **Backend:** `cd backend && python -m venv venv && venv\Scripts\activate &&
  pip install -r requirements.txt && python app.py` → http://localhost:5000
- **Frontend:** `cd frontend && npm install && npm run dev` → http://localhost:5173

## Open items (refine during build, not blocking)

- Product name (working title: "Post Preflight").
- Exact severity wording and how `verdict` maps from scores + high-severity risks (B2 decides, documents in `analysis/`).
- Target users (solo creators vs marketing teams) — affects copy, not structure.
