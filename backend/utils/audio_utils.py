"""
Audio Utilities for Voice Translator Backend
--------------------------------------------
Provides:
✔ Safe saving of uploaded audio files
✔ Standardizing audio sample rate for STT models
✔ WAV/MP3 conversion helpers
✔ Base64 encode/decode for audio transport
✔ Temporary file creation

Used by:
- stt_service.py
- scoring_service.py
- tts_service.py
"""

import tempfile
import base64
import os
from pydub import AudioSegment


# ============================================================
# 1. SAVE UPLOADED AUDIO TO TEMP FILE
# ============================================================

def save_uploaded_audio(uploaded_audio) -> str:
    """
    Saves a Flask `FileStorage` audio upload to a temporary file.
    Returns the file path.
    """
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    uploaded_audio.save(tmp.name)
    return tmp.name


# ============================================================
# 2. CONVERT AUDIO TO WAV (WHISPER-FRIENDLY)
# ============================================================

def convert_to_wav(input_path: str) -> str:
    """
    Convert any audio file (mp3/m4a/wav) to WAV format.
    Required for STT models like Whisper/Vosk.
    Returns path to converted .wav file.
    """

    output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name

    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)  # STT-friendly format
    audio.export(output_path, format="wav")

    return output_path


# ============================================================
# 3. CONVERT WAV → MP3 (for sending TTS results)
# ============================================================

def convert_wav_to_mp3(wav_path: str) -> str:
    """
    Converts WAV audio to MP3.
    Used by TTS to ensure small file size.
    """
    output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name

    audio = AudioSegment.from_wav(wav_path)
    audio.export(output_path, format="mp3")

    return output_path


# ============================================================
# 4. BASE64 HELPERS (OPTIONAL)
# ============================================================

def audio_to_base64(path: str) -> str:
    """
    Read an audio file and return base64 encoded string.
    Useful if front-end sends audio via JSON instead of multipart/form-data.
    """
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode("utf-8")


def base64_to_audio(b64: str) -> str:
    """
    Convert base64 audio string into a temporary WAV file.
    """
    audio_bytes = base64.b64decode(b64)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    with open(tmp.name, "wb") as f:
        f.write(audio_bytes)
    return tmp.name


# ============================================================
# 5. CLEANUP HELPERS
# ============================================================

def delete_file(path: str):
    """Safely delete a file if it exists."""
    if path and os.path.exists(path):
        os.remove(path)


# ============================================================
# DEBUG / DEV TESTS (Not used in production)
# ============================================================

if __name__ == "__main__":
    print("Audio utils loaded successfully.")
