# Findings

## Research & Discoveries
- **North Star**: Application type "Épargne digestive / Pauvre en résidus" pour chouchouter le système digestif. Éviter aliments gras et fermentescibles.
- **Source of Truth**: Complètement "Stateless". Aucune base de données nécessaire pour l'historique utilisateur.
- **Integration**: Gemini API (requiert gestion du texte et d'images/photos).

## Constraints
- **Fallback obligatoire** : Le système doit pouvoir admettre son ignorance et demander plus d'infos s'il ne reconnaît pas l'image ou l'aliment décrit.
- Affichage clair avec une "échelle simple et visuelle", nécessitant un formatage précis du résultat issu du LLM.
