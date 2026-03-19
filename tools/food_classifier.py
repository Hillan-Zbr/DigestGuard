import os
import json
import base64
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY introuvable dans .env")

def get_sop_content():
    sop_path = os.path.join(os.path.dirname(__file__), '..', 'architecture', 'food_classification_sop.md')
    with open(sop_path, 'r', encoding='utf-8') as f:
        return f.read()

def classify_food(text_query=None, image_data=None):
    client = genai.Client(api_key=api_key)
    
    system_instruction = (
        "Tu es l'Expert en épargne digestive du système DigestGuard.\n"
        "Respecte STRICTEMENT les règles définies dans le SOP suivant:\n"
        f"{get_sop_content()}\n\n"
        "Assure-toi de renvoyer UNIQUEMENT le dictionnaire JSON demandé dans la section 4."
    )

    contents = []
    
    if image_data:
        if image_data.startswith('data:image'):
            header, b64_str = image_data.split(',', 1)
            mime_type = header.split(':')[1].split(';')[0]
        else:
            b64_str = image_data
            mime_type = "image/jpeg"

        image_bytes = base64.b64decode(b64_str)
        contents.append(
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type
            )
        )

    if text_query:
        contents.append(text_query)

    if not contents:
        return {
            "status": "error",
            "food_name": "Inconnu",
            "classification": "inconnu",
            "visual_score": 0,
            "advice": "Aucune information fournie (texte ou image).",
            "followup_question": ""
        }

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
            )
        )
        return json.loads(response.text)

    except Exception as e:
        return {
            "status": "error",
            "food_name": "Erreur Interne",
            "classification": "inconnu",
            "visual_score": 0,
            "advice": f"Erreur API: {str(e)}",
            "followup_question": ""
        }
