from flask import Blueprint, request, jsonify
from transformers import pipeline

# Blueprint setup
sentiment_bp = Blueprint("sentiment", __name__)

# Load the sentiment analysis pipeline (auto-downloads model on first run)
sentiment_model = pipeline("sentiment-analysis")

@sentiment_bp.route("/analyze", methods=["POST"])
def analyze_sentiment():
    try:
        data = request.get_json()
        text = data.get("text", "")

        if not text:
            return jsonify({"error": "Text is required"}), 400

        # Perform sentiment analysis
        result = sentiment_model(text)[0]
        return jsonify({
            "label": result["label"],
            "score": round(result["score"], 4)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

                        