# services/tts_service.py

from gtts import gTTS
import tempfile
import os

def text_to_speech(text: str, language: str) -> str:
    """
    Convert text to speech using gTTS.
    Returns path to the saved audio file (MP3).
    """

    tts = gTTS(text=text, lang=language)

    # Save to temporary file
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)

    return tmp.name
