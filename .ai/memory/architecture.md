# Architecture

Still a scaffold — no application code yet. The planned form factor is a Python
web app that calls Anthropic Claude; the web framework is not yet chosen (see
`stack.md`).

## Current layout

- `.ai/` — Atlas AI workspace (config, memory, vocabulary, plans, research,
  decisions, results, skills). `.ai/config.json` is the source of truth for
  artifact locations.
- `AGENTS.md` / `CLAUDE.md` — agent instructions. `CLAUDE.md` imports `AGENTS.md`.
- `.agents/`, `.claude/`, `.cursor/` — generated agent surfaces.

## Unknowns (fill once code lands)

- Web framework (FastAPI vs Streamlit) and the request/response model.
- Module boundaries (UI, Claude calls, content/asset storage).
- Where content and assets live and how they are ingested and processed.
