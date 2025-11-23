from flask import Blueprint, request, jsonify
from utils.module2_utils import normalize_text
from services.scoring_service import compute_pronunciation_score

score_bp = Blueprint("score", __name__)


@score_bp.route("/score", methods=["POST"])
def score():
    """
    Pronunciation Scoring API

    Expected JSON:
    {
        "reference_text": "good morning",
        "user_text": "good mornin"
    }

    OR (in practice mode)
    {
        "reference_text": "hello",
        "user_audio": <binary>  # then STT runs inside scoring service
    }

    Returns:
    {
        "score": 84,
        "similarity": 0.84,
        "feedback": "Good pronunciation."
    }
    """

    data = request.json or {}

    reference = normalize_text(data.get("reference_text", ""))
    user_text = data.get("user_text")
    user_audio = data.get("user_audio")  # optional base64 string (if implemented)

    # Validation
    if not reference:
        return jsonify({"error": "reference_text is required"}), 400

    if not user_text and not user_audio:
        return jsonify({"error": "Provide either user_text or user_audio"}), 400

    try:
        # If audio is given, scoring service will run STT internally
        result = compute_pronunciation_score(
            reference=reference,
            user_text=user_text,
            user_audio=user_audio
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
