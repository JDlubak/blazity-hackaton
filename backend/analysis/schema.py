"""Pydantic models for the readiness report — the structured output Claude returns.

Field names mirror the FROZEN contract in ``shared/contract.example.json`` exactly
(including the camelCase ``overallScore``) so ``model_dump()`` produces a dict that
matches what B1's ``/api/analyze`` route and F1's frontend expect. The ``platform``
field is intentionally absent here — ``analyze_post`` injects it from the request,
so Claude can never echo back a mismatched platform.
"""

from typing import Literal

from pydantic import BaseModel, Field

# Enums — must match shared/contract.example.json "_enums".
RiskCategory = Literal[
    "hate_discrimination",
    "sensitive_politics_religion",
    "profanity",
    "unverifiable_claim",
    "legal_compliance",
    "brand_safety",
]
Severity = Literal["low", "medium", "high"]
Verdict = Literal["ready", "needs_work", "risky"]
DimensionKey = Literal["length", "tone", "hook", "hashtags_emoji", "cta", "readability"]


class Risk(BaseModel):
    span: str = Field(description="The exact substring copied verbatim from the draft that is risky.")
    category: RiskCategory = Field(description="Which kind of risk this is.")
    severity: Severity = Field(description="How damaging this would be if published.")
    reason: str = Field(description="One sentence: why this is risky on this platform/audience.")
    suggestion: str = Field(description="A concrete, actionable fix.")


class Dimension(BaseModel):
    key: DimensionKey = Field(description="Which fit dimension this scores.")
    label: str = Field(description="Human-readable name of the dimension, e.g. 'Length & format'.")
    score: int = Field(description="0-100 score for how well the draft does on this dimension for this platform.")
    comment: str = Field(description="One sentence on what is good or weak here.")
    suggestion: str = Field(description="A concrete improvement for this dimension.")


class Fit(BaseModel):
    verdict: Verdict = Field(description="Overall publish-readiness verdict.")
    overallScore: int = Field(description="0-100 overall platform-fit score.")
    dimensions: list[Dimension] = Field(
        description="One entry per fit dimension: length, tone, hook, hashtags_emoji, cta, readability.",
    )


class Rewrite(BaseModel):
    text: str = Field(description="The optimized post, tuned for the chosen platform and free of the flagged risks.")
    summary: str = Field(description="One sentence summarizing what was changed and why.")


class ReadinessReport(BaseModel):
    """Top-level structured output. ``platform`` is added by ``analyze_post``, not Claude."""

    risks: list[Risk] = Field(description="Every risky span found; empty list if the draft is clean.")
    fit: Fit
    rewrite: Rewrite
