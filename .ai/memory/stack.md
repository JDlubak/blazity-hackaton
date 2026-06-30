# Stack

## Decided

- Language: **Python**.
- AI provider: **Anthropic Claude** via the official Anthropic Python SDK
  (`anthropic`). Default to the latest Claude models. The API key is read from
  `ANTHROPIC_API_KEY` in `.env` (gitignored — never commit or print it).
- Atlas (`@blazity-atlas/core`) manages the AI workspace:
  `npx --yes @blazity-atlas/core@latest doctor`.

## Not yet locked

- Web framework: **FastAPI or Streamlit** — confirm before assuming.
- Build / test / run commands — none exist yet; record them here once
  established.
- Dependency manager (pip / uv / poetry) and target Python version.

## Notes

- No `package.json` or lockfile exists; this is a Python project, not Node. The
  Node-related entries in `.gitignore` are generic scaffolding leftovers.
