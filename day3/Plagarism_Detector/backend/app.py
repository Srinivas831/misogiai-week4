# app.py

from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from flask_cors import CORS
from utils.preprocess import preprocess_texts
from utils.embedding import get_openai_embeddings
from utils.similarity import calculate_similarity_matrix
from utils.detector import detect_clones


# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # ← ADD THIS


@app.route("/api/analyze", methods=["POST"])
def analyze_texts():
    data = request.get_json()
    texts = data.get("texts", [])
    print("texts",texts)
    if len(texts) < 2:
        return jsonify({"error": "At least 2 texts required"}), 400

    try:
        # 1. Preprocess
        cleaned_texts = preprocess_texts(texts)
        print("cleaned_texts",cleaned_texts)
        # 2. Get Embeddings
        embeddings = get_openai_embeddings(cleaned_texts, OPENAI_API_KEY)
        print("embeddings",embeddings)
        # 3. Similarity Matrix
        similarity_matrix = calculate_similarity_matrix(embeddings)
        print("similarity_matrix",similarity_matrix)

        # 4. Clone Detection
        clones = detect_clones(similarity_matrix, threshold=0.7)

        return jsonify({
            "similarity_matrix": similarity_matrix,
            "clones": clones
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
