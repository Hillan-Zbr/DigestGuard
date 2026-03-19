# Project Constitution (gemini.md)

## Data Schemas

**Input (Frontend -> Tool)**:
```json
{
  "text_query": "string (texte saisi par l'utilisateur, optionnel si image)",
  "image_data": "string (image encodée en base64, optionnel si texte)"
}
```

**Output (Tool -> Payload Frontend)**:
```json
{
  "status": "success | needs_info | error",
  "food_name": "string (nom de l'aliment identifié)",
  "classification": "privilégier | modération | éviter",
  "visual_score": "integer (1 à 5, où 1=Éviter complètement et 5=Parfait pour épargne digestive)",
  "advice": "string (explication sur un ton léger et bienveillant)",
  "followup_question": "string (question si status == needs_info pour demander des précisions)"
}
```

## Behavioral Rules
1. **Ton Général** : Léger, bienveillant, orienté sur l'idée de "chouchouter son système digestif".
2. **Tolérance Zéro (Hallucination)** : Si l'aliment n'arrive pas à être identifié ou si la classification (ex: quantité de fibres/graisses) n'est pas sûre, le système DOIT demander plus d'informations (répondre "pas assez d'info").
3. **Logique Métier** : Le régime "épargne digestive" / "pauvre en résidus" exige d'éviter ce qui fermente (fibres dures) et ce qui est trop gras.

## Architectural Invariants
- Application Stateless : aucune donnée de recherche n'est stockée de manière persistante.
- L'API Gemini (Vision/Text) est la seule source d'intelligence du pipeline.
- 3-Layer Architecture stricte.

## Maintenance Log
- Initialisation du schéma de données JSON (Input/Output).
- [Link] Validation de l'authentification avec `google-genai`.
- [Architect] SOP métier d'Épargne Digestive défini et encodé dans `food_classifier.py`.
- [Stylize] Intégration de l'interface graphique (Glassmorphism) testée et validée (Vanilla HTML/CSS/JS).
- [Trigger] Création du script d'exécution locale Windows `start_blast.bat`.
