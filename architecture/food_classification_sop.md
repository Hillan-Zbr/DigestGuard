# SOP : Food Classification Engine (Layer 1)

## 1. Goal
Évaluer un aliment (saisi via texte ou soumis via image) et déterminer s'il convient à un régime d'épargne digestive (pauvre en résidus), afin de générer un Payload JSON strict pour le frontend.

## 2. Inputs (Layer 2 -> Layer 3)
- `text_query`: String (Optionnel)
- `image_data`: Base64 String (Optionnel)

*Note*: Il faut au minimum un des deux paramètres.

## 3. Tool Logic (Prompting & Rules)
- **Rôle du système** : Expert en nutrition spécialisé en gastro-entérologie et régime sans résidus. Ton léger et bienveillant.
- **Contraintes de Santé strictes** :
  1. ÉVITER les aliments fermentescibles (choux, légumes secs, oignons, céréales complètes).
  2. ÉVITER les aliments trop gras (fritures, viandes grasses, charcuteries, sauces riches).
  3. PRIVILÉGIER les protéines maigres (viande blanche, poisson sans sauce grasse), les féculents raffinés (riz blanc, pâtes non complètes), et les laitages sans lactose ou selon la tolérance individuelle.
- **Système de Notation (Visual Score)** :
  - `1-2` : À éviter ou limiter fortement (Irritant ou trop gras/fermentescible)
  - `3` : À consommer avec modération selon tolérance individuelle
  - `4-5` : À privilégier (Parfait pour l'épargne digestive)
- **Zero-Hallucination Policy** : Si l'aliment n'est pas reconnaissable ou trop ambigu, la classification est ignorée, `status` devient `needs_info`, et un `followup_question` est posé.

## 4. Expected Output (JSON Payload)
```json
{
  "status": "success | needs_info | error",
  "food_name": "Nom de l'aliment identifié",
  "classification": "privilégier | modération | éviter",
  "visual_score": 1,
  "advice": "Court conseil bienveillant et léger",
  "followup_question": "Question de clarification (requis si needs_info)"
}
```

## 5. Edge Cases
- Image illisible/floue -> Rejeter poliment et demander plus d'infos (`needs_info`).
- Aliment composé mixte (ex: un plat en sauce avec légumes) -> Le score s'aligne sur l'ingrédient limitant (le pire ingrédient en termes digestifs).
