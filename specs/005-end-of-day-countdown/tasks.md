---
description: "Task list for Compte à Rebours de Fin de Journée implementation"
---

# Tasks: Compte à Rebours de Fin de Journée

**Input**: Design documents from `/specs/005-end-of-day-countdown/`
- Plan: [plan.md](plan.md)
- Specification: [spec.md](spec.md)
- Data Model: [data-model.md](data-model.md)
- Web Contracts: [contracts/web-routes.md](contracts/web-routes.md)
- Research: [research.md](research.md)
- Quickstart & Validation: [quickstart.md](quickstart.md)
- Clarifications: [clarifications.md](clarifications.md)

**Constitution Guidelines**:
- Tests automatisés obligatoires avec `pytest` pour toute la logique Python et le rendu des templates (Principe IV).
- Flask comme unique dépendance backend, HTML5/CSS3 pur et Vanilla JS ES6+ épuré sans framework lourd ni dépendance npm (Principes II et V).
- Minimalisme absolu des dépendances : uniquement `flask` et `pytest` dans `requirements.txt` (Principe V).
- Code lisible, auto-porteur et documenté de manière didactique pour des apprenants (Principe III).

**Format**: `- [ ] [ID] [P?] [Story?] Description with file path`
- **[P]**: Tâche exécutable en parallèle (fichiers distincts, aucune dépendance non résolue).
- **[Story]**: Rattachement à une User Story (`[US1]`, `[US2]`, `[US3]`, `[US4]`). Absent pour Setup, Foundational et Polish.
- **TDD (Test-First)** : Les tâches de tests sont systématiquement positionnées avant les tâches de code correspondantes.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Validation de l'environnement de développement et initialisation de l'arborescence statique JavaScript.

- [ ] T001 Vérifier l'environnement virtuel et l'exécution initiale de la suite de tests existante avec `.venv/bin/pytest` ou `pytest`
- [ ] T002 [P] Créer le répertoire `app/static/js/` destiné à accueillir les scripts JavaScript Vanilla de l'application

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Socle fondamental technique pour la distribution des fichiers statiques JavaScript et les styles universels d'accessibilité.

**⚠️ CRITICAL**: Les user stories dépendent de ce socle fondamental avant l'intégration du compte à rebours.

### Tests pour le socle fondamental ⚠️

> **NOTE: Écrire ces tests en premier et vérifier qu'ils échouent avant l'implémentation**

- [ ] T003 [P] Écrire le test d'intégration HTTP dans `tests/test_routes.py` vérifiant que Flask distribue correctement les fichiers statiques JavaScript situés dans `app/static/js/` avec le code HTTP 200

### Implémentation du socle fondamental

- [ ] T004 [P] Ajouter la classe utilitaire d'accessibilité `.sr-only` dans `app/static/css/style.css` (propriétés `position: absolute`, `width: 1px`, `height: 1px`, `padding: 0`, `margin: -1px`, `overflow: hidden`, `clip: rect(0, 0, 0, 0)`, `white-space: nowrap`, `border: 0`)
- [ ] T005 Déclarer le bloc Jinja2 extensible `{% block scripts %}{% endblock %}` avant la fermeture `</body>` dans `app/templates/base.html` pour permettre l'inclusion propre des scripts client par les templates enfants

**Checkpoint**: Socle fondamental prêt - l'implémentation des user stories peut débuter en respectant l'ordre de priorité.

---

## Phase 3: User Story 1 - Affichage dynamique du temps restant jusqu'à la fin de la journée (Priority: P1) 🎯 MVP

**Goal**: Afficher en temps réel le temps restant jusqu'à minuit dans la carte de motivation (`.quote-card`), à côté de l'illustration du chien encourageant, au format « HH h MM min SS s » (ex: « 05 h 32 min 10 s »), actualisé chaque seconde sans rechargement de page dès qu'au moins une tâche existe.

**Independent Test**: Créer au moins une tâche dans l'application, ouvrir la page d'accueil : le compte à rebours s'affiche immédiatement dans la carte de motivation au format « HH h MM min SS s » et décrémente ses secondes à chaque seconde écoulée sans aucun rafraîchissement de page.

### Tests pour User Story 1 ⚠️

> **NOTE: Écrire ces tests en premier et vérifier qu'ils échouent avant l'implémentation**

- [ ] T006 [P] [US1] Écrire les tests d'intégration HTTP pour la route statique `GET /static/js/countdown.js` dans `tests/test_routes.py` (vérification du code HTTP 200, Content-Type `text/javascript` ou `application/javascript`, et présence des signatures de fonctions `calculateRemainingTime`, `formatCountdown`, `initCountdown`)
- [ ] T007 [P] [US1] Écrire les tests d'intégration pour le rendu HTML de la page d'accueil avec tâche dans `tests/test_routes.py` (vérification que `GET /` avec au moins une tâche enregistrée contient l'élément `#countdown-container`, la balise `<time class="countdown-display">`, l'élément `#countdown-text` et la balise `<script defer src=".../countdown.js">` à l'intérieur de `.quote-card`)

### Implementation pour User Story 1

- [ ] T008 [P] [US1] Implémenter les fonctions pures `calculateRemainingTime(now = new Date())` et `formatCountdown(hours, minutes, seconds)` dans `app/static/js/countdown.js` conformément aux contraintes de `data-model.md` : calcul de la cible locale `target = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1, 0, 0, 0, 0)`, non-négativité stricte `diffMs = Math.max(0, target - now)`, plage des entiers `hours` ("0 à 23"), `minutes` ("0 à 59"), `seconds` ("0 à 59"), et formatage strict à deux chiffres `HH h MM min SS s` ("Les composants numériques sont complétés par un zéro à gauche si inférieurs à 10 (padStart(2, '0')), garantissant une largeur visuelle invariable et l'absence de sautillement de mise en page")
- [ ] T009 [US1] Implémenter la fonction `initCountdown()` et le gestionnaire de cycle de vie dans `app/static/js/countdown.js` pour cibler `#countdown-text`, effectuer une première mise à jour immédiate à l'affichage pour éviter tout délai d'initialisation, puis cadencer l'actualisation continue toutes les 1 000 ms via `setInterval`
- [ ] T010 [US1] Intégrer la structure HTML du compte à rebours dans la section `.quote-card` et l'inclusion du script client dans le gabarit `app/templates/index.html` selon `contracts/web-routes.md` : conteneur `<div class="quote-countdown" id="countdown-container">`, libellé `<span class="countdown-label">Temps restant :</span>`, affichage `<time class="countdown-display">`, et texte dynamique `<span id="countdown-text">-- h -- min -- s</span>`
- [ ] T011 [P] [US1] Définir les règles de style de base pour la disposition de la carte et du compte à rebours dans `app/static/css/style.css` (`.quote-card` en disposition flexbox avec espacement `justify-content: space-between`, carte `.quote-countdown` avec fond `#FAF5EE` et bordure douce, étiquette `.countdown-label` en majuscules discrètes, et affichage `.countdown-display` en police monospace `1.05rem`)

**Checkpoint**: User Story 1 pleinement fonctionnelle et testable de façon autonome (MVP atteint : affichage dynamique et défilement fluide par seconde dès qu'une tâche existe).

---

## Phase 4: User Story 2 - Masquage automatique du compte à rebours en l'absence de tâches (Priority: P2)

**Goal**: Masquer intégralement le compte à rebours (balisage HTML et exécution du script) lorsque l'application ne contient aucune tâche (état vide initial ou suite à la suppression de la dernière tâche), tout en maintenant le décompte actif si toutes les tâches sont achevées (100% de complétion avec carte de célébration).

**Independent Test**: Charger l'application sans tâche : vérifier l'absence complète de `#countdown-container` et de `countdown.js`. Ajouter une tâche : observer son apparition. Supprimer la tâche : vérifier sa disparition immédiate. Compléter toutes les tâches : vérifier que le compte à rebours demeure visible aux côtés de la célébration canine.

### Tests pour User Story 2 ⚠️

> **NOTE: Écrire ces tests en premier et vérifier qu'ils échouent avant l'implémentation**

- [ ] T012 [P] [US2] Écrire les tests d'intégration HTTP pour l'état d'accueil vide dans `tests/test_routes.py` (vérification que `GET /` sans aucune tâche ne contient ni `#countdown-container`, ni `<script ... countdown.js>`, conformément à SC-002)
- [ ] T013 [P] [US2] Écrire les tests d'intégration HTTP pour la suppression de la dernière tâche et le maintien lors de la célébration à 100% dans `tests/test_routes.py` selon `data-model.md` : vérification que la suppression de l'unique tâche (`len(tasks) == 1` vers `len(tasks) == 0`) retire `#countdown-container` du DOM, et vérification que lorsque toutes les tâches sont accomplies (`percentage == 100%`, `is_all_completed == True`), `#countdown-container` et `countdown.js` restent présents conjointement avec `.celebration-card` ("Tant que le nombre total de tâches est supérieur ou égal à 1, le compte à rebours s'exécute, même si toutes les tâches sont achevées")

### Implementation pour User Story 2

- [ ] T014 [US2] Encapsuler le conteneur `#countdown-container` et l'inclusion du script `countdown.js` sous la condition Jinja2 `{% if tasks %}` dans `app/templates/index.html` afin d'empêcher l'injection du balisage et l'exécution du timer lorsque `tasks` est vide
- [ ] T015 [US2] Ajouter une garde défensive au début de `initCountdown()` dans `app/static/js/countdown.js` (`const container = document.getElementById('countdown-container'); const textEl = document.getElementById('countdown-text'); if (!container || !textEl) return;`) pour interrompre immédiatement l'exécution sans erreur si le conteneur est absent du DOM

**Checkpoint**: User Stories 1 et 2 validées : affichage conditionné strictement par la présence de tâches, masquage total à l'état vide et maintien lors de la complétion à 100%.

---

## Phase 5: User Story 3 - Continuité fluide lors du passage à minuit (Priority: P3)

**Goal**: Garantir un enchaînement continu et transparent du décompte lors du franchissement de minuit (00:00:00), sans bloquer l'affichage, sans valeur négative, et sans exiger de rechargement de la page, tout en assurant une resynchronisation immédiate lors du réveil après mise en veille prolongée d'un onglet.

**Independent Test**: Simuler le passage de 23:59:59 à 00:00:00 : vérifier que le décompte passe immédiatement de « 00 h 00 min 01 s » à « 23 h 59 min 59 s » sans valeur négative ni blocage, et vérifier que la réactivation d'un onglet après plusieurs minutes d'arrière-plan recalcule instantanément le temps exact restant.

### Tests pour User Story 3 ⚠️

> **NOTE: Écrire ces tests en premier et vérifier qu'ils échouent avant l'implémentation**

- [ ] T016 [P] [US3] Écrire les tests automatisés dans `tests/test_routes.py` validant l'algorithme temporel et la résilience de transition dans `app/static/js/countdown.js` (vérification de la présence de la logique `Math.max(0, target - now)` interdisant les valeurs négatives, du calcul de la date cible locale au jour suivant `now.getDate() + 1` à `00:00:00`, et du calcul direct basé sur l'horloge système absolue `new Date()` garantissant l'immunité contre le ralentissement des onglets inactifs selon `data-model.md` : "Non-négativité stricte : diffMs >= 0, hours >= 0, minutes >= 0, seconds >= 0. Aucune valeur négative n'est tolérée dans le DOM")

### Implementation pour User Story 3

- [ ] T017 [US3] Consolider l'algorithme de calcul dynamique dans `app/static/js/countdown.js` selon les spécifications de `data-model.md` et `research.md` : recalcul dynamique de l'instant présent `now = new Date()` à chaque tick d'intervalle, ciblage dynamique du minuit calendaire suivant `new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1, 0, 0, 0, 0)`, basculement automatique et immédiat à `00:00:00` vers `23 h 59 min 59 s` sans interruption, et protection contre les millisecondes négatives via `Math.max(0, ...)`

**Checkpoint**: User Stories 1, 2 et 3 fonctionnelles : continuité temporelle sans faille à minuit et résilience aux onglets inactifs.

---

## Phase 6: User Story 4 - Accessibilité numérique et lisibilité mobile (Priority: P4)

**Goal**: Garantir une accessibilité numérique optimale pour les technologies d'assistance (libellé explicite, interdiction formelle de toute annonce vocale intempestive à chaque seconde) et assurer un affichage responsive soigné sur tous types d'écrans (320px à 2560px), particulièrement sur smartphone avec adaptation verticale.

**Independent Test**: Inspecter le balisage avec un outil d'accessibilité pour confirmer la présence de `aria-label="Temps restant avant la fin de la journée"`, `aria-live="off"`, `aria-hidden="true"` sur les secondes défilantes, et la classe `.sr-only`. Réduire la fenêtre du navigateur à 360px de large pour valider l'alignement harmonieux et l'absence de débordement sous la mascotte canine.

### Tests pour User Story 4 ⚠️

> **NOTE: Écrire ces tests en premier et vérifier qu'ils échouent avant l'implémentation**

- [ ] T018 [P] [US4] Écrire les tests d'intégration HTTP dans `tests/test_routes.py` vérifiant la conformité stricte du balisage d'accessibilité WAI-ARIA selon `contracts/web-routes.md` : présence de `role="region"`, `aria-label="Temps restant avant la fin de la journée"` sur `#countdown-container`, `aria-live="off"` sur `.countdown-display`, `aria-hidden="true"` sur `#countdown-text`, inclusion de `<span class="sr-only">Temps restant avant la fin de la journée</span>`, et absence formelle de `aria-live="polite"` ou `aria-live="assertive"`
- [ ] T019 [P] [US4] Écrire les tests de validation de la feuille de style dans `tests/test_routes.py` vérifiant la présence des règles de mise en page responsive mobile `@media (max-width: 600px)` et de la classe d'accessibilité `.sr-only` dans `app/static/css/style.css`

### Implementation pour User Story 4

- [ ] T020 [US4] Mettre en conformité le balisage sémantique HTML5 et WAI-ARIA dans `app/templates/index.html` conformément à `data-model.md` : attribut `role="region"` et `aria-label="Temps restant avant la fin de la journée"` sur `#countdown-container`, attribut `aria-live="off"` sur la balise `<time class="countdown-display">`, masquage du texte chiffré aux lecteurs d'écran via `aria-hidden="true"` sur `#countdown-text`, et libellé statique vocal accessible `<span class="sr-only">Temps restant avant la fin de la journée</span>`
- [ ] T021 [P] [US4] Ajouter les règles de mise en page responsive dans `app/static/css/style.css` pour les écrans de faible largeur via `@media (max-width: 600px)` (largeur `100%`, centrage des éléments avec `align-items: center`, marge supérieure de séparation `margin-top: 0.5rem`) afin de garantir une présentation fluide de 320px à 600px sans débordement (SC-005)

**Checkpoint**: Toutes les User Stories (US1 à US4) sont implémentées, accessibles, adaptatives et couvertes par les tests automatisés.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Qualité didactique du code, documentation pédagogique et validation exhaustive de bout en bout de la fonctionnalité.

- [ ] T022 [P] Vérifier la conformité PEP 257 des docstrings Python et enrichir les commentaires explicatifs didactiques dans `app/static/js/countdown.js`, `app/templates/index.html` et `tests/test_routes.py` (Constitution III)
- [ ] T023 Exécuter la suite complète de tests avec `pytest` et valider 100% de tests au vert (Constitution IV)
- [ ] T024 Valider l'absence de toute nouvelle dépendance externe dans `requirements.txt` en confirmant la présence exclusive de `Flask` et `pytest` (Constitution V)
- [ ] T025 Exécuter l'ensemble des scénarios de validation manuelle de bout en bout définis dans `specs/005-end-of-day-countdown/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Aucune dépendance - démarrage immédiat.
- **Foundational (Phase 2)**: Dépend de la Phase 1 (Setup) - BLOCAGE de toutes les user stories.
- **User Stories (Phase 3 à 6)**: Dépendent de l'achèvement de la Phase 2 (Foundational).
  - Déroulement séquentiel recommandé selon l'ordre de priorité : P1 (US1) → P2 (US2) → P3 (US3) → P4 (US4).
  - US2, US3 et US4 enrichissent la structure posée par US1 mais demeurent testables de façon autonome.
- **Polish (Phase 7)**: Dépend de l'achèvement de l'ensemble des User Stories.

### User Story Dependencies

- **User Story 1 (P1)**: Dépend uniquement de la Phase 2 (Foundational). Constitue le socle MVP autonome.
- **User Story 2 (P2)**: Dépend de la Phase 2 et s'articule avec l'affichage conditionnel initié en US1.
- **User Story 3 (P3)**: Dépend de la fonction de calcul temporel de US1 (`calculateRemainingTime`).
- **User Story 4 (P4)**: Dépend du balisage HTML de US1 et des styles CSS existants.

### Within Each User Story (TDD Pattern)

- **Tests FIRST** : Les tâches de tests (`tests/test_routes.py`) DOIVENT être rédigées en premier et constatées en échec avant toute implémentation.
- **Client Script & Templates** : Fonctions modulaires pures JS → Orchestration du timer → Gabarit HTML Jinja2 → Styles CSS.
- **Validation** : Chaque story doit être fonctionnelle et validée avant de passer à la priorité suivante.

### Parallel Opportunities

- Phase 1 : T002 peut s'exécuter en parallèle de T001.
- Phase 2 : T003 et T004 peuvent s'exécuter en parallèle.
- Phase 3 (US1) : T006 et T007 (tests) peuvent s'écrire en parallèle. Côté code, T008 (fonctions pures) et T011 (CSS) peuvent s'écrire en parallèle.
- Phase 4 (US2) : T012 et T013 (tests) peuvent s'écrire en parallèle.
- Phase 6 (US4) : T018 et T019 (tests) peuvent s'écrire en parallèle, et T021 (CSS responsive) en parallèle de T020.
- Phase 7 : T022 et T024 peuvent s'exécuter en parallèle.

---

## Parallel Example: User Story 1

```bash
# Rédaction des tests en premier (parallélisable) :
Task T006: "Tests d'intégration HTTP pour la route statique GET /static/js/countdown.js dans tests/test_routes.py"
Task T007: "Tests d'intégration pour le rendu HTML de la page d'accueil avec tâche dans tests/test_routes.py"

# Développement du code après échec constaté des tests :
Task T008: "Implémenter les fonctions pures calculateRemainingTime et formatCountdown dans app/static/js/countdown.js"
Task T011: "Définir les règles de style de base pour la disposition de la carte et du compte à rebours dans app/static/css/style.css"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Exécuter Phase 1 (Setup) et Phase 2 (Foundational).
2. Rédiger les tests de User Story 1 (T006, T007) et constater leur échec.
3. Implémenter les composants de User Story 1 (T008, T009, T010, T011).
4. **STOP et VALIDATION** : Vérifier que les tests US1 passent au vert et que le compte à rebours fonctionne en direct avec au moins une tâche. Déployable/démontrable immédiatement en tant que MVP !

### Incremental Delivery

1. **Incrément 1 (MVP - US1)** : Compte à rebours dynamique actif dès qu'une tâche existe.
2. **Incrément 2 (US2)** : Masquage propre à l'état vide et réactivité lors de la suppression de la dernière tâche.
3. **Incrément 3 (US3)** : Continuité fluide lors du passage à minuit (23:59:59 → 00:00:00) et immunité aux onglets inactifs.
4. **Incrément 4 (US4)** : Accessibilité numérique certifiée (zéro pollution sonore) et adaptabilité mobile soignée.
5. **Incrément 5 (Polish)** : Documentation didactique, revue de conformité constitutionnelle et validation quickstart.

---

## Notes

- Tous les identifiants de tâches suivent le format strict `[TaskID] [P?] [Story?] Description avec chemin de fichier`.
- Les libellés d'User Story (`[US1]`, `[US2]`, `[US3]`, `[US4]`) garantissent la traçabilité intégrale vers `spec.md`.
- Les contraintes temporelles et règles de validation issues de `data-model.md` sont citées textuellement pour éviter toute ambiguïté d'implémentation.
- Respect rigoureux du principe TDD : aucun code de production n'est écrit sans test préalable.
