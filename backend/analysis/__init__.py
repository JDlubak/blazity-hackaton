"""Post Preflight analysis package (agent B2).

Public API — the seam B1's Flask route imports:

    from analysis import analyze_post
"""

from .core import analyze_post

__all__ = ["analyze_post"]
