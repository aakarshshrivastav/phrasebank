from flask import Blueprint, request, jsonify, send_file
from services.tts_service import text_to_speech
from utils.module2_utils import normalize_text, LANGUAGES
import tempfile
import os

tts_bp = Blueprint("tts", __name__)


@tts_bp.route("/tts", methods=["POST"])
def tts():
    """
    Text-to-Speech API

    Expected JSON:
    {
        "text": "hello",
        "language": "en"
    }

    Returns: Audio file (MP3/WAV) as binary stream
    """

    data = request.json or {}
    text = normalize_text(data.get("text", ""))
    language = data.get("language", "en")

    if not text:
        return jsonify({"error": "Text is required"}), 400

    if language not in LANGUAGES:
        return jsonify({"error": f"Unsupported language: {language}"}), 400

    try:
        # Generate audio using TTS service
        audio_path = text_to_speech(text, language)

        # Send the audio file back to the client
        return send_file(
            audio_path,
            mimetype="audio/mp3",
            as_attachment=False
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Clean temporary file
        if "audio_path" in locals() and os.path.exists(audio_path):
            os.remove(audio_path)
