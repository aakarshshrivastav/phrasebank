from flask import Blueprint, request, jsonify
from services.stt_service import speech_to_text

stt_bp = Blueprint("stt", __name__)


@stt_bp.route("/stt", methods=["POST"])
def stt():
    """
    Speech-to-Text API
    Expects:
        - audio file (multipart/form-data)
        - language code (optional)

    Returns:
        { "text": "recognized speech" }
    """

    if "audio" not in request.files:
        return jsonify({"error": "Missing audio file"}), 400

    audio_file = request.files["audio"]
    language = request.form.get("language", "en")

    try:
        text = speech_to_text(audio_file, language)
        return jsonify({"text": text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
