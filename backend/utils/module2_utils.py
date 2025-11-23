"""
Module 2 – Core Utilities for the Voice Translator Project
-----------------------------------------------------------
Provides:
✔ Supported language map
✔ Phrase bank CSV loader (multilingual)
✔ Text normalization utilities
✔ Phrase filtering & slicing helpers
✔ Safe dictionary access

This module is clean, production-ready, and used across the backend.
"""

from pathlib import Path
import csv
from typing import Dict, List, Any

# ============================================================
# 1. SUPPORTED LANGUAGES
# ============================================================

LANGUAGES: Dict[str, Dict[str, str]] = {
    "en": {"name": "English", "code": "en-IN", "flag": "🇬🇧"},
    "hi": {"name": "Hindi", "code": "hi-IN", "flag": "🇮🇳"},
    "ta": {"name": "Tamil", "code": "ta-IN", "flag": "🇮🇳"},
    "te": {"name": "Telugu", "code": "te-IN", "flag": "🇮🇳"},
    "mr": {"name": "Marathi", "code": "mr-IN", "flag": "🇮🇳"},
    "bn": {"name": "Bengali", "code": "bn-IN", "flag": "🇮🇳"},
    "gu": {"name": "Gujarati", "code": "gu-IN", "flag": "🇮🇳"},
    "kn": {"name": "Kannada", "code": "kn-IN", "flag": "🇮🇳"},
    "ml": {"name": "Malayalam", "code": "ml-IN", "flag": "🇮🇳"},
    "pa": {"name": "Punjabi", "code": "pa-IN", "flag": "🇮🇳"},
}


def get_supported_language_keys() -> List[str]:
    """Return alphabetically sorted list of supported language keys."""
    return sorted(list(LANGUAGES.keys()))

# ============================================================
# 2. TEXT NORMALIZATION UTILITIES
# ============================================================

def normalize_text(s: str) -> str:
    """
    Normalize text:
    - Lowercase
    - Trim spaces
    - Remove punctuation
    - Collapse multiple spaces
    """
    if not s:
        return ""

    s = s.lower().strip()
    for p in [".", ",", "!", "?", ":", ";"]:
        s = s.replace(p, "")

    return " ".join(s.split())


def normalize_list(texts: List[str]) -> List[str]:
    """Normalize a list of strings."""
    return [normalize_text(t) for t in texts if t]

# ============================================================
# 3. PHRASE BANK (CSV LOADING)
# ============================================================

PHRASE_CSV_LOCATIONS = [
    Path("data/phrase_bank_multilang.csv"),
    Path("backend/data/phrase_bank_multilang.csv"),  # fallback for dev
]


def find_phrase_csv() -> Path:
    """Locate phrase bank CSV in the known directories."""
    for p in PHRASE_CSV_LOCATIONS:
        if p.exists():
            return p
    raise FileNotFoundError("phrase_bank_multilang.csv not found.")


def load_phrase_bank() -> List[Dict[str, Any]]:
    """
    Load multilingual phrases from CSV.
    Returns list of dictionaries (one per row).
    """
    path = find_phrase_csv()
    rows: List[Dict[str, Any]] = []

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cleaned = {k: (v or "").strip() for k, v in row.items()}
            rows.append(cleaned)

    return rows

# ============================================================
# 4. PHRASE HELPERS
# ============================================================

def filter_phrases_by_keyword(phrases: List[Dict[str, Any]], keyword: str) -> List[Dict[str, Any]]:
    """Return phrases whose English text contains the given keyword."""
    keyword = keyword.lower()
    return [p for p in phrases if keyword in p.get("english", "").lower()]


def top_n_phrases(phrases: List[Dict[str, Any]], n: int = 5) -> List[Dict[str, Any]]:
    """Return first N phrases (safe for short lists)."""
    return phrases[:n]


def get_all_english_phrases(phrases: List[Dict[str, Any]]) -> List[str]:
    """Extract all English phrases from phrase bank."""
    return [p.get("english", "") for p in phrases]


# ============================================================
# 5. SAFE GETTER
# ============================================================

def safe_get(d: Dict[str, Any], key: str, default="") -> str:
    """Safe dictionary access."""
    if d is None:
        return default
    return str(d.get(key, default)).strip()
