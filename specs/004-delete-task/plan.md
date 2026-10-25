# Implementation Plan: Suppression de Tâche Individuelle

**Branch**: `004-delete-task` | **Date**: 2026-10-24 | **Spec**: [specs/004-delete-task/spec.md](spec.md)

**Input**: Feature specification from `/specs/004-delete-task/spec.md`

## Summary

Cette fonctionnalité permet à tout utilisateur de supprimer définitivement une tâche individuelle de sa liste quotidienne :
1. Ajout d'une action de suppression accessible sur chaque carte de tâche (`POST /tasks/<task_id>/delete`) appliquant le patron Post/Redirect/Get (PRG) vers `/`.
2. Persistance locale mise à jour via la méthode `delete_task` de `TaskManager` dans `app/models.py`.
3. Recalcul instantané du compteur et de la jauge de progression (`ProgressStats`), avec retour automatique à l'état vide d'accueil (`dog-resting.svg`) si la dernière tâche est supprimée, ou activation de la bannière de célébration (`dog-cheer.svg`) si le taux atteint 100%.
4. Accessibilité complète au clavier et pour les lecteurs d'écran via un bouton natif doté d'un attribut `aria-label="Supprimer la tâche : {titre}"`.
5. Résilience et idempotence : redirection silencieuse 302 sans erreur 500 en cas d'identifiant introuvable ou de double-clic, et interdiction stricte de la méthode GET (HTTP 405).
6. Respect rigoureux de la Constitution : HTML/CSS natif, aucune dépendance externe additionnelle, et couverture exhaustive par des tests automatisés `pytest`.

## Technical Context

**Language/Version**: Python 3.10+ (typé avec annotations de type PEP 484)

**Primary Dependencies**: Flask (unique framework web backend autorisé par la constitution)

**Storage**: Fichier JSON local (`data/tasks.json`) manipulé de manière synchrone via le module standard `json`

**Testing**: `pytest` pour les tests unitaires (`test_models.py`) et les tests d'intégration HTTP (`test_routes.py`) via `app.test_client()`

**Target Platform**: Multiplateforme (Linux, macOS, Windows), exécution locale

**Project Type**: Application web locale en rendu côté serveur (SSR) sans framework JavaScript

**Performance Goals**: Temps de réponse local < 100ms, recalcul synchrone immédiat lors de la redirection

**Constraints**: Zéro framework JavaScript (formulaires HTML natifs uniquement), accessibilité WAI-ARIA (`aria-label` explicite, focalisation clavier), patron Post/Redirect/Get strict, méthode GET rejetée par HTTP 405

**Scale/Scope**: Application mono-utilisateur locale pour le suivi quotidien (0 à 50 tâches par session)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principe Constitutionnel | Exigence | Statut | Justification de Conformité |
|--------------------------|----------|--------|-----------------------------|
| **I. Simplicité et Vocation Pédagogique** | Architecture didactique, KISS / YAGNI | **PASS** | Formulaire HTML standard par tâche, méthode de suppression synchrone directe dans `TaskManager`, aucun concept abstrait superflu (pas de corbeille, pas de soft-delete, pas de confirmation complexe). |
| **II. Stack Web Épurée (HTML/CSS & Flask)** | HTML5/CSS3 natif, Flask unique dépendance backend | **PASS** | Déclenchement de la suppression par formulaire natif `<form method="POST">` avec bouton `<button type="submit">`. Zéro JavaScript. Traitement par route Flask standard et redirection 302 (SSR / PRG). |
| **III. Lisibilité et Documentation** | Code commenté, docstrings PEP 257 | **PASS** | Docstrings complètes pour la vue `delete_task`, explications pédagogiques du patron PRG et du rôle de l'attribut `aria-label` pour l'accessibilité. |
| **IV. Tests Automatisés avec pytest** | pytest obligatoire pour la logique Python | **PASS** | Suite de tests automatisés couvrant le cas nominal, la suppression de la dernière tâche, la transition vers 100%, la résilience face à un ID inconnu, et le rejet de la méthode GET (405). |
| **V. Minimalisme des Dépendances** | Uniquement Flask et pytest dans requirements.txt | **PASS** | Aucune nouvelle dépendance. Utilisation exclusive de Flask et de la bibliothèque standard Python (`uuid`, `json`, `pathlib`). |
| **VI. Sécurité et Données Sensibles** | Zéro secret, gestion sûre des requêtes | **PASS** | Action destructrice réservée à la méthode POST (protection contre préchargement/crawlers), aucune donnée sensible manipulée. |

## Project Structure

### Documentation (this feature)

```text
specs/004-delete-task/
├── spec.md              # Spécification fonctionnelle et critères d'acceptation
├── clarifications.md    # Clarifications techniques actées (routes, erreurs, ARIA)
├── plan.md              # Ce document (plan d'architecture et de mise en œuvre)
├── research.md          # Recherches et décisions techniques validées (Phase 0)
├── data-model.md        # Modèles de données et matrices de transition (Phase 1)
├── quickstart.md        # Guide de démarrage et scénarios de validation (Phase 1)
├── contracts/           # Contrats d'interfaces
│   └── web-routes.md    # Contrat d'endpoint HTTP et fragments Jinja2/CSS (Phase 1)
└── checklists/
    └── requirements.md  # Checklist de conformité des exigences
```

### Source Code (repository root)

```text
app/
├── __init__.py          # Usine logicielle Flask (create_app)
├── models.py            # TaskManager.delete_task() et recalcul dynamique de ProgressStats
├── routes.py            # Définition de la route POST /tasks/<task_id>/delete
├── quotes.py            # Citations de motivation et d'accueil
├── static/
│   ├── css/
│   │   └── style.css    # Styles CSS pour le bouton de suppression (.btn-delete) et actions
│   └── images/
│       └── dogs/
│           ├── dog-cheer.svg    # Illustration festive activée si le taux passe à 100%
│           ├── dog-happy.svg    # Illustration d'accompagnement
│           └── dog-resting.svg  # Illustration réactivée si la dernière tâche est supprimée
└── templates/
    ├── base.html        # Gabarit structurel HTML5
    └── index.html       # Intégration du formulaire de suppression et de l'aria-label

data/
└── tasks.json           # Stockage JSON des tâches (mis à jour par TaskManager)

tests/
├── conftest.py          # Fixtures de test pytest (client Flask, stockage temporaire)
├── test_models.py       # Tests unitaires de TaskManager.delete_task et ProgressStats
└── test_routes.py       # Tests d'intégration HTTP (PRG, 405, état vide, accessibilité)
```

**Structure Decision**: La logique de manipulation des données est centralisée dans `TaskManager.delete_task` (`app/models.py`), retournant un booléen de succès. La route `POST /tasks/<task_id>/delete` dans `app/routes.py` orchestre la suppression et la redirection 302 vers l'index (`/`), garantissant le patron PRG. Le template `app/templates/index.html` intègre le bouton d'action avec son attribut d'accessibilité ARIA, stylisé par `app/static/css/style.css`.

## Complexity Tracking

> Aucune violation constitutionnelle. Toutes les directives (KISS, SSR Flask, CSS pur, pytest non-négociable, zéro dépendance) sont strictement satisfaites.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| *Aucune* | - | - |
