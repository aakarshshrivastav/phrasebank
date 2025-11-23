from flask import Blueprint, request, jsonify
from datetime import datetime
import csv
from pathlib import Path

log_bp = Blueprint("log", __name__)

# Log file location
LOG_FILE = Path("data/logs.csv")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


def write_log_entry(entry: dict):
    """Append a log entry to logs.csv."""
    
    # If file doesn't exist, create header
    file_exists = LOG_FILE.exists()

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "timestamp",
                "phrase_id",
                "reference_text",
                "user_text",
                "score",
                "duration",
                "language"
            ]
        )
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)


@log_bp.route("/log", methods=["POST"])
def log_event():
    """
    Log API for storing user practice and scoring events.

    Expected JSON:
    {
        "phrase_id": "12",
        "reference_text": "good morning",
        "user_text": "good mornin",
        "score": 85,
        "duration": 4.2,
        "language": "en"
    }

    Returns:
    { "status": "saved" }
    """

    data = request.json or {}

    entry = {
        "timestamp": datetime.now().isoformat(),
        "phrase_id": data.get("phrase_id", ""),
        "reference_text": data.get("reference_text", ""),
        "user_text": data.get("user_text", ""),
        "score": data.get("score", ""),
        "duration": data.get("duration", ""),
        "language": data.get("language", "")
    }

    try:
        write_log_entry(entry)
        return jsonify({"status": "saved"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
