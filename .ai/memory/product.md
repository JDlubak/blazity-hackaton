# Product

Blazity Hackathon entry — theme **"AI for Content."** Judged on thinking and
demoability, not volume: a small tool that does one thing well, is explainable,
and shows the AI was aimed at the right problem and its output was checked.

## Concept: pre-publish readiness check for social posts

A web app that answers one question: **"Is this post ready to publish on this
platform?"** The user pastes a draft post, picks a target platform, and
optionally adds context (target audience, goal/CTA, brand tone). The app returns
a readiness report with three parts:

1. **Risk report** — flags potentially controversial or risky content
   (hate/discrimination, sensitive politics/religion, profanity,
   unverifiable/exaggerated claims, legal/compliance, brand-safety). Each flag
   shows the offending span, category, severity, why it is risky, and a suggested
   fix.
2. **Platform-fit score** — a transparent, per-dimension rubric (length/format,
   tone, hook/opening, hashtags/emoji, CTA, readability) instead of a single
   opaque number, plus an overall verdict (ready / needs work / risky).
3. **Rewrite proposal** — an optimized version of the post for the chosen
   platform, shown in a separate panel with the changed parts highlighted
   (e.g. bold/underline).

The whole app is "AI output that is checked and explained" — the angle the
hackathon rewards.

## Scope

- Platforms at launch: **LinkedIn, X/Twitter, Facebook, Instagram** — each with
  its own fit rubric.
- Input mode (MVP): paste an existing draft + optional context. Generation from
  structured ingredients is a possible later extension if time allows.
- Stateless MVP — no persistence needed.

## Decided

- Form factor: web app (see `stack.md` — Flask API + React/Vite, Anthropic
  Claude).

## Open / to refine

- Product name (working title: "Post Preflight").
- Exact risk categories and severity scale wording.
- How the rewrite diff is produced (Claude-marked changes vs client-side diff).
- Target users (solo creators vs social/marketing teams) — to confirm.
