from flask import Blueprint, jsonify, request
from utils.module2_utils import (
    load_phrase_bank,
    filter_phrases_by_keyword,
    top_n_phrases
)

phrases_bp = Blueprint("phrases", __name__)


@phrases_bp.route("/phrases", methods=["GET"])
def get_phrases():
    """
    Phrase Bank API
    Supports:
        /phrases
        /phrases?limit=10
        /phrases?keyword=hello
        /phrases?keyword=greet&limit=5

    Returns:
    {
        "phrases": [ ... ]
    }
    """

    # Load full phrase bank from CSV
    phrases = load_phrase_bank()

    # Query params
    keyword = request.args.get("keyword", type=str)
    limit = request.args.get("limit", type=int)

    # Filter by keyword (optional)
    if keyword:
        phrases = filter_phrases_by_keyword(phrases, keyword)

    # Limit results (optional)
    if limit:
        phrases = top_n_phrases(phrases, limit)

    return jsonify({"phrases": phrases})
