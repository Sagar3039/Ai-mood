from flask import Flask, request, jsonify
from flask_cors import CORS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
CORS(app)

analyzer = SentimentIntensityAnalyzer()

@app.route("/", methods=["GET"])
def home():
    return "AI Emotional Companion API is running!"

@app.route("/analyze", methods=["POST"])
def analyze_sentiment():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Get sentiment score
    sentiment_score = analyzer.polarity_scores(text)["compound"]

    # Determine Mood and Suggestion
    if sentiment_score > 0.2:
        mood = "Positive 😊"
        suggestion = "That's great! Keep up the good vibes. Try some meditation or listen to upbeat music."
    elif sentiment_score < -0.2:
        mood = "Negative 😔"
        suggestion = "It seems like you're feeling down. Talking to a friend or journaling might help. Maybe a short walk too?"
    else:
        mood = "Neutral 😐"
        suggestion = "You're feeling neutral. Maybe listen to some calming music or take a break."

    return jsonify({
        "original_text": text,
        "mood": mood,
        "suggestion": suggestion
    })

if __name__ == "__main__":
    app.run(debug=True)
