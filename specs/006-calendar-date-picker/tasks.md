---
description: "Task list for feature implementation: Calendrier et Marquage de Dates"
---

# Tasks: Calendrier et Marquage de Dates

**Input**: Design documents from `specs/006-calendar-date-picker/` (`spec.md`, `plan.md`, `clarifications.md`)

**Prerequisites**: `plan.md` (architecture technique Flask/Vanilla JS), `spec.md` (User Stories P1 à P4, critères d'acceptation, contraintes FR-001 à FR-011), `clarifications.md` (décisions d'architecture, `CalendarManager`, `calendar.json`, route `/calendar/toggle`, détection locale client de « Aujourd'hui »), `.specify/memory/constitution.md` (principes didactiques, minimalisme, pytest obligatoire).

**Tests**: Les tâches de tests automatisés (`pytest`) sont **systématiquement placées avant les tâches de code correspondantes** conformément aux exigences TDD et à la consigne explicite du projet.

**Organization**: Les tâches sont regroupées par phase et par user story pour garantir une implémentation incrémentale et des validations indépendantes.

## Format: `[ID] [P?] [Story] Description`

- **[P]** : Tâche parallélisable (fichiers distincts, aucune dépendance bloquante non résolue)
- **[Story]** : Identifiant de la user story rattachée (ex. `[US1]`, `[US2]`, `[US3]`, `[US4]`, `[US5]`)
- Chemins de fichiers explicites inclus dans chaque libellé

## Path Conventions

- **Backend Python (Flask)** : `app/models.py`, `app/routes.py`, `app/__init__.py`
- **Frontend & Templates** : `app/templates/index.html`, `app/static/css/style.css`, `app/static/js/calendar.js`
- **Persistance** : `data/calendar.json` (isolé de `data/tasks.json`)
- **Tests automatisés (`pytest`)** : `tests/conftest.py`, `tests/test_models.py`, `tests/test_routes.py`

---

## Phase 1: Setup (Infrastructure partagée)

**Purpose**: Configuration initiale et fixtures de test pour l'infrastructure du calendrier

- [ ] T001 Configurer la clé de persistance `CALENDAR_DATA_FILE="data/calendar.json"` dans la configuration par défaut de l'application Flask dans `app/__init__.py`
- [ ] T002 [P] Configurer les fixtures pytest `temp_calendar_storage_path` et `calendar_manager` dans `tests/conftest.py`

---

## Phase 2: Foundational (Socle bloquant & Modèle de données)

**Purpose**: Implémenter les structures de données, le calcul de la grille calendaire et la persistance avant toute implémentation d'interface utilisateur

**⚠️ CRITICAL**: Les tests unitaires du socle DOIVENT être écrits en premier et échouer avant l'implémentation du code.

### Tests du socle (TDD - À écrire en premier) ⚠️

- [ ] T003 [P] Écrire les tests unitaires pour la validation de `CheckedDate` (`date_string` au format ISO 8601 standard `YYYY-MM-DD`, `checked` booléen, `updated_at` ISO 8601 UTC) et la persistance dans `CalendarManager` dans `tests/test_models.py`
- [ ] T004 [P] Écrire les tests unitaires pour le calcul matriciel des semaines (7 colonnes lundi à dimanche, cases de padding d'alignement, nombre de jours par mois et gestion des années bissextiles) dans `tests/test_models.py`

### Implémentation du socle

- [ ] T005 Implémenter la dataclass `CheckedDate` et sa validation stricte du format ISO 8601 standard `YYYY-MM-DD` dans `app/models.py`
- [ ] T006 Implémenter les fonctions de calcul matriciel du calendrier mensuel (grille de 7 colonnes lundi=0 à dimanche=6, cases de décalage initiales, total de jours du mois) dans `app/models.py`
- [ ] T007 Implémenter la classe `CalendarManager` avec chargement/sauvegarde atomique dans `data/calendar.json` et isolation totale de `data/tasks.json` dans `app/models.py`

**Checkpoint**: Le socle modèle et la persistance calendaire sont testés et opérationnels. L'implémentation des User Stories peut commencer.

---

## Phase 3: User Story 1 - Affichage du calendrier mensuel interactif (Priority: P1) 🎯 MVP

**Goal**: Afficher dans l'interface un calendrier mensuel clair avec l'intitulé du mois et de l'année en cours, une grille hebdomadaire de 7 colonnes (lundi à dimanche), des cases d'alignement harmonieuses et la mise en évidence visuelle de la date du jour (« Aujourd'hui »).

**Independent Test**: Charger la page d'accueil `GET /` : vérifier la présence de `<section class="calendar-section">`, le titre du mois courant (« Novembre 2026 »), l'en-tête des 7 jours (Lun à Dim), l'alignement des cases et la classe `.is-today` sur la date du jour.

### Tests pour User Story 1 (À écrire en premier) ⚠️

- [ ] T008 [P] [US1] Écrire les tests d'intégration HTTP validant la présence de la section calendrier `<section class="calendar-section">` et le libellé du mois/année dans `tests/test_routes.py`
- [ ] T009 [P] [US1] Écrire les tests d'intégration HTTP validant la structure de la grille 7 colonnes (lundi à dimanche), les cellules d'alignement et l'indicateur visuel « Aujourd'hui » dans `tests/test_routes.py`

### Implémentation pour User Story 1

- [ ] T010 [US1] Injecter les métadonnées du calendrier du mois courant (`CalendarMonthInfo`, liste des jours, date du jour) dans la route `GET /` (`index()`) dans `app/routes.py`
- [ ] T011 [US1] Créer le bloc `<section class="calendar-section">` sous la liste des tâches avec en-tête mois/année, jours de la semaine (Lun-Dim) et grille de cellules de jours dans `app/templates/index.html`
- [ ] T012 [US1] Styliser la section calendrier, la grille CSS de 7 colonnes, les cellules vides de début de mois et la mise en évidence dédiée « Aujourd'hui » dans `app/static/css/style.css`

**Checkpoint**: Le calendrier mensuel du mois courant s'affiche harmonieusement sous la liste des tâches avec la date du jour mise en valeur.

---

## Phase 4: User Story 2 - Cocher et décocher des dates (Priority: P1)

**Goal**: Permettre à l'utilisateur de cliquer sur n'importe quel jour du calendrier pour cocher ou décocher cette date de manière réversible et persistante, avec affichage d'un marqueur canin (empreinte de patte 🐾) et retour d'interaction optimiste sous 150 ms (SC-002).

**Independent Test**: Effectuer une requête `POST /calendar/toggle` avec `{"date": "2026-11-23"}` et vérifier le retour JSON `{ "date": "2026-11-23", "checked": true }`. Répéter l'appel pour vérifier le basculement à `{ "checked": false }`. Recharger la page et vérifier la persistance de l'état coché dans le DOM HTML.

### Tests pour User Story 2 (À écrire en premier) ⚠️

- [ ] T013 [P] [US2] Écrire les tests unitaires pour la méthode `toggle_date(date_str)` de `CalendarManager` (bascule d'état coché/décoché et mise à jour de l'horodatage `updated_at`) dans `tests/test_models.py`
- [ ] T014 [P] [US2] Écrire les tests d'intégration HTTP pour le point de terminaison `POST /calendar/toggle` (succès 200 avec charge JSON, rejet 400 si date invalide, méthode non autorisée 405 sur GET) dans `tests/test_routes.py`

### Implémentation pour User Story 2

- [ ] T015 [US2] Implémenter la méthode `toggle_date(date_str)` dans `CalendarManager` gérant l'ajout, le retrait ou la mise à jour de `CheckedDate` dans `app/models.py`
- [ ] T016 [US2] Implémenter la route API `@bp.route("/calendar/toggle", methods=["POST"])` traitant la requête JSON ou de formulaire et renvoyant le nouvel état dans `app/routes.py`
- [ ] T017 [US2] Mettre à jour `app/templates/index.html` pour restituer l'état coché des cellules avec le symbole patte 🐾 et inclure le script `app/static/js/calendar.js`
- [ ] T018 [US2] Créer le script Vanilla JS `app/static/js/calendar.js` avec mise à jour optimiste du DOM en < 20 ms et envoi asynchrone `fetch('/calendar/toggle')` avec restauration en cas d'erreur réseau
- [ ] T019 [US2] Définir les styles CSS de l'état coché (`.is-checked`, patte canine 🐾, couleur d'accentuation contrastée) dans `app/static/css/style.css`

**Checkpoint**: Les dates peuvent être cochées et décochées d'un clic, avec persistance dans `data/calendar.json` et restitution au rechargement de page.

---

## Phase 5: User Story 3 - Navigation entre les mois (Priority: P2)

**Goal**: Proposer des commandes de navigation permettant de passer au « Mois précédent », au « Mois suivant », et un bouton de retour direct au mois en cours (« Aujourd'hui »), avec prise en charge robuste des transitions d'années (décembre <-> janvier), des années bissextiles et validation défensive des paramètres URL.

**Independent Test**: Appeler `GET /?year=2026&month=12` pour vérifier l'affichage de décembre 2026. Naviguer vers le mois suivant et constater l'affichage de janvier 2027 (`year=2027&month=1`). Fournir des paramètres invalides (`?year=abc&month=99`) et vérifier le repli gracieux et silencieux sur le mois courant sans erreur 500.

### Tests pour User Story 3 (À écrire en premier) ⚠️

- [ ] T020 [P] [US3] Écrire les tests unitaires pour le calcul des mois précédent/suivant (gestion des transitions d'années déc <-> jan et années bissextiles) et la validation défensive des bornes temporelles dans `tests/test_models.py`
- [ ] T021 [P] [US3] Écrire les tests d'intégration HTTP pour la route `GET /` avec paramètres de requête `year` et `month` (navigation valide, mois bissextile février 29 jours, et repli défensif sur le mois courant en cas de paramètres aberrants) dans `tests/test_routes.py`

### Implémentation pour User Story 3

- [ ] T022 [US3] Implémenter la validation défensive des paramètres `year` et `month` dans la route `index()` avec repli automatique sur la date courante en cas de valeur anormale dans `app/routes.py`
- [ ] T023 [US3] Intégrer les liens/boutons de navigation (« Mois précédent », « Mois suivant », « Revenir à aujourd'hui ») dans l'en-tête du calendrier dans `app/templates/index.html`
- [ ] T024 [US3] Styliser les boutons de navigation temporelle et de retour à aujourd'hui dans `app/static/css/style.css`
- [ ] T025 [US3] Enrichir `app/static/js/calendar.js` pour déterminer dynamiquement la date « Aujourd'hui » via l'horloge locale client (`new Date()`) et surligner fidèlement la cellule du jour

**Checkpoint**: L'utilisateur navigue librement d'un mois à l'autre et revient à la date du jour en un clic sans crash sur des paramètres erronés.

---

## Phase 6: User Story 4 - Compteur de dates cochées et bienveillance visuelle (Priority: P3)

**Goal**: Afficher un indicateur synthétique du nombre de dates cochées dans le mois visualisé, avec accord grammatical rigoureux (« Aucun jour coché ce mois-ci », « 1 jour coché ce mois-ci », « X jours cochés ce mois-ci ») et encouragement canin motivant.

**Independent Test**: Charger un mois sans date cochée : observer la mention « Aucun jour coché ce mois-ci ». Cocher une date : le compteur affiche immédiatement « 1 jour coché ce mois-ci » avec un message encourageant. Cocher 3 dates : le compteur affiche « 3 jours cochés ce mois-ci ».

### Tests pour User Story 4 (À écrire en premier) ⚠️

- [ ] T026 [P] [US4] Écrire les tests unitaires pour le calcul du nombre de dates cochées pour un mois et une année donnés dans `CalendarManager` dans `tests/test_models.py`
- [ ] T027 [P] [US4] Écrire les tests d'intégration HTTP validant l'affichage du compteur de dates cochées (cas 0 jour, 1 jour singulier, N jours pluriel) et du message d'encouragement dans `tests/test_routes.py`

### Implémentation pour User Story 4

- [ ] T028 [US4] Implémenter la méthode `get_month_checked_count(year, month)` dans `CalendarManager` dans `app/models.py`
- [ ] T029 [US4] Ajouter le badge de décompte mensuel et le message d'encouragement canin dans la section calendrier de `app/templates/index.html`
- [ ] T030 [US4] Mettre à jour `app/static/js/calendar.js` pour recalculer et rafraîchir instantanément le compteur lors de chaque bascule de date cochée
- [ ] T031 [US4] Styliser le badge de décompte mensuel et le message bienveillant dans `app/static/css/style.css`

**Checkpoint**: Le compteur mensuel reflète exactement le nombre de jours cochés avec un accord grammatical parfait et un retour visuel chaleureux.

---

## Phase 7: User Story 5 - Accessibilité au clavier et affichage adapté aux écrans mobiles (Priority: P4)

**Goal**: Garantir une accessibilité numérique WAI-ARIA exemplaire (navigation au clavier via Tab, Espace et Entrée, attributs `aria-pressed`, libellés vocaux descriptifs) et une ergonomie mobile réactive sans défilement horizontal dès 320px de largeur avec des zones tactiles d'au moins 40x40px.

**Independent Test**: Naviguer au clavier avec Tab jusqu'aux cases de dates et appuyer sur Entrée/Espace pour cocher/décocher : l'attribut `aria-pressed` bascule entre `true` et `false`. Inspecter le libellé vocal (`aria-label`) énonçant le nom complet de la date. Tester l'affichage en résolution 360px et 320px : aucun débordement horizontal, cibles tactiles >= 40x40px.

### Tests pour User Story 5 (À écrire en premier) ⚠️

- [ ] T032 [P] [US5] Écrire les tests d'intégration HTTP validant la conformité des attributs ARIA (`role="button"`, `aria-pressed`, `aria-label` descriptif complet avec date textuelle) dans `tests/test_routes.py`

### Implémentation pour User Story 5

- [ ] T033 [US5] Enrichir les cellules de jours dans `app/templates/index.html` avec les attributs d'accessibilité sémantiques (`role="button"`, `tabindex="0"`, `aria-pressed`, `aria-label="[Nom du jour] [numéro] [mois] [année]"`)
- [ ] T034 [US5] Gérer les événements clavier `keydown` (touches Entrée et Espace) dans `app/static/js/calendar.js` pour permettre le cochage/décochage sans souris
- [ ] T035 [US5] Définir les styles CSS d'accessibilité (anneau de focus bien visible `:focus-visible`, cibles tactiles minimales de 40x40px, media queries responsives 320px et 360px sans défilement horizontal) dans `app/static/css/style.css`

**Checkpoint**: L'intégralité du calendrier est manipulable au clavier et avec un lecteur d'écran, et s'adapte parfaitement aux petits écrans mobiles.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Validation d'ensemble, vérification de non-régression, conformité aux principes constitutionnels et documentation

- [ ] T036 [P] Exécuter la suite complète de tests avec `pytest` et vérifier 100% de succès sans régression sur les fonctionnalités existantes
- [ ] T037 Valider le comportement global de l'application sous différents navigateurs (Chrome, Firefox, Safari) et en l'absence de JavaScript (dégradation gracieuse)
- [ ] T038 [P] Documenter les fonctions et classes dans `app/models.py`, `app/routes.py` et `app/static/js/calendar.js` avec docstrings PEP 257 et commentaires pédagogiques

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)** : Aucune dépendance — peut débuter immédiatement.
- **Foundational (Phase 2)** : Dépend de la Phase 1 — **BLOQUE** toutes les user stories.
- **User Story 1 (Phase 3 - P1)** : Dépend de la Phase 2 — constitue le MVP d'affichage.
- **User Story 2 (Phase 4 - P1)** : Dépend de la Phase 3 (affichage de la grille) — apporte le cochage persistant.
- **User Story 3 (Phase 5 - P2)** : Dépend de la Phase 3 (structure de la grille et navigation d'URL).
- **User Story 4 (Phase 6 - P3)** : Dépend de la Phase 4 (dates cochées disponibles pour le calcul).
- **User Story 5 (Phase 7 - P4)** : Dépend des Phases 3 et 4 (accessibilité des cellules interactives).
- **Polish (Phase 8)** : Dépend de l'achèvement de toutes les user stories retenues.

### Ordonnancement strict dans chaque phase

1. **Les tâches de tests automatisés (`pytest`) sont écrites et exécutées en premier** (elles doivent échouer avant l'implémentation).
2. Les modèles et structures de données sont implémentés.
3. Les services et contrôleurs/routes Flask sont implémentés.
4. Les templates HTML5 et styles CSS sont intégrés.
5. Les scripts client Vanilla JS sont ajoutés.
6. Le checkpoint de validation indépendante est validé avant de passer à la suite.

### Opportunités de parallélisme

- **Phase 1** : T001 et T002 peuvent s'exécuter en parallèle.
- **Phase 2** : T003 et T004 (tests de modèles) peuvent s'écrire en parallèle.
- **Phase 3** : T008 et T009 (tests de routes US1) peuvent s'écrire en parallèle.
- **Phase 4** : T013 et T014 (tests unitaire et d'intégration US2) peuvent s'écrire en parallèle.
- **Phase 5** : T020 et T021 (tests unitaire et d'intégration US3) peuvent s'écrire en parallèle.
- **Phase 6** : T026 et T027 (tests US4) peuvent s'écrire en parallèle.
- **Phase 8** : T036 et T038 peuvent s'exécuter en parallèle.

---

## Parallel Example: User Story 1

```bash
# Lancement en parallèle des tests de l'User Story 1 (à faire avant le code) :
T008 [P] [US1] Écrire les tests d'intégration HTTP validant la présence de la section calendrier dans tests/test_routes.py
T009 [P] [US1] Écrire les tests d'intégration HTTP validant la grille 7 colonnes et l'indicateur « Aujourd'hui » dans tests/test_routes.py
```

## Parallel Example: User Story 2

```bash
# Lancement en parallèle des tests de l'User Story 2 (à faire avant le code) :
T013 [P] [US2] Écrire les tests unitaires pour la méthode toggle_date() de CalendarManager dans tests/test_models.py
T014 [P] [US2] Écrire les tests d'intégration HTTP pour la route POST /calendar/toggle dans tests/test_routes.py
```

---

## Implementation Strategy

### MVP First (User Story 1 & User Story 2)

1. Réaliser la **Phase 1** (Setup) et la **Phase 2** (Foundational).
2. Réaliser la **Phase 3** (User Story 1 - Affichage du calendrier) : les apprenants visualisent le calendrier du mois courant avec la date du jour.
3. Réaliser la **Phase 4** (User Story 2 - Cocher/décocher des dates) : le cœur de la valeur utilisateur est livré (calendrier interactif et persistant).
4. **Validation MVP** : Tester manuellement et avec pytest le fonctionnement autonome du calendrier et du cochage.

### Incréments fonctionnels ultérieurs

1. Ajouter la **Phase 5 (User Story 3)** pour naviguer entre les mois passés et futurs.
2. Ajouter la **Phase 6 (User Story 4)** pour enrichir l'expérience avec le compteur bienveillant canin.
3. Ajouter la **Phase 7 (User Story 5)** pour peaufiner l'accessibilité WAI-ARIA et le responsive mobile 320px/360px.
4. Conclure par la **Phase 8 (Polish)** pour valider la non-régression globale avec `pytest`.

---

## Notes

- Tous les identifiants de tâches suivent strictement le format `- [ ] TXXX [P?] [USX?] Description avec chemin de fichier`.
- Respect scrupuleux du principe de la Constitution : aucune dépendance externe superflue au-delà de Flask et pytest.
- Isolation complète des données : `data/calendar.json` évite toute interférence avec le fichier `data/tasks.json`.
- La date « Aujourd'hui » est résolue par le client JS (`new Date()`) pour s'adapter au fuseau horaire réel de l'utilisateur, éliminant tout décalage avec le serveur.
