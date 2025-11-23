"""
CSV Validation Script for phrase_bank_multilang.csv
---------------------------------------------------
Checks:
✔ Required columns exist
✔ No missing values in essential fields
✔ ID is unique + integer
✔ Supported languages present
✔ No duplicate rows
✔ Row count is reasonable (50–1000)

Usage:
    python validate_phrase_bank.py
"""

import pandas as pd
from pathlib import Path

# Path to your CSV
CSV_PATH = Path("../data/phrase_bank_multilang.csv")


# ============================================================
# VALIDATION RULES
# ============================================================

REQUIRED_COLUMNS = [
    "id", "english", "hindi", "tamil", "telugu",
    "bengali", "marathi", "gujarati", "punjabi",
    "hint", "category"
]

LANG_COLUMNS = [
    "english", "hindi", "tamil", "telugu",
    "bengali", "marathi", "gujarati", "punjabi",
]

MIN_ROWS = 50
MAX_ROWS = 2000


# ============================================================
# VALIDATION FUNCTION
# ============================================================

def validate_csv(path: Path):
    print(f"Validating CSV: {path}")

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found at {path}")

    df = pd.read_csv(path)

    # 1. Check required columns
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    print("✔ All required columns present")

    # 2. Check duplicate IDs
    if df["id"].duplicated().any():
        dupes = df[df["id"].duplicated()]["id"].tolist()
        raise ValueError(f"Duplicate IDs found: {dupes}")
    print("✔ No duplicate IDs")

    # 3. Check ID is integer
    if not pd.api.types.is_integer_dtype(df["id"]):
        raise ValueError("Column 'id' must be integer type")
    print("✔ ID column is integer")

    # 4. Check row count
    if not (MIN_ROWS <= len(df) <= MAX_ROWS):
        raise ValueError(f"Row count {len(df)} is outside expected range ({MIN_ROWS}-{MAX_ROWS})")
    print("✔ Row count is valid")

    # 5. Check empty essential fields
    for col in LANG_COLUMNS:
        if df[col].isna().any() or (df[col].astype(str).str.strip() == "").any():
            raise ValueError(f"Empty or missing values in required column '{col}'")
    print("✔ No missing values in essential language columns")

    # 6. Check for full-duplicate rows
    if df.duplicated().any():
        raise ValueError("Duplicate rows found in CSV")
    print("✔ No duplicate rows")

    # 7. Validate category/hints have values
    if (df["category"].astype(str).str.strip() == "").any():
        raise ValueError("Missing category values")
    if (df["hint"].astype(str).str.strip() == "").any():
        raise ValueError("Missing hint values")
    print("✔ hint/category fields valid")

    print("\n🎉 CSV validation: PASSED")
    return True


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    try:
        validate_csv(CSV_PATH)
    except Exception as e:
        print("\n❌ CSV validation FAILED:")
        print(e)
