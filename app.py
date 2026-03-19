from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Rendre tools/ impportable
sys.path.append(os.path.dirname(__file__))

from tools.food_classifier import classify_food

app = Flask(__name__)
CORS(app)

@app.route('/api/classify', methods=['POST'])
def classify():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON payload provided"}), 400

    text_query = data.get("text_query", "").strip()
    image_data = data.get("image_data", "").strip()

    if not text_query and not image_data:
        return jsonify({"error": "Veuillez fournir au moins un texte ou une image"}), 400

    # Routage strict vers Layer 3
    result = classify_food(
        text_query=text_query if text_query else None, 
        image_data=image_data if image_data else None
    )
    
    return jsonify(result)

if __name__ == '__main__':
    print("Démarrage du Serveur DigestGuard sur le port 5000...")
    app.run(debug=True, port=5000)
