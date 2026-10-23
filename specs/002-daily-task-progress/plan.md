# Implementation Plan: Suivi de la Progression Quotidienne

**Branch**: `002-daily-task-progress` | **Date**: 2026-10-23 | **Spec**: [specs/002-daily-task-progress/spec.md](spec.md)

**Input**: Feature specification from `/specs/002-daily-task-progress/spec.md`

## Summary

Cette fonctionnalité enrichit l'application « Tâches du Jour » d'un système de suivi visuel et dynamique de l'avancement quotidien :
1. Calcul automatique et transparent des statistiques de progression (nombre de tâches terminées, total, pourcentage de complétion arrondi).
2. Affichage d'un compteur textuel clair (ex. « 2 sur 4 tâches terminées (50%) ») et d'une barre de progression graphique accessible (HTML5 sémantique et CSS3 pur).
3. Déclenchement d'un message spécial de félicitations chaleureux accompagné d'une illustration canine festive (`dog-cheer.svg`) dès que 100% des tâches sont accomplies (avec au moins une tâche planifiée).
4. Respect strict du rendu côté serveur (SSR) avec Flask, sans aucun framework JavaScript, avec une couverture exhaustive par des tests automatisés `pytest`.

## Technical Context

**Language/Version**: Python 3.10+ (typé avec type hints standard)

**Primary Dependencies**: Flask (unique dépendance web backend autorisée par la constitution)

**Storage**: Fichier JSON local (`data/tasks.json`) manipulé via le module standard `json` (aucun changement requis sur le schéma JSON persistant)

**Testing**: `pytest` pour les tests unitaires et d'intégration HTTP (via `app.test_client()`)

**Target Platform**: Multiplateforme (Linux, macOS, Windows), exécution locale

**Project Type**: Application web locale en rendu côté serveur (SSR)

**Performance Goals**: Temps de réponse local < 100ms, calcul instantané de la progression en mémoire vive

**Constraints**: Zéro framework JavaScript, HTML5 sémantique avec attributs ARIA d'accessibilité (`role="progressbar"`, `aria-valuenow`, `aria-valuemin`, `aria-valuemax`), CSS3 pur avec variables CSS, code didactique et rigoureusement commenté

**Scale/Scope**: Application mono-utilisateur locale pour l'organisation quotidienne (0 à 50 tâches par session)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe Constitutionnel | Exigence | Statut | Justification de Conformité |
|--------------------------|----------|--------|-----------------------------|
| **I. Simplicité et Vocation Pédagogique** | Architecture didactique, KISS / YAGNI | **PASS** | Modélisation claire d'un objet/statistique de progression (`ProgressStats`), injection directe dans le template Jinja2, logique linéaire sans complexité superflue. |
| **II. Stack Web Épurée (HTML/CSS & Flask)** | HTML5/CSS3 natif, Flask unique dépendance backend | **PASS** | Aucun framework JS externe. Barre de progression réalisée en HTML/CSS pur avec propriétés CSS personnalisées (`width: X%`). Flask assure le calcul et le rendu SSR. |
| **III. Lisibilité et Documentation** | Code commenté, docstrings PEP 257 | **PASS** | Fonctions et classes munies de docstrings explicites et de commentaires pédagogiques expliquant le calcul du pourcentage et les règles des cas limites. |
| **IV. Tests Automatisés avec pytest** | pytest obligatoire pour la logique Python | **PASS** | Tests unitaires dédiés au calcul de progression (0 tâche, pourcentages arrondis, 100% de complétion) et tests d'intégration pour le rendu HTML du composant et de la bannière festive. |
| **V. Minimalisme des Dépendances** | Uniquement Flask et pytest dans requirements.txt | **PASS** | Utilisation exclusive de la bibliothèque standard Python (`dataclasses`, `typing`) avec Flask et pytest. |
| **VI. Sécurité et Données Sensibles** | Zéro secret, .gitignore rigoureux | **PASS** | Aucune clé, aucun secret, aucun cookie non sécurisé ni donnée sensible. |

## Project Structure

### Documentation (this feature)

```text
specs/002-daily-task-progress/
├── spec.md              # Spécification fonctionnelle (/speckit.specify)
├── plan.md              # Plan technique d'architecture (/speckit.plan)
├── research.md          # Recherches et décisions techniques (Phase 0)
├── data-model.md        # Modèles de données et entités de progression (Phase 1)
├── quickstart.md        # Guide de démarrage et scénarios de validation (Phase 1)
├── contracts/           # Contrats d'interfaces
│   └── web-routes.md    # Contrat d'affichage et contexte template Jinja2
└── checklists/
    └── requirements.md  # Checklist de validation des exigences
```

### Source Code (repository root)

```text
app/
├── __init__.py          # Usine applicative Flask (create_app)
├── models.py            # Task, TaskManager et calcul des statistiques de progression
├── routes.py            # Route GET / avec injection des données de progression
├── quotes.py            # Citations de motivation et messages de félicitations
├── static/
│   ├── css/
│   │   └── style.css    # Styles CSS pour la barre de progression et la bannière festive
│   └── images/
│       └── dogs/
│           ├── dog-cheer.svg    # Illustration festive pour la complétion à 100%
│           ├── dog-happy.svg    # Illustration d'accompagnement
│           └── dog-resting.svg  # Illustration état vide
└── templates/
    ├── base.html        # Gabarit principal HTML5
    └── index.html       # Intégration de la barre de progression et des félicitations

data/
└── tasks.json           # Stockage JSON existant (non altéré dans sa structure)

tests/
├── conftest.py          # Fixtures pytest
├── test_models.py       # Tests unitaires (dont le calcul de progression et cas limites)
└── test_routes.py       # Tests d'intégration HTTP (présence de la barre et des félicitations)
```

**Structure Decision**: La logique de calcul de la progression est intégrée au domaine métier dans `app/models.py` (méthode de `TaskManager` ou dataclass dédiée `ProgressStats`), garantissant sa réutilisabilité et son testabilité unitaire indépendamment du web. La route `GET /` de `app/routes.py` transmet ces statistiques au template `app/templates/index.html`. Les styles CSS associés sont ajoutés à `app/static/css/style.css` et tirent parti de l'illustration SVG existante `dog-cheer.svg`.

## Complexity Tracking

> Aucune violation constitutionnelle. Toutes les directives (KISS, SSR Flask, CSS pur, pytest) sont strictement respectées.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| *Aucune* | - | - |
