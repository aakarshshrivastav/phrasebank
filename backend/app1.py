from flask import Flask
from flask_cors import CORS

# Import all route blueprints
from routes.stt_route import stt_bp
from routes.translate_route import translate_bp
from routes.tts_route import tts_bp
from routes.score_route import score_bp
from routes.phrases_route import phrases_bp
from routes.log_route import log_bp


def create_app():
    """
    Application factory for the Voice Translator backend.
    Loads all blueprints and configures CORS.
    """
    app = Flask(__name__)

    # Enable CORS (allow calls from React frontend on port 3000)
    CORS(app, resources={r"*": {"origins": "*"}})

    # Register all blueprints
    app.register_blueprint(stt_bp)
    app.register_blueprint(translate_bp)
    app.register_blueprint(tts_bp)
    app.register_blueprint(score_bp)
    app.register_blueprint(phrases_bp)
    app.register_blueprint(log_bp)

    @app.route("/")
    def home():
        return {"status": "Voice Translator Backend Running"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)

