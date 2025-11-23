# services/stt_service.py

import whisper
import tempfile
import os

# Load model once
model = whisper.load_model("base")


def speech_to_text(audio_file, language="en"):
    """
    Convert uploaded audio file into text using Whisper.
    """
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        audio_file.save(tmp.name)
        temp_path = tmp.name

    try:
        result = model.transcribe(temp_path, language=language)
        text = result.get("text", "").strip()
        return text

    finally:
        os.remove(temp_path)
