"""Configuration for the Post Preflight backend (B1 — API & Integration).

Loads environment from a local .env (gitignored) and exposes typed settings.
The Anthropic key stays server-side and is read by B2's analysis package; B1
only checks that it exists so failures are clear, not mysterious mid-request.
"""

import os

from dotenv import load_dotenv

load_dotenv()  # reads backend/.env if present; no-op when the file is absent


class Config:
    # --- Anthropic (used by backend/analysis/, never sent to the browser) ---
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

    # --- HTTP server ---
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", "5000"))
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"

    # --- CORS: the Vite dev server origin(s) allowed to call /api/* ---
    CORS_ORIGINS = [
        o.strip()
        for o in os.getenv(
            "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
        ).split(",")
        if o.strip()
    ]

    # --- Input guards ---
    MAX_DRAFT_CHARS = int(os.getenv("MAX_DRAFT_CHARS", "10000"))

    @classmethod
    def has_api_key(cls) -> bool:
        return bool(cls.ANTHROPIC_API_KEY)
