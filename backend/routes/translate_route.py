from flask import Blueprint, request, jsonify
from utils.module2_utils import LANGUAGES, normalize_text
from services.translate_service import translate_text

translate_bp = Blueprint("translate", __name__)


@translate_bp.route("/translate", methods=["POST"])
def translate():
    """
    Text Translation API

    Expected JSON:
    {
        "text": "hello",
        "source": "en",
        "target": "hi"
    }

    Returns:
    {
        "translated_text": "नमस्ते"
    }
    """

    data = request.json or {}
    
    text = normalize_text(data.get("text", ""))
    source = data.get("source")
    target = data.get("target")

    # Validate input
    if not text:
        return jsonify({"error": "Text is required"}), 400

    if source not in LANGUAGES:
        return jsonify({"error": f"Invalid source language: {source}"}), 400

    if target not in LANGUAGES:
        return jsonify({"error": f"Invalid target language: {target}"}), 400

    try:
        translated = translate_text(text, source, target)
        return jsonify({"translated_text": translated})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
