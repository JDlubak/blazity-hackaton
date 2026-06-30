"""The analysis seam: analyze_post(draft, platform, context) -> dict.

This is the only symbol B1 (the Flask API agent) depends on. It returns a dict
matching the `response` shape in shared/contract.example.json.
"""

import anthropic

from .platforms import PLATFORMS
from .prompts import SYSTEM_PROMPT, build_user_prompt
from .schema import ReadinessReport

# Most capable model; structured outputs + adaptive thinking are supported on it.
MODEL = "claude-opus-4-8"
MAX_TOKENS = 12000

# Lazily constructed on first use, so importing this package never requires the
# API key to be present yet (env is loaded by the Flask app or the test script
# before the first analyze_post call). Reads ANTHROPIC_API_KEY from the env.
_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client


def analyze_post(draft: str, platform: str, context: dict | None = None) -> dict:
    """Analyze a draft for a target platform and return a readiness report dict.

    Args:
        draft: the post text to analyze.
        platform: one of linkedin | x | facebook | instagram.
        context: optional {audience?, goal?, brandTone?}.

    Returns:
        A dict matching shared/contract.example.json's `response`:
        {platform, risks[], fit{verdict, overallScore, dimensions[]}, rewrite{text, summary}}.

    Raises:
        ValueError: if `draft` is empty or `platform` is unknown.
        RuntimeError: if Claude declines (refusal) or returns no parseable output.
    """
    if not draft or not draft.strip():
        raise ValueError("draft must be a non-empty string.")
    if platform not in PLATFORMS:
        raise ValueError(
            f"Unknown platform {platform!r}. Expected one of: {', '.join(PLATFORMS)}."
        )

    response = _get_client().messages.parse(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        thinking={"type": "adaptive"},
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_user_prompt(draft, platform, context)}],
        output_format=ReadinessReport,
    )

    if response.stop_reason == "refusal":
        raise RuntimeError("The model declined to analyze this draft.")

    report = response.parsed_output
    if report is None:
        raise RuntimeError("The model returned no parseable readiness report.")

    # Inject the authoritative platform from the request, then dump to a plain dict.
    return {"platform": platform, **report.model_dump()}
