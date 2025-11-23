from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# NLLB model
model_name = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Map simple language codes to NLLB language tags
LANG_MAP = {
    "en": "eng_Latn",
    "hi": "hin_Deva",
    "ta": "tam_Taml",
    "te": "tel_Telu",
    "bn": "ben_Beng",
    "mr": "mar_Deva",
    "gu": "guj_Gujr",
    "pa": "pan_Guru",
}


def _get_lang_id(lang_code: str) -> int:
    """
    Get the token id for a language code like 'hin_Deva' without relying on
    tokenizer.lang_code_to_id (which is missing in older transformers).
    """
    # If your tokenizer DOES have lang_code_to_id, use it
    if hasattr(tokenizer, "lang_code_to_id"):
        return tokenizer.lang_code_to_id[lang_code]

    # Fallback: convert the language code token to id directly
    return tokenizer.convert_tokens_to_ids(lang_code)


def translate_text(text: str, source: str, target: str) -> str:
    # Resolve language tags, with safe defaults
    src = LANG_MAP.get(source, "eng_Latn")
    tgt = LANG_MAP.get(target, "hin_Deva")

    # Tell tokenizer what the source language is
    tokenizer.src_lang = src

    # Tokenize
    inputs = tokenizer(text, return_tensors="pt")

    # Generate, forcing BOS to the target language id
    forced_bos_id = _get_lang_id(tgt)
    output = model.generate(
        **inputs,
        forced_bos_token_id=forced_bos_id,
        max_length=128,
    )

    translated = tokenizer.batch_decode(output, skip_special_tokens=True)[0].strip()

    # Custom rule: "hi sir" → "नमस्ते सर" (instead of "हाय सर")
    if source == "en" and target == "hi":
        if text.strip().lower().startswith("hi sir"):
            translated = "नमस्ते सर"
    if source == "en" and target == "hi":
        if text.strip().lower().startswith("hi mam"):
            translated = "नमस्ते मैडम"

    return translated
