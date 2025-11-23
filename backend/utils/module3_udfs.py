"""
Module 3 – Advanced Utility Functions for Voice Translator Project
------------------------------------------------------------------
Provides:
✔ Safe dictionary access
✔ Safe text conversion
✔ Chunking utilities (batch processing)
✔ Dynamic language list builder
✔ Text similarity scoring (for pronunciation module)
✔ Retry decorator (for unstable API calls — STT, TTS, Translate)

This file is clean, optimized, and used by:
- scoring_service.py
- translate_route.py
- stt_service.py (if cloud APIs are used)
- background/retry operations
"""

from typing import List, Dict, Any, Generator, Callable
import time


# ============================================================
# 1. SAFE ACCESS HELPERS
# ============================================================

def safe_get(d: Dict[str, Any], key: str, default=None):
    """
    Safe dictionary access. Avoids KeyErrors and handles None.
    """
    if d is None:
        return default
    return d.get(key, default)


def ensure_text(value: Any) -> str:
    """
    Convert any value (None, int, float, list) to a clean string.
    Prevents crashes when processing inconsistent data.
    """
    if value is None:
        return ""
    return str(value).strip()


# ============================================================
# 2. LANGUAGE LIST BUILDER
# ============================================================

def build_lang_list(lang_map: Dict[str, Dict[str, str]]) -> List[str]:
    """
    Given the LANGUAGES map from module2_utils,
    return a sorted list of language keys.
    
    Example:
        build_lang_list({"en": {...}, "hi": {...}})
        → ["en", "hi"]
    """
    if not lang_map:
        return []
    return sorted(list(lang_map.keys()))


# ============================================================
# 3. LIST CHUNKING UTILITIES
# ============================================================

def chunk_list(items: List[Any], chunk_size: int) -> Generator[List[Any], None, None]:
    """
    Yield successive chunk lists from a list.
    Useful for batching:
    - Large translation tasks
    - Audio segmentation
    - Long phrase banks
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")

    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]


# ============================================================
# 4. TEXT SIMILARITY (FOR PRONUNCIATION SCORING)
# ============================================================

def simple_similarity(a: str, b: str) -> float:
    """
    Compute a lightweight similarity score between 2 strings (0–1).
    Used in:
    - Pronunciation scoring
    - Feedback calculation

    Logic:
    Matches characters in aligned positions:
        "hello" vs "helxo" → 0.8
    """

    a = ensure_text(a).lower()
    b = ensure_text(b).lower()

    # Edge cases
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0

    matches = sum(1 for x, y in zip(a, b) if x == y)
    return matches / max(len(a), len(b))


# ============================================================
# 5. RETRY DECORATOR (CRITICAL FOR API STABILITY)
# ============================================================

def retry(times: int = 3, delay: float = 1.0):
    """
    Decorator to retry a function multiple times.
    Extremely useful for:
    - Cloud-based STT calls (rate limits)
    - Translation APIs that timeout
    - TTS services (network instability)

    Example:
        @retry(times=3, delay=2)
        def call_translate():
            ...
    """

    def decorator(fn: Callable):
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    print(f"[WARN] Attempt {attempt}/{times} failed: {e}")
                    if attempt < times:
                        time.sleep(delay)
            raise RuntimeError(f"Function failed after {times} retries.")
        return wrapper

    return decorator


# ============================================================
# TEST BLOCK FOR DEVELOPMENT (NOT USED IN PRODUCTION)
# ============================================================

if __name__ == "__main__":
    # Manual developer checks
    print("Similarity test:", simple_similarity("hello", "helo"))
    print("Chunk test:", list(chunk_list([1, 2, 3, 4, 5], 2)))
    print("Lang list:", build_lang_list({"en": {}, "hi": {}, "ta": {}}))
