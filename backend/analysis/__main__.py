"""Standalone test for the analysis seam — no Flask required.

Run from the backend/ directory:

    python -m analysis                 # uses the built-in sample draft
    python -m analysis linkedin        # same sample, explicit platform
    python -m analysis x "my draft"    # custom platform + draft

Loads ANTHROPIC_API_KEY from the repo-root .env, calls analyze_post, prints the
JSON, and structurally checks it against the frozen contract.
"""

import json
import sys

# Print emoji/Unicode safely even on a legacy Windows code page (cp1250).
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())  # must run before analyze_post constructs the client

from analysis import analyze_post  # noqa: E402  (after dotenv load)
from analysis.platforms import PLATFORMS  # noqa: E402

SAMPLE_DRAFT = (
    "Just shipped our new AI tool. It's literally the best thing ever and will "
    "10x your output overnight, guaranteed. DM me."
)
SAMPLE_CONTEXT = {
    "audience": "B2B SaaS founders",
    "goal": "drive demo signups",
    "brandTone": "confident but credible",
}

EXPECTED_DIMENSIONS = {"length", "tone", "hook", "hashtags_emoji", "cta", "readability"}


def _check_contract(report: dict) -> list[str]:
    """Light structural validation against shared/contract.example.json. Returns problems."""
    problems: list[str] = []
    for key in ("platform", "risks", "fit", "rewrite"):
        if key not in report:
            problems.append(f"missing top-level key: {key}")
    fit = report.get("fit", {})
    for key in ("verdict", "overallScore", "dimensions"):
        if key not in fit:
            problems.append(f"missing fit.{key}")
    if fit.get("verdict") not in {"ready", "needs_work", "risky"}:
        problems.append(f"bad verdict: {fit.get('verdict')!r}")
    dims = {d.get("key") for d in fit.get("dimensions", [])}
    missing_dims = EXPECTED_DIMENSIONS - dims
    if missing_dims:
        problems.append(f"missing dimensions: {sorted(missing_dims)}")
    for key in ("text", "summary"):
        if key not in report.get("rewrite", {}):
            problems.append(f"missing rewrite.{key}")
    return problems


def main() -> int:
    platform = sys.argv[1] if len(sys.argv) > 1 else "linkedin"
    draft = sys.argv[2] if len(sys.argv) > 2 else SAMPLE_DRAFT
    context = SAMPLE_CONTEXT if draft == SAMPLE_DRAFT else None

    if platform not in PLATFORMS:
        print(f"Unknown platform {platform!r}. Choose from: {', '.join(PLATFORMS)}")
        return 2

    print(f"Analyzing for platform: {platform}\n{'=' * 60}")
    report = analyze_post(draft, platform, context)
    print(json.dumps(report, indent=2, ensure_ascii=False))

    problems = _check_contract(report)
    print("\n" + "=" * 60)
    if problems:
        print("CONTRACT CHECK: FAILED")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(
        f"CONTRACT CHECK: OK  "
        f"(verdict={report['fit']['verdict']}, "
        f"overallScore={report['fit']['overallScore']}, "
        f"risks={len(report['risks'])})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
