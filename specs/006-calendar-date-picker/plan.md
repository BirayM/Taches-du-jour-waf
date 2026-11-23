# Implementation Plan: Calendrier et Marquage de Dates

**Branch**: `006-calendar-date-picker` | **Date**: 2026-11-23 | **Spec**: [specs/006-calendar-date-picker/spec.md](spec.md)

**Input**: Feature specification from `/specs/006-calendar-date-picker/spec.md` et clarifications techniques de [clarifications.md](clarifications.md)

## Summary

Cette fonctionnalité dote l'application « Tâches du Jour » d'un calendrier mensuel interactif permettant de visualiser le mois en cours et de marquer (cocher/décocher) des dates importantes avec persistance locale :
1. **Grille calendaire mensuelle (7 colonnes)** : Rendu côté serveur (Jinja2/Flask) avec la bibliothèque standard `calendar` de Python. Semaines alignées du lundi au dimanche, cases de remplissage pour aligner le 1er du mois, et mise en évidence de la date « Aujourd'hui » (FR-001, FR-002, FR-003).
2. **Cochage/décochage persistant et réactif (< 150 ms)** : Route JSON `POST /calendar/toggle` et script client `app/static/js/calendar.js` (Vanilla JS ES6+). Mise à jour optimiste du DOM en < 20 ms avec symbole patte canine 🐾, envoi asynchrone via `fetch()`, et persistance dans un fichier dédié `data/calendar.json` administré par `CalendarManager` (FR-004, FR-005, FR-006, SC-002, SC-003).
3. **Navigation temporelle robuste** : Navigation serveur via paramètres d'URL `GET /?year=YYYY&month=MM` avec boutons « Mois précédent », « Mois suivant » et retour direct « Aujourd'hui ». Validation défensive avec repli automatique sur le mois courant en cas de paramètres hors limites (FR-007, SC-004).
4. **Compteur mensuel bienveillant** : Indicateur dynamique du nombre de jours cochés dans le mois (« Aucun jour coché ce mois-ci », « X jour(s) coché(s) ce mois-ci ») avec encouragements canins (FR-008).
5. **Accessibilité WAI-ARIA et design responsive** : Grille entièrement pilotable au clavier (Tab, Espace, Entrée), attributs `aria-pressed` et libellés vocaux complets. CSS fluide sans défilement horizontal de 320px à 2560px avec cibles tactiles >= 40x40px (FR-009, FR-010, SC-005, SC-006).
6. **Harmonisation de la date d'aujourd'hui** : Date serveur par défaut, avec ajustement dynamique par le client JS selon le fuseau horaire local de l'utilisateur (`new Date()`).
7. **Couverture de tests pytest exhaustive** : Tests unitaires de `CalendarManager` et `CheckedDate` dans `tests/test_models.py`, tests d'intégration HTTP et de rendu Jinja2 dans `tests/test_routes.py`.

## Technical Context

**Language/Version**: Python 3.10+ (backend Flask SSR & JSON endpoint) & JavaScript Vanilla ES6+ (script interactif client)

**Primary Dependencies**: Flask (unique micro-framework web backend autorisé par la Constitution)

**Storage**: Fichier JSON dédié (`data/calendar.json`) géré par `CalendarManager` (configuré via `app.config["CALENDAR_DATA_FILE"]`), garantissant l'isolation totale par rapport à `data/tasks.json`

**Testing**: `pytest` pour les tests unitaires (`tests/test_models.py`) et les tests d'intégration HTTP / rendu de routes (`tests/test_routes.py`)

**Target Platform**: Navigateurs modernes (Chrome, Firefox, Safari, Edge) sur desktop et mobile (Linux, macOS, Windows, Android, iOS)

**Project Type**: Application web locale en rendu côté serveur (SSR Flask) rehaussée en Vanilla JS sans framework frontend lourd

**Performance Goals**: Bascule visuelle de date < 20 ms (optimiste), retour réseau < 150 ms (SC-002), chargement de page < 100 ms

**Constraints**: Zéro nouvelle dépendance (aucun npm, bundler ou bibliothèque JS/CSS tierce), conformité WAI-ARIA stricte (`aria-pressed`, navigation clavier), responsive sans débordement horizontal à 320px/360px, dégradation gracieuse en cas de JS inactif

**Scale/Scope**: Application mono-utilisateur locale (1 écran d'accueil avec section calendrier sous la liste des tâches, calendrier mensuel multi-années)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe Constitutionnel | Exigence | Statut | Justification de Conformité |
|--------------------------|----------|--------|-----------------------------|
| **I. Simplicité et Vocation Pédagogique** | Architecture didactique, KISS / YAGNI | **PASS** | `CalendarManager` compact et lisible, utilisation du module standard `calendar` de Python, script JS limpide sans abstractions complexes. |
| **II. Stack Web Épurée (HTML/CSS & Flask)** | HTML5/CSS3 natif, Flask unique dépendance backend | **PASS** | Grille CSS native en Flexbox/CSS Grid, HTML5 sémantique, route Flask standard `@bp.route("/calendar/toggle")`. Aucun framework frontend lourd. |
| **III. Lisibilité et Documentation** | Code commenté, docstrings PEP 257 | **PASS** | Docstrings complètes sur toutes les classes et fonctions, commentaires didactiques sur le calcul de la grille et l'accessibilité ARIA. |
| **IV. Tests Automatisés avec pytest** | pytest obligatoire pour la logique applicative | **PASS** | Couverture pytest complète des modèles calendaires, de la persistance, des routes HTTP et des cas limites (bissextile, débordement de mois, sécurité). |
| **V. Minimalisme des Dépendances** | Uniquement Flask et pytest dans requirements.txt | **PASS** | Aucune nouvelle dépendance. Usage strict de la bibliothèque standard Python (`calendar`, `datetime`, `json`, `pathlib`, `dataclasses`) et des API natives du navigateur (`fetch`, `Date`). |
| **VI. Sécurité et Données Sensibles** | Zéro secret, gestion sûre des requêtes | **PASS** | Aucune donnée sensible ou clé d'API. Validation stricte des entrées (`year`, `month`, format ISO de date `YYYY-MM-DD`). |

## Project Structure

### Documentation (this feature)

```text
specs/006-calendar-date-picker/
├── spec.md              # Spécification fonctionnelle et critères d'acceptation
├── clarifications.md    # Clarifications techniques actées (persistance, toggle JSON, navigation)
├── plan.md              # Ce document (plan d'architecture et de mise en œuvre)
├── checklists/
│   └── requirements.md  # Checklist de conformité des exigences
└── tasks.md             # Décomposition ordonnée et exécutable des tâches (Phase 2)
```

### Source Code (repository root)

```text
app/
├── __init__.py          # Fabrique Flask : enregistrement de CALENDAR_DATA_FILE dans app.config
├── models.py            # CheckedDate, CalendarMonthInfo, CalendarManager (persistance calendar.json)
├── routes.py            # GET / (avec paramètres year/month), POST /calendar/toggle (JSON)
├── static/
│   ├── css/
│   │   └── style.css    # Styles de la section calendrier (.calendar-section, .calendar-grid, etc.)
│   └── js/
│       └── calendar.js  # Script Vanilla JS : toggle asynchrone, mise à jour optimiste, détection today locale
└── templates/
    └── index.html       # Bloc <section class="calendar-section"> et inclusion conditionnelle calendar.js

data/
├── tasks.json           # Stockage JSON des tâches (inchangé)
└── calendar.json        # Stockage JSON des dates cochées (nouveau fichier)

tests/
├── conftest.py          # Fixtures temp_calendar_storage_path et calendar_manager
├── test_models.py       # Tests unitaires pour CheckedDate et CalendarManager
└── test_routes.py       # Tests d'intégration Flask (GET /, navigation mois, POST /calendar/toggle, ARIA)
```

**Structure Decision**:
- L'isolation des données est garantie par un fichier `data/calendar.json` administré par `CalendarManager` dans `app/models.py`.
- Le calendrier est rendu dans `index.html` sous la liste des tâches (`.calendar-section`), assurant une intégration harmonieuse sans rupture visuelle.
- L'interaction temps réel (<150ms) s'appuie sur `POST /calendar/toggle` et `app/static/js/calendar.js`.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| *Aucune violation* | N/A | N/A |
