import os
import sys
from dotenv import load_dotenv

try:
    from google import genai
except ImportError:
    print("Veuillez installer le sdk: pip install google-genai")
    sys.exit(1)

# Charger les variables d'environnement
load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key or api_key == "votre_cle_api_ici":
    print("ERREUR : GEMINI_API_KEY est introuvable ou n'a pas été modifiée dans le fichier .env.")
    print("Action requise : Ouvrez le fichier .env et insérez votre vraie clé API Gemini.")
    sys.exit(1)

def test_connection():
    try:
        print("Test de connexion à l'API Gemini...")
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents='Test de connexion. Réponds uniquement par le mot "SUCCÈS" si tu me reçois.'
        )
        print(f"L'API a répondu : {response.text.strip()}")
        print("La Phase 2 (Link) est validée !")
    except Exception as e:
        print(f"ÉCHEC DU TEST. Raison : {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_connection()
