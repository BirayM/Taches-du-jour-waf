# Implementation Plan: Compte à Rebours de Fin de Journée

**Branch**: `005-end-of-day-countdown` | **Date**: 2026-11-02 | **Spec**: [specs/005-end-of-day-countdown/spec.md](spec.md)

**Input**: Feature specification from `/specs/005-end-of-day-countdown/spec.md`

## Summary

Cette fonctionnalité enrichit l'application « Tâches du Jour » en intégrant un compte à rebours dynamique dans la carte de motivation (`.quote-card`), disposé aux côtés de l'illustration canine encourageante :
1. **Comportement dynamique en Vanilla JavaScript** : Développé en pur JavaScript moderne (ES6+) dans `app/static/js/countdown.js`, sans aucun framework externe, bundler ou bibliothèque tierce (Constitution II et V).
2. **Pilotage conditionnel côté serveur (Jinja2)** : Affiché uniquement lorsqu'au moins une tâche existe (`{% if tasks %}`), et totalement masqué à l'état vide d'accueil (FR-001, FR-002, SC-002). Le décompte reste visible si toutes les tâches sont accomplies (100% avec bannière de fête).
3. **Calcul d'horloge absolue et transition fluide à minuit** : Calcul instantané basé sur l'horloge système locale (`new Date()`) ciblant le minuit suivant. Format normalisé « HH h MM min SS s » avec zéros initiaux. Transition continue à 00:00:00 vers 23 h 59 min 59 s sans valeur négative ni rechargement (FR-004, FR-006, SC-004), et résilience native au bridage des onglets inactifs.
4. **Accessibilité numérique WAI-ARIA** : Balise sémantique `<time>` avec libellé explicite `aria-label="Temps restant avant la fin de la journée"`, omission stricte d'annonces dynamiques (`aria-live="off"`), et masquage des secondes défilantes via `aria-hidden="true"` pour éviter la pollution sonore des lecteurs d'écran (FR-007, SC-006).
5. **Intégration responsive** : Flexbox harmonieux s'adaptant des smartphones (320px) aux écrans larges (2560px), reprenant la palette chaleureuse existante (SC-005).
6. **Contrôle qualité automatisé avec pytest** : Tests d'intégration Flask validant le rendu conditionnel, la conformité ARIA et la distribution de la ressource statique (Constitution IV).

## Technical Context

**Language/Version**: Python 3.10+ (backend Flask SSR) & JavaScript Vanilla ES6+ (script dynamique client)

**Primary Dependencies**: Flask (unique micro-framework web backend autorisé par la Constitution)

**Storage**: Fichier JSON local (`data/tasks.json`) manipulé par `TaskManager` (inchangé ; aucune donnée de décompte n'est persistée sur le serveur)

**Testing**: `pytest` pour les tests d'intégration HTTP et de rendu des templates (`tests/test_routes.py`) et les tests unitaires (`tests/test_models.py`)

**Target Platform**: Navigateurs modernes (Chrome, Firefox, Safari, Edge) sur desktop et mobile (Linux, macOS, Windows, Android, iOS)

**Project Type**: Application web locale en rendu côté serveur (SSR Flask) avec rehaussement progressif par script Vanilla JS

**Performance Goals**: Exécution du calcul temporel < 1 ms par seconde côté client, 0 ms de surcharge backend, chargement de page < 100 ms

**Constraints**: Zéro nouvelle dépendance (aucun npm, bundler ou CDN), conformité WAI-ARIA stricte (zéro annonce vocale intempestive), dégradation gracieuse en cas de JS désactivé, affichage responsive fluide (320px à 2560px)

**Scale/Scope**: Application mono-utilisateur locale pour le suivi quotidien (1 écran principal, 0 à 50 tâches)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe Constitutionnel | Exigence | Statut | Justification de Conformité |
|--------------------------|----------|--------|-----------------------------|
| **I. Simplicité et Vocation Pédagogique** | Architecture didactique, KISS / YAGNI | **PASS** | Script JavaScript Vanilla direct, fonctions pures (`calculateRemainingTime`, `formatCountdown`), aucun composant abstrait inutile. Code facile à lire pour des apprenants. |
| **II. Stack Web Épurée (HTML/CSS & Flask)** | HTML5/CSS3 natif, Flask unique dépendance backend | **PASS** | Pas de framework frontend lourd (React, Vue, Alpine). Fichier JS statique épuré servi par Flask, gabarit Jinja2 standard avec balises HTML5 sémantiques. |
| **III. Lisibilité et Documentation** | Code commenté, docstrings PEP 257 | **PASS** | Docstrings complètes sur les fonctions et commentaires explicatifs sur les calculs d'intervalles et les règles ARIA. |
| **IV. Tests Automatisés avec pytest** | pytest obligatoire pour la logique applicative | **PASS** | Couverture pytest exhaustive dans `tests/test_routes.py` vérifiant la présence conditionnelle Jinja2, les attributs ARIA et la distribution HTTP 200 du fichier statique JS. |
| **V. Minimalisme des Dépendances** | Uniquement Flask et pytest dans requirements.txt | **PASS** | Aucune nouvelle dépendance. Le fichier `requirements.txt` reste strictement inchangé. Utilisation des API natives du navigateur (`Date`, `setInterval`, `document.getElementById`). |
| **VI. Sécurité et Données Sensibles** | Zéro secret, gestion sûre des requêtes | **PASS** | Aucune clé, aucun secret, aucun échange réseau sensible. Calcul d'horloge 100% confiné au navigateur client. |

## Project Structure

### Documentation (this feature)

```text
specs/005-end-of-day-countdown/
├── spec.md              # Spécification fonctionnelle et critères d'acceptation
├── clarifications.md    # Clarifications techniques actées (Vanilla JS, Jinja2, ARIA)
├── plan.md              # Ce document (plan d'architecture et de mise en œuvre)
├── research.md          # Recherches et décisions techniques validées (Phase 0)
├── data-model.md        # Modèles d'entités, données temporelles et transitions (Phase 1)
├── quickstart.md        # Guide de démarrage et scénarios de validation (Phase 1)
├── contracts/           # Contrats d'interfaces
│   └── web-routes.md    # Contrat Jinja2, API JS client, ARIA et CSS (Phase 1)
└── checklists/
    └── requirements.md  # Checklist de conformité des exigences
```

### Source Code (repository root)

```text
app/
├── __init__.py          # Usine logicielle Flask (create_app)
├── models.py            # Task, TaskManager, ProgressStats (inchangé)
├── routes.py            # Routes Flask (GET /, POST /tasks/add, etc.)
├── quotes.py            # Citations de motivation et d'accueil
├── static/
│   ├── css/
│   │   └── style.css    # Styles CSS pour .quote-countdown, .countdown-display, responsive
│   ├── js/
│   │   └── countdown.js # Script Vanilla JS : calcul temporel, défilement et mise à jour DOM
│   └── images/
│       └── dogs/
│           ├── dog-cheer.svg    # Illustration de célébration (maintien du compte à rebours)
│           ├── dog-happy.svg    # Mascotte principale
│           └── dog-resting.svg  # État vide (masquage du compte à rebours)
└── templates/
    ├── base.html        # Gabarit structurel HTML5
    └── index.html       # Gabarit principal : condition Jinja2 {% if tasks %} et bloc countdown

data/
└── tasks.json           # Stockage JSON des tâches (inchangé)

tests/
├── conftest.py          # Fixtures de test pytest
├── test_models.py       # Tests unitaires de la couche modèle
└── test_routes.py       # Tests d'intégration Flask (condition Jinja2, ARIA, ressource statique JS)
```

**Structure Decision**:
- La logique dynamique de l'horloge réside dans un fichier statique dédié `app/static/js/countdown.js`, évitant toute surcharge du backend Flask.
- L'affichage conditionnel est piloté au niveau du gabarit `app/templates/index.html` via Jinja2 (`{% if tasks %}`), garantissant qu'aucun balisage ni script ne tourne lorsque l'application est à l'état vide.
- Les styles sont intégrés dans `app/static/css/style.css` en respectant la charte visuelle canine bienveillante.
- Les vérifications automatisées sont assurées dans `tests/test_routes.py` avec `pytest`.

## Complexity Tracking

> Aucune violation constitutionnelle. Toutes les exigences fondamentales (KISS, SSR Flask, CSS pur, Vanilla JS sans dépendance, pytest non-négociable, zéro npm) sont strictement respectées.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| *Aucune* | - | - |
