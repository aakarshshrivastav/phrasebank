# services/scoring_service.py

from utils.module2_utils import normalize_text
from utils.module3_udfs import simple_similarity


def compute_pronunciation_score(reference: str, user_text: str = None, user_audio=None):
    """
    Compute pronunciation score:
    - If user_audio is given → (OPTIONAL) run STT here
    - Then compare reference text with user_text

    Returns:
    {
        "score": int,
        "similarity": float,
        "feedback": str
    }
    """

    # (Optional) If user_audio is provided, integrate STT here
    # user_text = whisper_transcribe(user_audio)

    reference = normalize_text(reference)
    user_text = normalize_text(user_text)

    similarity = simple_similarity(reference, user_text)
    score = int(similarity * 100)

    # Generate user feedback
    if score > 85:
        feedback = "Excellent pronunciation!"
    elif score > 70:
        feedback = "Good pronunciation."
    elif score > 50:
        feedback = "Average, needs improvement."
    else:
        feedback = "Poor pronunciation. Practice more."

    return {
        "score": score,
        "similarity": round(similarity, 3),
        "feedback": feedback
    }
