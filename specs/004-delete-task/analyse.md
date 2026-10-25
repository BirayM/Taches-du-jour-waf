# Specification Analysis Report: Suppression de Tâche Individuelle

**Feature**: `004-delete-task`  
**Date d'analyse** : 2026-10-24  
**Documents analysés** : `spec.md`, `plan.md`, `tasks.md`, `data-model.md`, `contracts/web-routes.md`, `research.md`, `clarifications.md`, `quickstart.md`, `checklists/requirements.md`  
**Référentiel constitutionnel** : `.specify/memory/constitution.md` (Version 1.1.0)

---

## 1. Findings Table

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| I1 | Inconsistency | LOW | `spec.md:L46, L72` vs `data-model.md:L16`, `contracts/web-routes.md:L59`, `tasks.md:L101` | Divergence mineure de terminologie pour le gabarit de libellé accessible : `spec.md` mentionne `{nom}` (`aria-label="Supprimer la tâche : {nom}"`), tandis que `data-model.md`, `contracts/` et `tasks.md` utilisent l'attribut d'entité réel `task.title` / `{titre}`. | Harmoniser `spec.md` pour mentionner `{titre}` afin de correspondre rigoureusement à l'attribut de modèle `Task.title`. |
| U1 | Underspecification | LOW | `spec.md:L89` (SC-002) vs `tasks.md` | Le critère SC-002 exige un recalcul du tableau de bord en moins d'une seconde, mais aucune tâche dans `tasks.md` n'inclut d'assertion explicite de temps d'exécution (benchmark ou timer de latence HTTP). | L'architecture locale synchrone en SSR Flask garantit nativement un temps de traitement inférieur à 50 ms. Consigner explicitement cette garantie architecturale ou ajouter une assertion de seuil (< 1000 ms) dans `test_routes.py`. |
| D1 | Duplication | LOW | `spec.md:L63-64` (FR-003, FR-004) vs `data-model.md:L46-52` | Séparation en deux exigences distinctes (FR-003 pour le compteur "X sur Y" et FR-004 pour la barre de progression graphique) alors que les deux grandeurs sont produites de façon atomique par l'objet calculé unique `ProgressStats` (`TaskManager.get_progress()`). | Conserver la distinction fonctionnelle pour la clarté utilisateur, mais annoter dans l'implémentation que la mise à jour est atomique et ne nécessite pas deux calculs distincts. |

---

## 2. Coverage Summary Table

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|
| **FR-001** (Bouton de suppression identifiable) | Oui | T009, T010, T016, T017 | Formulaire HTML avec bouton `.btn-delete` et icône `🗑️` dans chaque carte de tâche. |
| **FR-002** (Suppression définitive de la persistance locale via ID) | Oui | T003, T004, T006, T008 | Méthode `TaskManager.delete_task(task_id)` synchrone sans corbeille ni soft-delete. |
| **FR-003** (Recalcul immédiat du compteur de tâches) | Oui | T005, T006, T008 | Recalcul dans `ProgressStats` via `get_progress()`. |
| **FR-004** (Recalcul immédiat de la barre de progression) | Oui | T005, T006, T007, T008 | Ajustement du pourcentage `0%..100%` et déclenchement célébration si 100%. |
| **FR-005** (Retour à l'état vide d'accueil si dernière tâche supprimée) | Oui | T011, T012, T013 | Masquage de `.progress-section`, restitution de `dog-resting.svg` et citation d'accueil. |
| **FR-006** (Patron Post/Redirect/Get - PRG vers `/`) | Oui | T006, T008, T020 | Redirection HTTP 302 vers `/`, protection contre ré-émission lors d'un F5. |
| **FR-007** (Gestion sans erreur d'un ID inexistant ou supprimé) | Oui | T003, T006, T008 | Idempotence : `delete_task` renvoie `False` sans lever d'exception, redirection 302 sans code 500. |
| **FR-008** (Accessibilité clavier et libellé `aria-label` explicite) | Oui | T014, T015, T016, T017, T020 | Attributs `aria-label`, `title`, masquage de l'icône via `aria-hidden="true"`, et focus clavier visible. |
| **FR-009** (Exclusions : pas de modale, pas de corbeille, pas de lot) | Oui | T008, T009, T016 | Respecté nativement par conception (soumission directe sans dialogue JS bloquant ni soft delete). |
| **SC-001** (100% suppressions effectives sans altérer l'ordre) | Oui | T003, T006 | Couvert par les tests unitaires et d'intégration. |
| **SC-002** (Recalcul et actualisation en < 1 seconde) | Oui | T006, T008 | Garanti structurellement par le rendu côté serveur Flask en mémoire/JSON local (< 50 ms). |
| **SC-003** (100% bascule vers l'état d'accueil initial sans incohérence) | Oui | T011, T012, T013 | Couvert par test de non-régression et gabarit Jinja2. |
| **SC-004** (100% conformité PRG sans avertissement navigateur) | Oui | T006, T020 | Validé par test HTTP et scénario manuel 5. |
| **SC-005** (100% boutons actionnables au clavier et aria-label individualisé) | Oui | T014, T015, T016, T017, T020 | Validé par tests de rendu HTTP et scénario manuel 6. |
| **SC-006** (0 erreur 500 sur identifiant inexistant ou re-clic) | Oui | T003, T006, T008 | Test unitaire et test HTTP dédiés. |

---

## 3. Constitution Alignment Issues

**Résultat : 0 conflit constitutionnel.**

- **Principe I (Simplicité et Vocation Pédagogique)** : **CONFORME**. Architecture linéaire KISS/YAGNI, aucune abstraction superflue (pas de corbeille, pas de boîte modale complexe).
- **Principe II (Stack Web Épurée - HTML/CSS Natif & Flask)** : **CONFORME**. Soumission par formulaire HTML standard `<form method="POST">`, aucune dépendance JavaScript, rendu côté serveur direct.
- **Principe III (Lisibilité et Documentation)** : **CONFORME**. Prévu en tâche T018 avec docstrings PEP 257 et commentaires pédagogiques sur le patron PRG et WAI-ARIA.
- **Principe IV (Tests Automatisés Obligatoires avec pytest)** : **CONFORME**. Approche TDD stricte : toutes les tâches de tests (T003, T005, T006, T007, T011, T012, T014, T015) sont planifiées avant le code d'implémentation.
- **Principe V (Minimalisme des Dépendances)** : **CONFORME**. Aucune bibliothèque tierce additionnelle ; utilisation stricte de Flask, pytest et de la bibliothèque standard Python (`json`, `pathlib`).
- **Principe VI (Hygiène de Sécurité)** : **CONFORME**. Point d'accès strictement restreint à la méthode POST (rejet GET par HTTP 405), aucune donnée sensible manipulée.

---

## 4. Unmapped Tasks

Toutes les tâches définies dans `tasks.md` sont directement justifiées et rattachées :

- **Tâches d'infrastructure & configuration (Setup)** :
  - `T001` : Validation de l'environnement virtuel et de l'état initial des tests (Principe IV).
  - `T002` : Vérification des ressources vectorielles existantes (`dog-resting.svg`, `dog-cheer.svg`).
- **Tâches fondamentales (Foundational)** :
  - `T003`, `T004` : Persistance unitaire `delete_task` servant de socle bloquant pour toutes les User Stories.
- **Tâches User Story 1 (P1)** :
  - `T005` à `T010` : Tests TDD et implémentation de la suppression, recalcul et route PRG.
- **Tâches User Story 2 (P2)** :
  - `T011` à `T013` : Tests TDD et gestion de l'état vide d'accueil.
- **Tâches User Story 3 (P3)** :
  - `T014` à `T017` : Tests TDD et accessibilité WAI-ARIA / navigation clavier.
- **Tâches transversales de finition (Polish)** :
  - `T018` : Documentation pédagogique et docstrings (Principe III).
  - `T019` : Validation d'ensemble par la suite `pytest` (Principe IV).
  - `T020` : Exécution des scénarios de validation manuelle de bout en bout (`quickstart.md`).
  - `T021` : Mise à jour documentaire dans `README.md`.

---

## 5. Metrics

- **Total Functional Requirements (FR)** : 9
- **Total Success Criteria (SC)** : 6
- **Total Requirements & Criteria** : 15
- **Total Tasks** : 21
- **Coverage %** : **100%** (15/15 exigences et critères disposent d'au moins une tâche de réalisation ou de test)
- **Ambiguity Count** : 1 (SC-002 sans seuil temporel testé de façon automatisée)
- **Duplication Count** : 1 (FR-003 / FR-004 regroupés dans le même état calculé `ProgressStats`)
- **Critical Issues Count** : **0**

---

## 6. Next Actions

Le dossier de spécification et d'ingénierie `specs/004-delete-task` présente une excellente cohérence, une conformité totale avec la Constitution du projet et une traçabilité intégrale (100% de couverture des exigences par les tâches de tests et d'implémentation).

- **Statut global** : **PRÊT POUR IMPLÉMENTATION** (`/speckit.implement`).
- **Actions recommandées** :
  1. *Optionnel* : Corriger la mention de `{nom}` en `{titre}` dans `spec.md` (FR-008) pour une parfaite harmonie sémantique avec `data-model.md`.
  2. Passer à la phase d'implémentation via la commande `/speckit.implement`.

---

*Souhaitez-vous que je propose des modifications de remédiation concrètes pour les points mineurs identifiés ?*
