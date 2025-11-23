"""
Module 3 – Filter / Map Utilities for Voice Translator Project
--------------------------------------------------------------
Provides:
✔ Text list normalization wrapper
✔ Score filtering for dashboards
✔ Sorting utilities for progress stats
✔ Leaderboard string conversion helpers

Optimized for:
- Progress dashboard
- Pronunciation scores
- Analytics
- Phrase search
"""

from typing import List, Dict, Any
from utils.module3_udfs import ensure_text


# ============================================================
# 1. TEXT NORMALIZATION FOR LISTS
# ============================================================

def normalize_list_of_texts(texts: List[str]) -> List[str]:
    """
    Normalize list of text strings using ensure_text + cleanup.
    Example use:
        - Cleaning phrase bank lists
        - Cleaning STT transcripts
        - Preparing lists for scoring
    """
    normalized = []
    for t in texts or []:
        clean = ensure_text(t).lower()
        for p in [".", ",", "!", "?", ":", ";"]:
            clean = clean.replace(p, "")
        normalized.append(" ".join(clean.split()))
    return normalized


# ============================================================
# 2. SCORE FILTERING (For Dashboard)
# ============================================================

def filter_high_scores(records: List[Dict[str, Any]], threshold: int = 80):
    """
    Return only records whose score >= threshold.
    Used in:
        - Leaderboard view
        - Weekly progress screen
    """
    if not records:
        return []
    return [r for r in records if r.get("score", 0) >= threshold]


# ============================================================
# 3. SORTING SCORE RECORDS
# ============================================================

def sort_records_by_score(records: List[Dict[str, Any]], descending: bool = True):
    """
    Sort pronunciation score dictionaries by score.
    Important for:
        - Leaderboard
        - "Recent Attempts" sorted list
    """
    return sorted(records, key=lambda r: r.get("score", 0), reverse=descending)


# ============================================================
# 4. LEADERBOARD STRING CONVERSION
# ============================================================

def map_to_leaderboard(records: List[Dict[str, Any]]) -> List[str]:
    """
    Convert score dictionaries into display strings.
    Example:
        {"user": "Alice", "score": 90}
        → "Alice — 90%"
    """
    output = []
    for r in records:
        user = ensure_text(r.get("user", "?"))
        score = ensure_text(r.get("score", 0))
        output.append(f"{user} — {score}%")
    return output


# ============================================================
# 5. OPTIONAL DEBUG BLOCK (Not used in production)
# ============================================================

if __name__ == "__main__":
    # Quick developer verification block
    sample = [
        {"user": "Alice", "score": 92},
        {"user": "Bob", "score": 67},
        {"user": "Charlie", "score": 84}
    ]

    print("High scores:", filter_high_scores(sample))
    print("Sorted:", sort_records_by_score(sample))
    print("Leaderboard:", map_to_leaderboard(sample))
