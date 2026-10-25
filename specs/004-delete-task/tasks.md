---
description: "Task list for Suppression de Tâche Individuelle implementation"
---

# Tasks: Suppression de Tâche Individuelle

**Input**: Design documents from `/specs/004-delete-task/`
- Plan: [plan.md](plan.md)
- Specification: [spec.md](spec.md)
- Data Model: [data-model.md](data-model.md)
- Web Contracts: [contracts/web-routes.md](contracts/web-routes.md)
- Research: [research.md](research.md)
- Quickstart & Validation: [quickstart.md](quickstart.md)
- Clarifications: [clarifications.md](clarifications.md)

**Constitution Guidelines**:
- Tests automatisés obligatoires avec `pytest` pour toute la logique Python (Principe IV).
- Flask comme unique dépendance backend, HTML5/CSS3 pur pour le frontend sans framework JS (Principe II).
- Minimalisme absolu des dépendances : uniquement `flask` et `pytest` dans `requirements.txt` (Principe V).
- Code lisible, auto-porteur et commenté de manière didactique pour des apprenants (Principe III).

**Format**: `- [ ] [ID] [P?] [Story?] Description with file path`
- **[P]**: Tâche exécutable en parallèle (fichiers distincts, aucune dépendance non résolue).
- **[Story]**: Rattachement à une User Story (`[US1]`, `[US2]`, `[US3]`). Absent pour Setup, Foundational et Polish.
- **TDD (Test-First)** : Les tâches de tests sont systématiquement positionnées avant les tâches de code correspondantes.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Validation de l'environnement de développement et vérification des ressources statiques requises.

- [X] T001 Vérifier l'environnement virtuel et l'exécution initiale de la suite de tests existante avec `.venv/bin/pytest`
- [X] T002 [P] Vérifier la présence des illustrations vectorielles canines requises dans `app/static/images/dogs/dog-resting.svg` et `app/static/images/dogs/dog-cheer.svg`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Socle fondamental de données et méthode de persistance de suppression requises avant le développement des routes et des interfaces.

**⚠️ CRITICAL**: Les user stories dépendent de ce socle fondamental de persistance.

- [X] T003 [P] Écrire les tests unitaires pour la suppression de tâche dans `tests/test_models.py` (vérification de la suppression physique dans le fichier JSON, intégrité des tâches restantes, et retour `False` sans exception pour un identifiant inexistant)
- [X] T004 Valider et documenter l'implémentation de la méthode `delete_task(task_id: str) -> bool` au sein de `TaskManager` dans `app/models.py` conformément aux contraintes de `data-model.md` : argument `task_id` ("Identifiant unique de la tâche à supprimer"), retour `bool` ("True si la tâche a été trouvée et supprimée, False si elle n'existait pas"), "La tâche est retirée de la liste en mémoire. La nouvelle liste est sérialisée dans data/tasks.json avec indentation standard. La fonction retourne True", "Si task_id ne correspond à aucune tâche (inconnu, déjà supprimé, chaîne vide) : Aucun accès en écriture n'est effectué sur le fichier de persistance. La fonction retourne False sans lever d'exception", et cycle de destruction physique ("retirée sans archivage intermédiaire, sans corbeille (recycle bin) et sans possibilité d'annulation (undo)")

**Checkpoint**: Persistance validée au niveau modèle avec tests au vert - l'implémentation des user stories peut débuter.

---

## Phase 3: User Story 1 - Suppression ciblée d'une tâche et mise à jour du tableau de bord (Priority: P1) 🎯 MVP

**Goal**: Permettre à l'utilisateur de supprimer définitivement une tâche individuelle de sa liste quotidienne, recalculer immédiatement le compteur ("X sur Y") et la barre de progression (0% à 100%), et garantir le patron Post/Redirect/Get (PRG) vers `/`.

**Independent Test**: Créer deux tâches (dont une terminée), cliquer sur le bouton de suppression de la tâche non terminée. La tâche ciblée disparaît immédiatement de la liste, le compteur passe à 1 sur 1 (100%), la barre de progression s'ajuste à 100% avec déclenchement de la célébration festive, et un rafraîchissement ultérieur de la page (F5) ne génère aucune invite de renvoi de données.

### Tests pour User Story 1 ⚠️

> **NOTE: Écrire ces tests en premier et vérifier qu'ils échouent avant l'implémentation**

- [X] T005 [P] [US1] Écrire les tests unitaires de recalcul des statistiques de progression `ProgressStats` post-suppression dans `tests/test_models.py` selon `data-model.md` : `total` ("décrémenté de 1 si la suppression réussit"), `completed` ("décrémenté de 1 si la tâche supprimée était terminée"), `percentage` ("round((completed / total) * 100) si total > 0, sinon 0"), et `is_all_completed` ("True si et seulement si total > 0 et completed == total")
- [X] T006 [P] [US1] Écrire les tests de contrat et d'intégration HTTP pour la route `POST /tasks/<task_id>/delete` dans `tests/test_routes.py` (vérification de la redirection 302 Found avec en-tête `Location: /` selon le patron PRG, retrait effectif de la tâche dans le rendu HTML, actualisation du compteur "1 sur 2" et de la jauge à 50%, résilience face à un identifiant inconnu redirigeant en 302 sans erreur 500, et rejet des requêtes GET par le code HTTP 405 Method Not Allowed)
- [X] T007 [P] [US1] Écrire le test d'intégration HTTP pour la transition vers 100% de complétion lors de la suppression d'une tâche non terminée dans `tests/test_routes.py` (vérification de l'activation de `.celebration-card` et de l'illustration `dog-cheer.svg` lorsque toutes les tâches restantes sont terminées)

### Implementation pour User Story 1

- [X] T008 [US1] Implémenter le point d'accès HTTP `POST /tasks/<task_id>/delete` dans `app/routes.py` restreint strictement à la méthode POST (`methods=["POST"]`), orchestrant l'appel à `manager.delete_task(task_id)` et la redirection PRG `return redirect(url_for("main.index"))` sans message flash superflu
- [X] T009 [US1] Intégrer le formulaire de suppression HTML5 `<form action="{{ url_for('main.delete_task', task_id=task.id) }}" method="POST" class="delete-form">` avec son bouton `<button type="submit" class="btn-delete">` au sein de chaque élément `<li class="task-item">` dans `app/templates/index.html`
- [X] T010 [P] [US1] Ajouter les déclarations CSS pour le groupe d'actions `.task-actions`, le formulaire `.delete-form` et le bouton `.btn-delete` (disposition flexbox, réinitialisation des styles de bouton natif, transition fluide et survol `:hover` en rouge clair) dans `app/static/css/style.css`

**Checkpoint**: User Story 1 pleinement fonctionnelle et testable de façon autonome (MVP atteint).

---

## Phase 4: User Story 2 - Retour automatique à l'état vide d'accueil lors de la suppression de la dernière tâche (Priority: P2)

**Goal**: Assurer un retour propre et immédiat à l'état d'accueil initial (illustration `dog-resting.svg`, message d'accueil et masquage complet de la barre de progression et du compteur) lorsque l'utilisateur supprime la dernière tâche restante.

**Independent Test**: Disposer d'une seule tâche dans l'application, cliquer sur son bouton de suppression. L'application réaffiche l'écran initial avec l'illustration canine au repos et le message invitant à planifier une première tâche, sans barre de progression orpheline ni compteur résiduel.

### Tests pour User Story 2 ⚠️

> **NOTE: Écrire ces tests en premier et vérifier qu'ils échouent avant l'implémentation**

- [X] T011 [P] [US2] Écrire le test unitaire pour la remise à zéro de `ProgressStats` lors de la suppression de la dernière tâche dans `tests/test_models.py` (vérification que `total=0`, `completed=0`, `percentage=0`, et `is_all_completed=False`)
- [X] T012 [P] [US2] Écrire le test d'intégration HTTP pour la suppression de la dernière tâche dans `tests/test_routes.py` (vérification de la présence de `dog-resting.svg`, du titre `Aucune tâche pour l'instant !`, de la citation `WELCOME_QUOTE`, et de l'absence complète des éléments `.progress-section` et `.celebration-card`)

### Implementation pour User Story 2

- [X] T013 [US2] Adapter et sécuriser les conditions d'affichage Jinja2 dans `app/templates/index.html` pour garantir le masquage immédiat de `.progress-section` (`{% if progress and progress.total > 0 %}`) et la réapparition fluide du bloc `.empty-state` avec `dog-resting.svg` et la citation d'accueil lorsque `tasks` est vide suite à une suppression

**Checkpoint**: User Stories 1 et 2 intégrées et fonctionnelles sans état intermédiaire incohérent.

---

## Phase 5: User Story 3 - Accessibilité du bouton de suppression (Priority: P3)

**Goal**: Offrir une accessibilité numérique complète au bouton de suppression pour les utilisateurs naviguant au clavier ou utilisant un lecteur d'écran (focalisation séquentielle, libellé `aria-label` individualisé, opérabilité permanente y compris sur les tâches complétées).

**Independent Test**: Utiliser exclusivement la touche Tabulation pour atteindre le bouton de suppression d'une tâche nommée "Sortir le chien", vérifier la présence d'un libellé vocal explicite "Supprimer la tâche : Sortir le chien", et déclencher la suppression avec la touche Entrée ou Espace. Vérifier également la présence active du bouton sur une tâche marquée comme terminée.

### Tests pour User Story 3 ⚠️

> **NOTE: Écrire ces tests en premier et vérifier qu'ils échouent avant l'implémentation**

- [X] T014 [P] [US3] Écrire les tests d'intégration HTTP vérifiant la présence et la conformité des attributs d'accessibilité du bouton de suppression dans `tests/test_routes.py` (vérification de `aria-label="Supprimer la tâche : {titre}"`, de l'infobulle `title="Supprimer la tâche : {titre}"`, et de la balise `<span class="delete-icon" aria-hidden="true">🗑️</span>`)
- [X] T015 [P] [US3] Écrire le test d'intégration HTTP vérifiant que le bouton de suppression reste actif sans attribut `disabled` sur une tâche déjà complétée (`task.completed == True`, classe `.is-completed`) et permet sa suppression avec recalcul exact du ratio dans `tests/test_routes.py`

### Implementation pour User Story 3

- [X] T016 [US3] Mettre en conformité les attributs d'accessibilité du bouton de suppression dans `app/templates/index.html` selon `data-model.md` : liaison dynamique avec `task.title` ("Intitulé descriptif (1 à 200 caractères), utilisé pour composer le libellé accessible aria-label"), attributs `aria-label="Supprimer la tâche : {{ task.title }}"` et `title="Supprimer la tâche : {{ task.title }}"`, icône masquée aux technologies d'assistance via `<span class="delete-icon" aria-hidden="true">🗑️</span>`, et absence stricte d'attribut `disabled` quel que soit l'état `completed`
- [X] T017 [P] [US3] Ajouter les règles CSS de focalisation accessible au clavier pour le bouton de suppression (`.btn-delete:focus-visible` avec contour visible `2px solid var(--color-primary, #4f46e5)` et décalage `outline-offset: 2px`) dans `app/static/css/style.css`

**Checkpoint**: Toutes les User Stories (US1, US2, US3) sont complètes, accessibles et couvertes par les tests automatisés.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Qualité didactique du code, documentation pédagogique et validation exhaustive de la solution.

- [X] T018 [P] Ajouter des docstrings complètes (PEP 257) et des commentaires pédagogiques sur le patron PRG, l'idempotence et l'accessibilité WAI-ARIA dans `app/models.py`, `app/routes.py`, `app/templates/index.html` et `app/static/css/style.css`
- [X] T019 Exécuter l'intégralité de la suite de tests automatisés `pytest -v` via `.venv/bin/pytest` et confirmer un taux de réussite de 100%
- [X] T020 Dérouler manuellement l'ensemble des 6 scénarios de validation de bout en bout décrits dans `specs/004-delete-task/quickstart.md`
- [X] T021 [P] Mettre à jour la documentation du projet dans `README.md` pour documenter la suppression individuelle de tâche, la route `POST /tasks/<task_id>/delete` et les critères d'accessibilité associés

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)** : Aucune dépendance - peut démarrer immédiatement.
- **Foundational (Phase 2)** : Dépend de la Phase 1 - BLOQUE toutes les User Stories.
- **User Stories (Phases 3 à 5)** : Dépendent de la complétion de la Phase 2 (Foundational).
  - Priorité séquentielle recommandée : US1 (P1) → US2 (P2) → US3 (P3).
- **Polish (Phase 6)** : Dépend de la réalisation de l'ensemble des User Stories souhaitées.

### User Story Dependencies

- **User Story 1 (P1)** : Dépend de la Phase 2. Aucune dépendance sur US2 ou US3 (MVP autonome).
- **User Story 2 (P2)** : Dépend de la Phase 2 et s'appuie sur le mécanisme de suppression et le rendu de liste introduits par US1.
- **User Story 3 (P3)** : Dépend de la Phase 2 et complète l'accessibilité ARIA et CSS du bouton introduit par US1.

### Within Each User Story

1. Les tests TDD automatisés (`tests/test_models.py`, `tests/test_routes.py`) DOIVENT être rédigés en premier et échouer avant toute écriture de code applicatif.
2. Évolution ou validation du modèle dans `app/models.py`.
3. Routage HTTP et contrôleurs dans `app/routes.py`.
4. Rendu de gabarit dans `app/templates/index.html`.
5. Stylisation CSS dans `app/static/css/style.css`.
6. Validation du retour au vert des tests avant de passer à la story ou phase suivante.

### Parallel Opportunities

- Les tâches marquées `[P]` portent sur des fichiers distincts et peuvent être exécutées en parallèle :
  - **Phase 1** : T002 en parallèle de T001.
  - **Phase 2** : T003 (tests) en parallèle de T001/T002 avant T004.
  - **Phase 3 (US1)** : T005, T006 et T007 (tests) peuvent être rédigés en parallèle ; T010 (CSS) peut être réalisé en parallèle de T008 et T009.
  - **Phase 4 (US2)** : T011 et T012 (tests) peuvent être rédigés en parallèle.
  - **Phase 5 (US3)** : T014 et T015 (tests) peuvent être rédigés en parallèle ; T017 (CSS) en parallèle de T016 (HTML).
  - **Phase 6 (Polish)** : T018 et T021 en parallèle.

---

## Parallel Example: User Story 1

```bash
# Rédaction simultanée des tests unitaires et d'intégration HTTP pour US1 :
Task: "T005 [P] [US1] Écrire les tests unitaires de recalcul des statistiques ProgressStats post-suppression dans tests/test_models.py"
Task: "T006 [P] [US1] Écrire les tests de contrat et d'intégration HTTP pour la route POST /tasks/<task_id>/delete dans tests/test_routes.py"
Task: "T007 [P] [US1] Écrire le test d'intégration HTTP pour la transition vers 100% de complétion dans tests/test_routes.py"

# En parallèle de l'intégration template, préparation des styles CSS :
Task: "T010 [P] [US1] Ajouter les déclarations CSS pour le groupe d'actions et le bouton de suppression dans app/static/css/style.css"
```

---

## Parallel Example: User Story 2

```bash
# Rédaction simultanée des tests unitaires et d'intégration pour le retour à l'état vide :
Task: "T011 [P] [US2] Écrire le test unitaire pour la remise à zéro de ProgressStats dans tests/test_models.py"
Task: "T012 [P] [US2] Écrire le test d'intégration HTTP pour la suppression de la dernière tâche dans tests/test_routes.py"
```

---

## Parallel Example: User Story 3

```bash
# Rédaction simultanée des tests d'accessibilité ARIA et d'état non-désactivé :
Task: "T014 [P] [US3] Écrire les tests d'intégration HTTP vérifiant les attributs d'accessibilité du bouton dans tests/test_routes.py"
Task: "T015 [P] [US3] Écrire le test d'intégration HTTP vérifiant que le bouton de suppression reste actif sur tâche complétée dans tests/test_routes.py"

# En parallèle du template HTML, préparation des styles de focalisation clavier :
Task: "T017 [P] [US3] Ajouter les règles CSS de focalisation accessible au clavier dans app/static/css/style.css"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Réaliser la Phase 1 (Setup) et la Phase 2 (Foundational : `delete_task`).
2. Réaliser la Phase 3 (User Story 1 : tests d'abord, puis route `POST /tasks/<id>/delete`, formulaire HTML et style CSS).
3. **STOP et VALIDATION** : Vérifier que la suppression d'une tâche, le recalcul de la progression et le patron PRG fonctionnent de façon autonome.
4. L'application offre immédiatement la valeur principale demandée : suppression définitive d'une tâche avec mise à jour du tableau de bord.

### Incremental Delivery

1. **Incrément 1 (MVP)** : Suppression ciblée, recalcul proportionnel du compteur et de la jauge, conformité PRG (US1).
2. **Incrément 2** : Gestion fluide et sécurisée de la suppression de la dernière tâche avec retour à l'état vide d'accueil (US2).
3. **Incrément 3** : Accessibilité numérique complète (ARIA, navigation clavier, support des tâches terminées) (US3).
4. **Incrément 4** : Documentation didactique, validation globale `pytest` et exécution des scénarios `quickstart.md` (Polish).

### Parallel Team Strategy

Avec plusieurs développeurs :
1. L'équipe réalise ensemble le Setup (Phase 1) et le socle Foundational (Phase 2).
2. Une fois la Phase 2 validée :
   - Développeur A : Réalise l'US1 (Suppression nominale et mise à jour de progression).
   - Développeur B : Prépare les scénarios de l'US2 (Transition vers l'état d'accueil).
   - Développeur C : Développe l'accessibilité WAI-ARIA et les styles clavier de l'US3.
3. Chaque incrément s'intègre de manière prédictible et sans conflit grâce aux tests automatisés.

---

## Notes

- Les tâches marquées `[P]` portent sur des fichiers distincts et n'ont aucune dépendance non résolue.
- Le marqueur `[Story]` (`[US1]`, `[US2]`, `[US3]`) assure la traçabilité directe avec `spec.md`.
- Règle TDD stricte : les tests doivent être rédigés en premier et échouer avant l'implémentation du code correspondant.
- Engagement git recommandé après chaque tâche ou groupe cohérent.
- Conformité stricte avec la Constitution : Flask SSR, HTML5/CSS3 natif, zéro framework JS, tests `pytest` obligatoires.
