---
applyTo: "**"
---

# Instructions Générales GitHub Copilot

## 1. Organisation et taille des fichiers

- Limiter chaque fichier à **200 lignes maximum** pour maintenir une bonne lisibilité.
- Si un fichier dépasse cette taille, **découper le code en plusieurs fichiers plus petits**, thématiques et modulaires.
- Organiser les fichiers par fonctionnalité ou couche (ex : logique métier, interface, utilitaires).

## 2. Qualité et style de code

- Favoriser un code **clair, simple et lisible** pour faciliter la maintenance.
- Respecter les conventions et bonnes pratiques du langage utilisé (ex : PEP8 pour Python, ESLint pour JavaScript).
- Utiliser une indentation cohérente, préférablement 2 ou 4 espaces selon la norme du langage.
- Utiliser des noms **explicites** pour variables, fonctions, classes, et modules.
- Éviter les répétitions en créant des fonctions ou classes réutilisables.

## 3. Conception et modularité

- Structurer le code en **fonctions ou classes courtes**, focalisées sur une seule responsabilité.
- Documenter chaque fonction, classe, interface ou module avec un commentaire clair sur son rôle et son usage.
- Prioriser les interfaces propres et bien définies.
- Favoriser la réutilisation des composants pour éviter la duplication.

## 4. Commentaires et documentation

- Ajouter des **commentaires explicatifs uniquement** quand le code n'est pas immédiatement clair.
- Utiliser des docstrings ou annotations standard du langage pour documenter les API publiques.
- Inclure des exemples d'utilisation pour les fonctions complexes ou critiques.

## 5. Performance et simplicité

- Éviter la complexité inutile, privilégier des solutions simples et efficaces.
- Optimiser seulement quand une amélioration claire est nécessaire.
- Écrire un code robuste, qui gère proprement les erreurs et conditions limites.

## 6. Tests et validation

- Développer des tests unitaires ou d'intégration associés à chaque fonctionnalité importante.
- Assurer que le code passe les tests existants avant l'intégration.

---