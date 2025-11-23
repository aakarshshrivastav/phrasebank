# services/translate_service.py

from transformers import MarianTokenizer, MarianMTModel

# Map of (source → target) → corresponding model
MODEL_MAP = {
    ("en", "hi"): "Helsinki-NLP/opus-mt-en-hi",
    ("hi", "en"): "Helsinki-NLP/opus-mt-hi-en",

    ("en", "ta"): "Helsinki-NLP/opus-mt-en-ta",
    ("ta", "en"): "Helsinki-NLP/opus-mt-ta-en",

    ("en", "te"): "Helsinki-NLP/opus-mt-en-te",
    ("te", "en"): "Helsinki-NLP/opus-mt-te-en",

    ("en", "bn"): "Helsinki-NLP/opus-mt-en-bn",
    ("bn", "en"): "Helsinki-NLP/opus-mt-bn-en",

    ("en", "mr"): "Helsinki-NLP/opus-mt-en-mr",
    ("mr", "en"): "Helsinki-NLP/opus-mt-mr-en",

    ("en", "gu"): "Helsinki-NLP/opus-mt-en-gu",
    ("gu", "en"): "Helsinki-NLP/opus-mt-gu-en",

    ("en", "pa"): "Helsinki-NLP/opus-mt-en-pa",
    ("pa", "en"): "Helsinki-NLP/opus-mt-pa-en",
}

# Cache for loaded models so we don't reload on every request
_loaded_models = {}


def load_model(src: str, tgt: str):
    """Load + cache model for a given language pair."""
    key = (src, tgt)

    if key not in MODEL_MAP:
        raise ValueError(f"Translation from {src} → {tgt} is not supported.")

    model_name = MODEL_MAP[key]

    if model_name not in _loaded_models:
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        _loaded_models[model_name] = (tokenizer, model)

    return _loaded_models[model_name]


def translate_text(text: str, source: str, target: str) -> str:
    """
    Translate text using public Helsinki-NLP MarianMT models.
    Works on CPU and with recent transformers versions.
    """
    tokenizer, model = load_model(source, target)

    # Standard, future-proof API:
    encoded = tokenizer([text], return_tensors="pt", padding=True, truncation=True)
    generated = model.generate(**encoded, max_length=256)

    translated = tokenizer.batch_decode(generated, skip_special_tokens=True)[0]
    return translated.strip()


