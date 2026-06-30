# Project Vocabulary

Canonical product and codebase terms for AI agents. Keep entries short; add terms
as the product takes shape.

## Terms

| Term | Meaning | Avoid |
| --- | --- | --- |
| Content | The artifacts the product helps manage — posts, copy, docs, social, newsletters, subtitles, asset libraries. Intentionally broad. | — |
| AI for Content | The hackathon theme: using AI to solve a real content-management pain. | — |
| Claude | The Anthropic model family used as this project's AI provider. | "the AI", "GPT", "the LLM" |
| Anthropic SDK | The official `anthropic` Python package used to call Claude. | "the API wrapper" |
| Atlas | `@blazity-atlas/core`, the tool that manages the `.ai/` AI workspace. | — |
| Readiness report | The full result of analyzing a draft: risk report + platform-fit score + rewrite proposal. | "the analysis" |
| Risk flag | One flagged item in the risk report: span + category + severity + reason + suggested fix. | — |
| Platform-fit score | Per-dimension rubric scoring how well a post fits the chosen platform, plus an overall verdict. | "the score" (alone) |
| Rewrite | The optimized, platform-tuned version of the draft, with changed parts highlighted. | — |
| Draft | The user's input post being analyzed (paste-in for MVP). | — |
