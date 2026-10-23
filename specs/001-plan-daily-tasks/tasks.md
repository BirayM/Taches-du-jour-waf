---
description: "Task list for Planification des Tâches du Jour implementation"
---

# Tasks: Planification des Tâches du Jour

**Input**: Design documents from `/specs/001-plan-daily-tasks/`
- Plan: [plan.md](plan.md)
- Specification: [spec.md](spec.md)
- Data Model: [data-model.md](data-model.md)
- Web Contracts: [contracts/web-routes.md](contracts/web-routes.md)
- Quickstart & Validation: [quickstart.md](quickstart.md)

**Constitution Guidelines**:
- Tests automatisés obligatoires avec `pytest` pour toute la logique Python (Principe IV).
- Flask comme unique dépendance backend, HTML5/CSS3 pur pour le frontend (Principe II).
- Minimalisme absolu des dépendances : uniquement `flask` et `pytest` dans `requirements.txt` (Principe V).
- Code lisible, explicite et commenté de manière didactique (Principe III).

**Format**: `- [ ] [ID] [P?] [Story?] Description with file path`
- **[P]**: Tâche exécutable en parallèle (fichiers distincts, aucune dépendance non résolue).
- **[Story]**: Rattachement à une User Story (`[US1]`, `[US2]`, `[US3]`).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialisation du projet et mise en place de la structure de base.

- [X] T001 Créer l'arborescence du projet (`app/`, `app/static/css/`, `app/static/images/dogs/`, `app/templates/`, `data/`, `tests/`) conformément au plan d'architecture
- [X] T002 [P] Déclarer les dépendances autorisées (`flask>=3.0.0`, `pytest>=8.0.0`) dans `requirements.txt`
- [X] T003 [P] Configurer les exclusions de fichiers temporaires, caches Python/pytest et environnements virtuels dans `.gitignore`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Socle applicatif et persistance requis avant le développement des user stories.

**⚠️ CRITICAL**: Les user stories dépendent de ce socle fondamental.

- [X] T004 [P] Implémenter le modèle `Task` et le gestionnaire de stockage JSON dans `app/models.py` avec validation stricte : `id` ("identifiant unique non modifiable"), `title` ("DOIT PAS être vide après suppression des espaces", "longueur DOIT être comprise entre 1 et 200 caractères"), `completed` ("booléen strict", défaut `False`), `created_at` (horodatage ISO 8601), et initialisation automatique de `data/tasks.json` avec `[]` si absent
- [X] T005 [P] Implémenter la collection de citations positives et canines avec fonction de tirage aléatoire (`random.choice`) dans `app/quotes.py`
- [X] T006 Implémenter la fabrique applicative Flask `create_app()` dans `app/__init__.py` en configurant les dossiers de templates et de fichiers statiques
- [X] T007 [P] Créer le script d'exécution du serveur local de développement dans `run.py`
- [X] T008 [P] Configurer les fixtures pytest d'isolation (client de test Flask et stockage temporaire avec `tmp_path`) dans `tests/conftest.py`

**Checkpoint**: Socle prêt - l'implémentation des user stories peut démarrer.

---

## Phase 3: User Story 1 - Saisie et enchaînement d'ajout de tâches (Priority: P1) 🎯 MVP

**Goal**: Permettre à l'utilisateur d'entrer l'intitulé d'une tâche dans un formulaire, de valider l'enregistrement et de réinitialiser immédiatement le champ pour saisir la tâche suivante sans friction.

**Independent Test**: Accéder à `http://localhost:5000/`, soumettre "Préparer le cours de programmation", vérifier que la tâche est persistée et que le champ est réinitialisé et prêt pour une nouvelle entrée. Soumettre un champ vide et vérifier le blocage avec message d'erreur.

### Tests pour User Story 1 ⚠️

> **Écrire les tests en premier et vérifier qu'ils échouent avant l'implémentation**

- [X] T009 [P] [US1] Écrire les tests unitaires pour la validation et l'instanciation de `Task` (`title.strip() != ""`, `1 <= len(title) <= 200`) dans `tests/test_models.py`
- [X] T010 [P] [US1] Écrire les tests d'intégration pour la route `POST /tasks` (redirection 302 vers `/`, rejet des entrées vides, échappement des caractères spéciaux) dans `tests/test_routes.py`

### Implementation pour User Story 1

- [X] T011 [US1] Créer le gabarit de base HTML5 sémantique avec blocs de contenu et viewport responsive dans `app/templates/base.html`
- [X] T012 [US1] Créer le formulaire de saisie de tâche (champ texte avec autofocus, bouton de soumission et zone d'alerte d'erreur) dans `app/templates/index.html`
- [X] T013 [US1] Implémenter le contrôleur de route `POST /tasks` dans `app/routes.py` appliquant le patron Post/Redirect/Get (validation, création de `Task`, persistance JSON et redirection 302 vers `/`)

**Checkpoint**: User Story 1 fonctionnelle et testable de façon autonome (MVP atteint).

---

## Phase 4: User Story 2 - Affichage de la liste des tâches, suivi et message de motivation (Priority: P2)

**Goal**: Afficher les tâches saisies sous forme de liste claire et ordonnée, permettre de cocher une tâche comme terminée (mise à jour d'état) et afficher une citation bienveillante et canine aléatoire.

**Independent Test**: Ajouter plusieurs tâches, vérifier leur affichage ordonné avec une citation canine, cocher une tâche pour la marquer terminée et vérifier la persistance de l'état après redémarrage simulé.

### Tests pour User Story 2 ⚠️

- [X] T014 [P] [US2] Écrire les tests unitaires pour le passage à l'état `completed = True` et la recharge fidèle du fichier JSON dans `tests/test_models.py`
- [X] T015 [P] [US2] Écrire les tests d'intégration pour la route `GET /` (restitution ordonnée des tâches, présence d'une citation) et la route `POST /tasks/<id>/complete` dans `tests/test_routes.py`

### Implementation pour User Story 2

- [X] T016 [US2] Implémenter le contrôleur de route `POST /tasks/<id>/complete` et finaliser `GET /` dans `app/routes.py` pour transmettre la liste ordonnée des tâches et une citation aléatoire au template
- [X] T017 [US2] Enrichir `app/templates/index.html` pour afficher la liste des tâches avec indicateur d'état (case à cocher/bouton de complétion), l'état vide convivial quand aucune tâche n'existe, et la bannière de citation motivante

**Checkpoint**: User Stories 1 et 2 pleinement fonctionnelles et persistées.

---

## Phase 5: User Story 3 - Expérience visuelle chaleureuse avec illustrations canines (Priority: P3)

**Goal**: Offrir une ambiance graphique réconfortante, chaleureuse et déstressante avec une charte aux tons doux et des illustrations de chiens intégrées dans l'interface.

**Independent Test**: Vérifier visuellement l'application : palette de couleurs chaleureuses, typographie accueillante, illustration canine d'accueil, chien au repos pour l'état vide, et chien enthousiaste pour la liste active.

### Implementation pour User Story 3

- [X] T018 [P] [US3] Créer les illustrations vectorielles SVG canines locales (chien amical pour l'en-tête, chiot au repos pour l'état vide, chien encourageant pour les tâches) dans `app/static/images/dogs/`
- [X] T019 [P] [US3] Rédiger la feuille de style CSS3 moderne en CSS pur (variables CSS `--color-warm-bg`, `--color-primary`, mise en page flexbox/grid fluide) dans `app/static/css/style.css`
- [X] T020 [US3] Lier les styles et intégrer harmonieusement les illustrations canines dans `app/templates/base.html` et `app/templates/index.html`

**Checkpoint**: Les 3 User Stories sont intégrées dans une interface complète et soignée.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Qualité pédagogique, finitions, documentation et validation finale.

- [X] T021 [P] Ajouter des docstrings complètes (PEP 257) et des commentaires pédagogiques détaillés dans `app/models.py`, `app/routes.py` et `app/quotes.py`
- [X] T022 Exécuter l'ensemble de la suite de tests `pytest -v` et dérouler tous les scénarios de validation manuelle décrits dans `specs/001-plan-daily-tasks/quickstart.md`
- [X] T023 [P] Rédiger le fichier `README.md` à la racine avec présentation du projet pédagogique, prérequis et instructions de démarrage

---

## Dependencies & Execution Order

### Phase Dependencies

```text
Phase 1: Setup
     │
     ▼
Phase 2: Foundational (Models, Quotes, App Factory, Pytest Fixtures)
     │
     ▼
Phase 3: User Story 1 (P1 - MVP : Formulaire & Ajout)
     │
     ▼
Phase 4: User Story 2 (P2 : Liste, Complétion & Citations)
     │
     ▼
Phase 5: User Story 3 (P3 : Thème Chaleureux & Illustrations SVG)
     │
     ▼
Phase 6: Polish (Docstrings, Tests complets, README)
```

### User Story Dependencies

- **User Story 1 (P1)** : Dépend uniquement de la Phase 2 (Foundational). Constitue le MVP.
- **User Story 2 (P2)** : Dépend de la Phase 2 et s'appuie sur la structure de template initiée en US1.
- **User Story 3 (P3)** : Dépend de la structure HTML des US1/US2 pour appliquer les styles et intégrer les SVG.
- **Polish (Phase 6)** : Dépend de l'achèvement des 3 User Stories.

### Parallel Opportunities

- **En Phase 1** : `T002` (`requirements.txt`) et `T003` (`.gitignore`) peuvent être menés en parallèle.
- **En Phase 2** : `T004` (`models.py`), `T005` (`quotes.py`), `T007` (`run.py`) et `T008` (`conftest.py`) peuvent être développés en parallèle.
- **En Phase 3 (US1)** : Les tests `T009` et `T010` peuvent être écrits en parallèle avant l'implémentation.
- **En Phase 4 (US2)** : Les tests `T014` et `T015` peuvent être écrits en parallèle.
- **En Phase 5 (US3)** : La création des assets SVG (`T018`) et la rédaction du CSS (`T019`) peuvent se faire en parallèle.
- **En Phase 6** : La documentation du code (`T021`) et le `README.md` (`T023`) peuvent être réalisés en parallèle.

---

## Parallel Example: User Story 1

```bash
# Écriture parallèle des tests pour US1 :
Task T009: "tests/test_models.py (tests unitaires de validation Task)"
Task T010: "tests/test_routes.py (tests d'intégration POST /tasks)"

# Après écriture des tests, préparation des templates :
Task T011: "app/templates/base.html"
Task T012: "app/templates/index.html"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Réaliser la Phase 1 (Setup) et la Phase 2 (Foundational).
2. Implémenter la Phase 3 (User Story 1 avec ses tests).
3. **Valider le MVP** : Vérifier que l'utilisateur peut saisir et enchaîner des tâches avec persistance JSON fonctionnelle.

### Incremental Delivery
1. Valider le MVP (US1).
2. Déployer US2 : Liste visuelle, cochage de tâche terminée et message motivant.
3. Déployer US3 : Habillage graphique chaleureux et illustrations canines.
4. Finaliser la Phase 6 : Documentation pédagogique et validation complète avec `pytest`.
