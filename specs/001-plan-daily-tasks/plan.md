# Implementation Plan: Planification des Tâches du Jour

**Branch**: `001-plan-daily-tasks` | **Date**: 2026-10-22 | **Spec**: [specs/001-plan-daily-tasks/spec.md](spec.md)

**Input**: Feature specification from `/specs/001-plan-daily-tasks/spec.md`

## Summary

L'application « Tâches du Jour » permet aux utilisateurs de planifier leurs activités quotidiennes via une interface web chaleureuse et réconfortante, ornée d'illustrations de chiens et de citations positives. L'implémentation technique s'appuie sur une architecture Flask en rendu côté serveur (SSR) sans framework JavaScript, utilisant des formulaires HTML standards suivant le patron Post/Redirect/Get pour une saisie en chaîne fluide. Les données sont persistées localement dans un fichier `data/tasks.json` manipulé par la bibliothèque standard Python, et l'intégralité de la logique est rigoureusement couverte par des tests automatisés `pytest`.

## Technical Context

**Language/Version**: Python 3.10+ (typé avec type hints standard)

**Primary Dependencies**: Flask (unique framework web backend autorisé)

**Storage**: Fichier JSON local (`data/tasks.json`) manipulé via le module standard `json` avec initialisation automatique

**Testing**: `pytest` pour les tests unitaires et d'intégration HTTP (via `app.test_client()`)

**Target Platform**: Multiplateforme (Linux, macOS, Windows), exécution locale

**Project Type**: Application web locale en rendu côté serveur (SSR)

**Performance Goals**: Temps de réponse local < 100ms, réactivité instantanée pour l'enchaînement de la saisie

**Constraints**: Zéro framework JavaScript, HTML5 sémantique et CSS3 pur, code pédagogique largement commenté, zéro donnée sensible dans le dépôt

**Scale/Scope**: Application mono-utilisateur locale pour l'organisation quotidienne (1 à 50 tâches par session)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe Constitutionnel | Exigence | Statut | Justification de Conformité |
|--------------------------|----------|--------|-----------------------------|
| **I. Simplicité et Vocation Pédagogique** | Architecture didactique, KISS / YAGNI | **PASS** | Conception linéaire et modulaire : un modèle clair, des routes explicites et des templates simples sans abstraction superflue. |
| **II. Stack Web Épurée (HTML/CSS & Flask)** | HTML5/CSS3 natif, Flask unique dépendance backend | **PASS** | Aucun framework JS externe. Frontend pur HTML/CSS avec variables CSS. Flask assure le routage et le rendu Jinja2. |
| **III. Lisibilité et Documentation** | Code commenté, docstrings PEP 257 | **PASS** | Modules structurés avec commentaires pédagogiques détaillés pour faciliter la lecture par des apprenants. |
| **IV. Tests Automatisés avec pytest** | pytest obligatoire pour la logique Python | **PASS** | Tests unitaires du modèle/persistance et tests d'intégration des routes HTTP définis et exécutés avec pytest. |
| **V. Minimalisme des Dépendances** | Uniquement Flask et pytest dans requirements.txt | **PASS** | Utilisation exclusive de la bibliothèque standard (`json`, `random`, `uuid`, `os`, `datetime`) complétée de Flask et pytest. |
| **VI. Sécurité et Données Sensibles** | Zéro secret, .gitignore rigoureux | **PASS** | Aucune clé d'API ni donnée sensible ; exclusion des fichiers temporaires (`.pytest_cache`, `__pycache__`) dans `.gitignore`. |

## Project Structure

### Documentation (this feature)

```text
specs/001-plan-daily-tasks/
├── spec.md              # Spécification fonctionnelle (/speckit.specify)
├── plan.md              # Plan technique d'architecture (/speckit.plan)
├── research.md          # Recherches et décisions techniques (Phase 0)
├── data-model.md        # Modèles de données et schéma JSON (Phase 1)
├── quickstart.md        # Guide de démarrage et scénarios de validation (Phase 1)
├── contracts/           # Contrats d'interfaces
│   └── web-routes.md    # Spécification des routes HTTP Flask
└── checklists/
    └── requirements.md  # Checklist de validation des exigences
```

### Source Code (repository root)

```text
app/
├── __init__.py          # Usine applicative Flask (create_app)
├── models.py            # Classe Task et gestionnaire de persistance JSON
├── routes.py            # Routes HTTP (GET /, POST /tasks, POST /tasks/<id>/complete)
├── quotes.py            # Collection de citations positives et canines
├── static/
│   ├── css/
│   │   └── style.css    # Feuille de style chaleureuse en CSS3 pur
│   └── images/
│       └── dogs/        # Illustrations vectorielles SVG canines locales
└── templates/
    ├── base.html        # Gabarit principal HTML5
    └── index.html       # Vue principale : formulaire, liste et messages

data/
└── tasks.json           # Fichier local de stockage des tâches (créé automatiquement)

tests/
├── __init__.py
├── conftest.py          # Fixtures pytest (client de test, dossier data temporaire)
├── test_models.py       # Tests unitaires de la logique Task et de la persistance
└── test_routes.py       # Tests d'intégration des routes et des interactions

requirements.txt         # Dépendances minimales : flask, pytest
run.py                   # Point d'entrée pour lancer le serveur local
.gitignore               # Exclusion des caches, venv et fichiers temporaires
```

**Structure Decision**: Architecture applicative Flask modulaire organisée sous `app/` avec séparation claire du domaine métier (`models.py`), des points d'accès HTTP (`routes.py`), des templates Jinja2 et des styles/images statiques. Les tests automatisés sont isolés dans `tests/` et utilisent une base de données JSON temporaire pour garantir la reproductibilité des tests sans effets de bord.

## Complexity Tracking

> Aucune violation des règles constitutionnelles n'a été introduite. Toutes les directives (Flask unique dépendance, HTML/CSS natif, pytest obligatoire) sont strictement respectées.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| *Aucune* | - | - |
