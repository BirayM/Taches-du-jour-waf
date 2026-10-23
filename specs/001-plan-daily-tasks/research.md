# Research & Technical Decisions: Planification des Tâches du Jour

**Feature**: `001-plan-daily-tasks` | **Date**: 2026-10-22

Ce document synthétise les choix d'architecture et de conception technique retenus pour implémenter la fonctionnalité de planification quotidienne des tâches, en conformité stricte avec la constitution du projet (simplicité, code pédagogique, Flask comme unique dépendance serveur, HTML/CSS pur et tests pytest).

## Décision 1 : Architecture Web & Mode de Rendu

- **Décision** : Rendu côté serveur pur (*Server-Side Rendering* - SSR) avec le moteur de templates Jinja2 intégré nativement à Flask et des formulaires HTML standards suivant le patron **PRG (Post/Redirect/Get)**.
- **Rationale** :
  - Conforme au principe constitutionnel II (HTML5/CSS3 natif, pas de frameworks JavaScript lourds).
  - Le patron PRG garantit qu'après validation d'un formulaire, le navigateur est redirigé vers la page d'accueil avec un champ de saisie vide et propre, évitant ainsi tout renvoi accidentel de formulaire lors d'un rafraîchissement (F5).
  - Très didactique pour des apprenants : le cycle requête-réponse HTTP est explicite et limpide.
- **Alternatives rejetées** :
  - *Single Page Application (SPA) / React / Vue* : Rejeté (interdit par la constitution, surcharge conceptuelle et dépendances inutiles).
  - *Requêtes asynchrones Fetch/AJAX* : Rejeté pour la v1 (le rechargement fluide en SSR avec formulaires natifs répond à 100% du besoin utilisateur avec une simplicité maximale).

## Décision 2 : Mécanisme de Persistance Locale

- **Décision** : Fichier JSON structuré (`data/tasks.json`) manipulé via le module standard `json` de Python, encapsulé dans un gestionnaire de persistance dédié (`app/models.py`).
- **Rationale** :
  - Conforme à la clarification utilisateur exigeant la préservation des tâches entre redémarrages.
  - Conforme au principe de minimalisme des dépendances (utilise `json` de la bibliothèque standard).
  - Lisibilité absolue : les apprenants et développeurs peuvent ouvrir le fichier `tasks.json` directement pour observer comment les données sont modélisées et stockées.
  - Initialisation automatique : si le fichier ou le dossier `data/` n'existe pas au démarrage, le service le crée automatiquement avec une liste vide `[]`.
- **Alternatives rejetées** :
  - *Base de données relationnelle SQLite / SQLAlchemy* : Rejeté pour la v1 (trop lourd et abstrait pour une liste pédagogique simple d'une vingtaine de tâches quotidiennes).
  - *Stockage éphémère en mémoire vive* : Rejeté suite à la clarification explicite de l'utilisateur demandant la persistance locale.

## Décision 3 : Gestion des Citations Positives et Canines

- **Décision** : Module statique dédié `app/quotes.py` exposant une collection de citations bienveillantes thématisées sur les chiens et une fonction de sélection aléatoire basée sur `random.choice`.
- **Rationale** :
  - Isole la responsabilité du contenu textuel de la logique de contrôle et d'affichage.
  - Utilise la bibliothèque standard (`random`), sans aucune dépendance externe.
  - Facile à enrichir par des élèves ou contributeurs sans impacter le code de l'application.
- **Alternatives rejetées** :
  - *Appel à une API externe de citations* : Rejeté (violation du principe d'autonomie locale sans dépendance réseau externe).
  - *Stockage des citations en base de données* : Rejeté (complexité inutile pour une liste fixe de messages prédéfinis).

## Décision 4 : Intégration Visuelle et Assets Canins

- **Décision** : Utilisation d'illustrations canines au format vectoriel **SVG** intégrées localement dans `app/static/images/dogs/` et stylisées via CSS3 pur (variables CSS, flexbox, palettes chaleureuses).
- **Rationale** :
  - Les fichiers SVG sont légers, redimensionnables sans perte de qualité et stockés localement dans le dépôt sans risque de dépendance réseau ou d'assets manquants.
  - Le CSS utilise des variables CSS claires (`--color-warm-bg`, `--color-primary`, `--font-main`) pour faciliter la lecture et la personnalisation pédagogique.
- **Alternatives rejetées** :
  - *Frameworks CSS (Bootstrap, Tailwind)* : Rejeté par la constitution qui privilégie le CSS natif pour l'apprentissage.
  - *Images Bitmap lourdes non optimisées* : Rejeté pour maintenir la légèreté du dépôt.

## Décision 5 : Stratégie de Tests Automatisés avec pytest

- **Décision** : Organisation des tests sous `tests/` avec `pytest` et `pytest-flask` (ou le client de test natif `app.test_client()`), séparant :
  1. Les tests unitaires du modèle et de la persistance JSON (`tests/test_models.py`).
  2. Les tests d'intégration des routes HTTP et formulaires (`tests/test_routes.py`).
  3. L'isolation des données via une fixture pytest temporaire (`tmp_path`) pour ne jamais altérer les données réelles du projet pendant l'exécution des tests.
- **Rationale** :
  - Satisfait l'exigence constitutionnelle non négociable de couverture de test pytest pour toute la logique Python.
  - `app.test_client()` permet de simuler des requêtes HTTP complètes (GET, POST) sans lancer de serveur réseau réel.
