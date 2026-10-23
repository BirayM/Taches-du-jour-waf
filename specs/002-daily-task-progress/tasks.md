---
description: "Task list for Suivi de la Progression Quotidienne implementation"
---

# Tasks: Suivi de la Progression Quotidienne

**Input**: Design documents from `/specs/002-daily-task-progress/`
- Plan: [plan.md](plan.md)
- Specification: [spec.md](spec.md)
- Data Model: [data-model.md](data-model.md)
- Web Contracts: [contracts/web-routes.md](contracts/web-routes.md)
- Quickstart & Validation: [quickstart.md](quickstart.md)

**Constitution Guidelines**:
- Tests automatisés obligatoires avec `pytest` pour toute la logique Python (Principe IV).
- Flask comme unique dépendance backend, HTML5/CSS3 pur pour le frontend sans framework JS (Principe II).
- Minimalisme absolu des dépendances : uniquement `flask` et `pytest` dans `requirements.txt` (Principe V).
- Code lisible, explicite et commenté de manière didactique pour des apprenants (Principe III).

**Format**: `- [ ] [ID] [P?] [Story?] Description with file path`
- **[P]**: Tâche exécutable en parallèle (fichiers distincts, aucune dépendance non résolue).
- **[Story]**: Rattachement à une User Story (`[US1]`, `[US2]`, `[US3]`).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Validation de l'environnement de développement et des ressources statiques requises.

- [X] T001 Vérifier l'environnement virtuel et l'exécution initiale de la suite de tests avec `.venv/bin/pytest`
- [X] T002 [P] Vérifier la présence et la conformité de l'illustration vectorielle festive dans `app/static/images/dogs/dog-cheer.svg`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Modélisation métier et calcul des statistiques de progression requis avant le développement des interfaces.

**⚠️ CRITICAL**: Les user stories dépendent de ce socle fondamental de données.

- [X] T003 [P] Définir la dataclass `ProgressStats` dans `app/models.py` avec ses contraintes de validation : `total` ("nombre total de tâches planifiées pour la journée", `total >= 0`), `completed` ("nombre de tâches ayant le statut completed == True", `0 <= completed <= total`), `percentage` ("pourcentage de complétion arrondi à l'entier le plus proche (entre 0 et 100)", "si total == 0: percentage = 0", "si total > 0: percentage = round((completed / total) * 100)"), et `is_all_completed` ("strictement évalué à total > 0 and completed == total", "ne peut jamais valoir True si total == 0")
- [X] T004 Implémenter la méthode `get_progress()` au sein de `TaskManager` dans `app/models.py` retournant une instance de `ProgressStats` calculée à partir des tâches enregistrées

**Checkpoint**: Modèle et calcul de progression disponibles en mémoire - l'implémentation des user stories peut démarrer.

---

## Phase 3: User Story 1 - Affichage du compteur de tâches et de la barre de progression (Priority: P1) 🎯 MVP

**Goal**: Permettre à l'utilisateur de visualiser le nombre de tâches accomplies sur le total et d'observer une barre de progression graphique proportionnelle (0% à 100%) dès qu'au moins une tâche existe.

**Independent Test**: Planifier 4 tâches, en cocher 1 comme terminée. L'interface affiche immédiatement « 1 sur 4 tâche terminée (25%) » avec une barre de progression remplie à 25%. En cocher une seconde, vérifier l'avancement à « 2 sur 4 tâches terminées (50%) ».

### Tests pour User Story 1 ⚠️

> **Écrire les tests en premier et vérifier qu'ils échouent avant l'implémentation**

- [X] T005 [P] [US1] Écrire les tests unitaires pour `ProgressStats` et `TaskManager.get_progress()` (cas nominaux 1/4 = 25%, 2/4 = 50%, et calculs d'arrondis 1/3 = 33%, 2/3 = 67%) dans `tests/test_models.py`
- [X] T006 [P] [US1] Écrire les tests d'intégration HTTP pour la présence du compteur textuel "X sur Y" et de la barre de progression (`role="progressbar"`, `aria-valuenow`, `aria-valuemin="0"`, `aria-valuemax="100"`, largeur CSS en pourcentage) dans `tests/test_routes.py`

### Implementation pour User Story 1

- [X] T007 [US1] Injecter l'objet `progress` retourné par `manager.get_progress()` dans le contexte de rendu de la vue `index()` dans `app/routes.py`
- [X] T008 [US1] Intégrer la structure HTML5 accessible du composant de progression (`.progress-section`, `.progress-track` avec `role="progressbar"`, `.progress-fill`, `.progress-counter`) dans `app/templates/index.html`
- [X] T009 [P] [US1] Ajouter les styles CSS de la barre de progression (`.progress-section`, `.progress-track`, `.progress-fill` avec variables CSS `--color-primary`, border-radius et transition d'animation fluide) dans `app/static/css/style.css`

**Checkpoint**: User Story 1 pleinement fonctionnelle et testable de façon autonome (MVP atteint).

---

## Phase 4: User Story 2 - Message de félicitations spécial à l'achèvement complet (Priority: P2)

**Goal**: Féliciter chaleureusement l'utilisateur par une bannière spéciale et l'illustration festive `dog-cheer.svg` dès que 100% des tâches du jour sont accomplies.

**Independent Test**: Marquer toutes les tâches d'une liste comme terminées (ex: 3/3). Vérifier l'apparition de la bannière festive avec `dog-cheer.svg`. Ajouter ensuite une nouvelle tâche non terminée : vérifier que la progression redescend à 75% et que la bannière de célébration disparaît immédiatement.

### Tests pour User Story 2 ⚠️

- [X] T010 [P] [US2] Écrire les tests unitaires pour `is_all_completed == True` lorsque `total > 0 and completed == total`, et son retour à `False` lors de l'ajout d'une nouvelle tâche dans `tests/test_models.py`
- [X] T011 [P] [US2] Écrire les tests d'intégration HTTP vérifiant le rendu de la bannière de célébration (`.celebration-card`, image `dog-cheer.svg`, message festif) lors de la complétion à 100%, et sa disparition lors de l'ajout d'une tâche dans `tests/test_routes.py`

### Implementation pour User Story 2

- [X] T012 [US2] Intégrer la bannière de célébration conditionnelle (`{% if progress.is_all_completed %}`) affichant `dog-cheer.svg` et le message de félicitations dans `app/templates/index.html`
- [X] T013 [P] [US2] Ajouter les styles CSS pour la bannière de célébration (`.celebration-card`, disposition flexbox, cadre chaleureux, typographie festive) dans `app/static/css/style.css`

**Checkpoint**: User Stories 1 et 2 intégrées : suivi continu et récompense visuelle à 100%.

---

## Phase 5: User Story 3 - Prise en compte de l'état initial sans tâche (Priority: P3)

**Goal**: Garantir un comportement sobre, élégant et sans anomalie lorsque la liste des tâches est vide (0 tâche au total) : pas d'erreur de calcul arithmétique, pas de jauge inutile et pas de félicitations prématurées.

**Independent Test**: Lancer l'application avec un stockage vide (0 tâche). Vérifier que le message d'accueil avec `dog-resting.svg` est affiché, sans barre de progression encombrante et sans message de félicitations.

### Tests pour User Story 3 ⚠️

- [X] T014 [P] [US3] Écrire les tests unitaires pour la garde de division par zéro lorsque `total == 0` (`percentage == 0`, `is_all_completed == False`) dans `tests/test_models.py`
- [X] T015 [P] [US3] Écrire les tests d'intégration HTTP confirmant l'absence de la section de progression et des félicitations spéciales lorsque la liste des tâches est vide dans `tests/test_routes.py`

### Implementation pour User Story 3

- [X] T016 [US3] Conditionner l'affichage du bloc de progression (`{% if progress.total > 0 %}`) dans `app/templates/index.html` pour préserver l'état vide d'accueil d'origine

**Checkpoint**: Les 3 User Stories fonctionnent harmonieusement en couvrant tous les états de l'application.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Qualité pédagogique du code, documentation didactique et validation finale exhaustive.

- [X] T017 [P] Ajouter des docstrings complètes (PEP 257) et des commentaires pédagogiques expliquant les règles arithmétiques, de garde et d'accessibilité dans `app/models.py`, `app/routes.py` et `app/static/css/style.css`
- [X] T018 Exécuter l'intégralité de la suite de tests automatisés `pytest -v` via `.venv/bin/pytest` et confirmer un statut vert à 100%
- [X] T019 Dérouler manuellement l'ensemble des 6 scénarios de validation de bout en bout décrits dans `specs/002-daily-task-progress/quickstart.md`
- [X] T020 [P] Mettre à jour la documentation du projet dans `README.md` pour présenter le suivi de la progression quotidienne et la célébration canine

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)** : Aucune dépendance - peut démarrer immédiatement.
- **Foundational (Phase 2)** : Dépend de la Phase 1 - BLOQUE toutes les User Stories.
- **User Stories (Phases 3 à 5)** : Dépendent de la complétion de la Phase 2 (Foundational).
  - Priorité séquentielle recommandée : US1 (P1) → US2 (P2) → US3 (P3).
- **Polish (Phase 6)** : Dépend de la réalisation des User Stories.

### User Story Dependencies

- **User Story 1 (P1)** : Dépend de la Phase 2. Aucune dépendance sur US2 ou US3 (MVP autonome).
- **User Story 2 (P2)** : Dépend de la Phase 2 et s'intègre sur le template enrichi par US1.
- **User Story 3 (P3)** : Dépend de la Phase 2 et affine la condition d'affichage introduite par US1.

### Within Each User Story

1. Les tests TDD automatisés (`tests/test_models.py`, `tests/test_routes.py`) DOIVENT être rédigés en premier et échouer.
2. Modélisation et logique backend dans `app/models.py` et `app/routes.py`.
3. Gabarits et rendu frontend dans `app/templates/index.html`.
4. Styles CSS associés dans `app/static/css/style.css`.
5. Validation que les tests passent au vert avant de passer à la story suivante.

### Parallel Opportunities

- Les tâches marquées `[P]` portent sur des fichiers distincts et peuvent être exécutées en parallèle :
  - **Phase 1** : T002 en parallèle de T001.
  - **Phase 2** : T003 en parallèle de T004.
  - **Phase 3 (US1)** : T005 et T006 (tests) en parallèle ; T009 (CSS) en parallèle de T007/T008.
  - **Phase 4 (US2)** : T010 et T011 (tests) en parallèle ; T013 (CSS) en parallèle de T012.
  - **Phase 5 (US3)** : T014 et T015 (tests) en parallèle.
  - **Phase 6 (Polish)** : T017 et T020 en parallèle.

---

## Parallel Example: User Story 1

```bash
# Lancement simultané de la rédaction des tests unitaire et d'intégration :
Task: "T005 [P] [US1] Écrire les tests unitaires pour ProgressStats et TaskManager.get_progress() dans tests/test_models.py"
Task: "T006 [P] [US1] Écrire les tests d'intégration HTTP pour la barre de progression dans tests/test_routes.py"

# En parallèle de l'intégration template, préparation des styles CSS :
Task: "T009 [P] [US1] Ajouter les styles CSS de la barre de progression dans app/static/css/style.css"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Réaliser la Phase 1 (Setup) et la Phase 2 (Foundational).
2. Réaliser la Phase 3 (User Story 1).
3. **STOP et VALIDATION** : Vérifier que le compteur et la barre de progression fonctionnent de façon autonome.
4. L'application dispose déjà de sa valeur clé : le suivi visuel chiffré et graphique de l'avancement.

### Incremental Delivery

1. **Incrément 1 (MVP)** : Suivi chiffré et jauge de progression (US1).
2. **Incrément 2** : Bannière festive de célébration à 100% avec `dog-cheer.svg` (US2).
3. **Incrément 3** : Encadrement sobre de l'état sans tâche sans fausse célébration (US3).
4. **Incrément 4** : Documentation didactique et validation globale de bout en bout (Polish).
