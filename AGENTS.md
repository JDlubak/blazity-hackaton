# Project AI Instructions

## What this repo is

`blazity-hackaton` — a Blazity Hackathon entry, theme **"AI for Content."** The
goal is a **web app that uses AI to solve a real content-management pain**
(reformatting, brand/tone consistency, asset search, summarization, etc.). Today
the repo is still a scaffold: only README, LICENSE, and the Atlas AI workspace
under `.ai/` exist; no application code yet. Stack is a Flask (Python) JSON API +
React/Vite frontend with Anthropic Claude; the concrete use case is still open.
See `.ai/memory/` for stable context.

## Structure

- `.ai/` — Atlas AI workspace. `.ai/config.json` is the source of truth for
  artifact locations (memory, vocabulary, plans, research, decisions, results).
- `AGENTS.md` / `CLAUDE.md` — agent instructions; `CLAUDE.md` imports this file.
- `.agents/`, `.claude/`, `.cursor/` — generated agent surfaces.

## Working rules

- Stack: **Flask** (Python 3.12) JSON API backend + **React/Vite** frontend; AI
  via **Anthropic Claude** (`anthropic` SDK, latest models). The backend owns all
  Claude calls and the API key. Python deps via **pip + venv**; frontend via
  **npm**. Details in `.ai/memory/stack.md`.
- The Anthropic key lives in `.env` as `ANTHROPIC_API_KEY` (gitignored — never
  commit it or print its value) and must stay server-side, never in the browser.
- No build/test/run commands exist yet (nothing scaffolded). Atlas health check
  is the only safe command: `npx --yes @blazity-atlas/core@latest doctor`.
- Windows: the `.claude/.cursor/.agents` `skills` symlinks need Administrator or
  Developer Mode to create (see `.ai/memory/lessons.md`).
- Do not edit the `<!-- BEGIN/END ATLAS -->` managed block below by hand.
- Keep durable docs depersonalized (see Atlas Documentation Rules below).

<!-- BEGIN ATLAS: artifact-paths -->
## Atlas Artifact Paths

`.ai/config.json` is the source of truth for AI artifact locations in this repository.
Before writing plans, research, decisions, ADRs, results, memory, vocabulary, or skill outputs, resolve the destination through `artifactRoot`, `paths`, and `pathAliases`.
If an imported skill, template, or instruction mentions a different path, map it through `.ai/config.json` before reading or writing files.
Do not create new documentation roots unless `.ai/config.json` explicitly allows them.

## Atlas Documentation Rules

Durable documentation records needs, decisions, and reasons — never individuals or internal process.
Write "memory was needed to persist context across runs", not "<name> wanted memory".
Keep personal names, private schedules, internal-only references, and absolute local paths out of workspace artifacts.
<!-- END ATLAS: artifact-paths -->
