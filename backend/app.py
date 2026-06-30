"""Post Preflight — Flask API (B1: API & Integration).

Owns the web plumbing: the single `POST /api/analyze` route, request validation,
CORS, error handling, and response assembly. The actual analysis is B2's job,
reached through one seam: `analyze_post(draft, platform, context) -> dict`.

Phase 1 ships a STUB that returns the frozen contract's example response so the
frontend (F1) can integrate on day one. Phase 2 flips USE_STUB off (or simply
removes the fallback) once B2's `backend/analysis/` package is in place.
"""

import json
import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from config import Config

# --- Frozen contract -------------------------------------------------------
# Single source of truth shared by B1/B2/F1. We load it for the stub response
# and to derive the platform enum, so the API and the contract never drift.
_CONTRACT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "shared", "contract.example.json"
)
with open(_CONTRACT_PATH, encoding="utf-8") as fh:
    _CONTRACT = json.load(fh)

VALID_PLATFORMS = set(_CONTRACT["_enums"]["platform"])
_STUB_RESPONSE = _CONTRACT["response"]

# Flip to False in Phase 2 once backend/analysis/ exists. Kept as a stub by
# default so `python app.py` works before B2's package lands.
USE_STUB = os.getenv("USE_STUB", "1") == "1"


# --- The seam to B2 --------------------------------------------------------
def run_analysis(draft: str, platform: str, context: dict | None) -> dict:
    """Return a contract-shaped readiness report.

    Phase 2: delegates to B2's `analyze_post`. Phase 1: returns the frozen
    example response (with the requested platform echoed back) so the contract
    is exercised end-to-end before the AI logic exists.
    """
    if not USE_STUB:
        from analysis import analyze_post  # imported lazily — B2 owns this module

        return analyze_post(draft, platform, context)

    stub = json.loads(json.dumps(_STUB_RESPONSE))  # deep copy so we don't mutate
    stub["platform"] = platform
    return stub


# --- Request validation ----------------------------------------------------
class BadRequest(Exception):
    """Raised for client input problems; mapped to HTTP 400."""


def validate_payload(payload) -> tuple[str, str, dict | None]:
    if not isinstance(payload, dict):
        raise BadRequest("Request body must be a JSON object.")

    draft = payload.get("draft")
    if not isinstance(draft, str) or not draft.strip():
        raise BadRequest("'draft' is required and must be a non-empty string.")
    if len(draft) > Config.MAX_DRAFT_CHARS:
        raise BadRequest(
            f"'draft' exceeds the {Config.MAX_DRAFT_CHARS}-character limit."
        )

    platform = payload.get("platform")
    if platform not in VALID_PLATFORMS:
        allowed = ", ".join(sorted(VALID_PLATFORMS))
        raise BadRequest(f"'platform' must be one of: {allowed}.")

    context = payload.get("context")
    if context is not None:
        if not isinstance(context, dict):
            raise BadRequest("'context' must be an object when provided.")
        for field in ("audience", "goal", "brandTone"):
            value = context.get(field)
            if value is not None and not isinstance(value, str):
                raise BadRequest(f"'context.{field}' must be a string when provided.")

    return draft, platform, context


# --- App factory -----------------------------------------------------------
def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": Config.CORS_ORIGINS}})

    @app.get("/api/health")
    def health():
        return jsonify(
            {
                "status": "ok",
                "mode": "stub" if USE_STUB else "live",
                "hasApiKey": Config.has_api_key(),
                "platforms": sorted(VALID_PLATFORMS),
            }
        )

    @app.post("/api/analyze")
    def analyze():
        payload = request.get_json(silent=True)
        try:
            draft, platform, context = validate_payload(payload)
        except BadRequest as exc:
            return jsonify({"error": str(exc)}), 400

        try:
            report = run_analysis(draft, platform, context)
        except Exception as exc:  # noqa: BLE001 — surface any analysis failure as 500
            app.logger.exception("analysis failed")
            return jsonify({"error": f"Analysis failed: {exc}"}), 500

        return jsonify(report)

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"error": "Not found."}), 404

    @app.errorhandler(405)
    def method_not_allowed(_):
        return jsonify({"error": "Method not allowed."}), 405

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
