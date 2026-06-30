"""Per-platform rubrics.

Each entry guides Claude on what "fits" a given platform across the six scoring
dimensions. Keep these concrete and contrasting — the differences between
platforms are what make the platform-fit score meaningful rather than generic.
"""

# Keys must match the `platform` enum in shared/contract.example.json.
PLATFORMS: dict[str, dict[str, str]] = {
    "linkedin": {
        "name": "LinkedIn",
        "rubric": (
            "Audience: professionals, B2B, recruiters. "
            "Length: medium-to-long works well (roughly 900-1800 characters); reward structure with short paragraphs and line breaks. "
            "Tone: credible, insightful, lightly personal; punish hype, hard-sell, and clickbait. "
            "Hook: the first 1-2 lines must earn the 'see more' click — lead with a result, insight, or tension. "
            "Hashtags & emoji: 3-5 relevant hashtags is ideal; emoji sparingly (0-3). "
            "CTA: invite discussion (a question, 'what's your take') or a single clear link; avoid 'DM me'. "
            "Readability: short skimmable lines beat dense blocks."
        ),
    },
    "x": {
        "name": "X / Twitter",
        "rubric": (
            "Audience: fast-scrolling, broad, opinionated. "
            "Length: a single post should fit ~280 characters; if the draft is much longer, it should be a thread or be tightened. "
            "Tone: punchy, direct, a strong point of view; padding and corporate-speak die here. "
            "Hook: the first line is everything — it must stop the scroll in the first few words. "
            "Hashtags & emoji: 0-2 hashtags max (more reads as spam); emoji optional and light. "
            "CTA: a sharp question, a hot take to reply to, or one link; keep friction minimal. "
            "Readability: terse, one idea per post."
        ),
    },
    "facebook": {
        "name": "Facebook",
        "rubric": (
            "Audience: broad, community- and friends-driven, mixed ages. "
            "Length: short-to-medium (roughly 100-500 characters) tends to outperform; very long posts lose people. "
            "Tone: warm, conversational, relatable; overly polished or salesy copy underperforms. "
            "Hook: open with something human or relatable that invites a reaction. "
            "Hashtags & emoji: hashtags add little (0-2); emoji are welcome and boost warmth. "
            "CTA: encourage comments, shares, or tagging a friend; a link is fine. "
            "Readability: friendly and easy, written like you talk."
        ),
    },
    "instagram": {
        "name": "Instagram",
        "rubric": (
            "Audience: visual-first, casual, younger-skewing. "
            "Length: caption supports a visual — a strong first line plus short body; can be longer if storytelling. "
            "Tone: casual, authentic, energetic; corporate tone feels out of place. "
            "Hook: the first line (before 'more') must grab — captions are read after the image hooks. "
            "Hashtags & emoji: hashtags matter for reach (5-15, often grouped at the end); emoji are expected and on-brand. "
            "CTA: 'save this', 'share to your story', 'tell us in the comments', or 'link in bio'. "
            "Readability: short lines, emoji as visual punctuation."
        ),
    },
}


def platform_rubric(platform: str) -> str:
    """Return the rubric text for a platform, or raise if unknown."""
    entry = PLATFORMS.get(platform)
    if entry is None:
        raise ValueError(
            f"Unknown platform {platform!r}. Expected one of: {', '.join(PLATFORMS)}."
        )
    return f"{entry['name']} rubric:\n{entry['rubric']}"


def platform_display_name(platform: str) -> str:
    entry = PLATFORMS.get(platform)
    return entry["name"] if entry else platform
