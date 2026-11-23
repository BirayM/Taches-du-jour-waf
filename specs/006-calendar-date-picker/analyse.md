# Specification Analysis Report: Calendrier et Marquage de Dates

**Feature**: `006-calendar-date-picker`  
**Date d'analyse** : 2026-11-23  
**Documents analysés** : `spec.md`, `plan.md`, `tasks.md`, `clarifications.md`, `checklists/requirements.md`  
**Référentiel constitutionnel** : `.specify/memory/constitution.md` (Version 1.1.0)

---

## 1. Findings Table

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| U1 | Underspecification | HIGH | `tasks.md:L42` (T002) vs `tests/conftest.py:L23-32` | Risque de rupture d'étanchéité des tests dans `tests/conftest.py`. La tâche T002 prévoit de créer les fixtures `temp_calendar_storage_path` et `calendar_manager`, mais n'explicite pas la mise à jour de la fixture centrale `app_instance` pour surcharger `"CALENDAR_DATA_FILE": temp_calendar_storage_path`. Sans cette injection, les requêtes simulées via le client Flask (`client`) dans les tests d'intégration HTTP (T008, T009, T014, T021, T027, T032) utiliseront la valeur par défaut `data/calendar.json` et pollueront le stockage réel du projet. | Mettre à jour la description de T002 pour stipuler explicitement que la fixture `app_instance` de `tests/conftest.py` doit être enrichie avec `"CALENDAR_DATA_FILE": temp_calendar_storage_path`, garantissant l'isolation totale des tests conformément au Principe IV et VI de la Constitution. |
| I1 | Inconsistency | MEDIUM | `plan.md:L78` vs `spec.md:L6-18, L102-104`, `clarifications.md:L70-80` | Mention contradictoire d'une « inclusion conditionnelle calendar.js » dans l'arborescence de `plan.md:L78`. Dans `spec.md` et `clarifications.md`, la section calendrier est un composant permanent de la page d'accueil (situé sous la liste des tâches, visible même si la liste des tâches est vide ou lors de l'accueil initial). Contrairement au script `countdown.js` (conditionné par `{% if tasks %}`), `calendar.js` doit être chargé systématiquement sur la page pour permettre les interactions de navigation et de cochage. | Aligner `plan.md:L78` en remplaçant « inclusion conditionnelle calendar.js » par « inclusion systématique de calendar.js via {% block scripts %} » pour éviter toute confusion lors de l'intégration dans `app/templates/index.html`. |
| I2 | Inconsistency | LOW | `spec.md:L117` vs `plan.md:L70`, `tasks.md:L63` (T010) | Dérive terminologique (*terminology drift*) sur l'entité représentant le mois. `spec.md` nomme l'entité `CalendarMonth`, tandis que `plan.md` et `tasks.md` emploient la désignation `CalendarMonthInfo`. | Aligner la spécification ou documenter dans `plan.md` que `CalendarMonthInfo` est le nom d'implémentation Python retenu pour la dataclass représentant le mois affiché. |
| I3 | Inconsistency | LOW | `clarifications.md:L38` vs `tasks.md:L78-80` (Test US2) | Divergence sur le schéma de charge utile de la réponse `POST /calendar/toggle`. `clarifications.md` stipule que le point de terminaison renvoie `{ "date": "YYYY-MM-DD", "checked": true, "month_checked_count": 3 }`, tandis que le scénario de test indépendant de l'US2 dans `tasks.md` n'illustre que `{ "date": "2026-11-23", "checked": true }` sans la clé du compteur. | Confirmer et homogénéiser la signature de retour en incluant systématiquement `month_checked_count` dans la réponse JSON afin de permettre la synchronisation immédiate du compteur sans calcul client divergent. |
| A1 | Ambiguity | LOW | `spec.md:L109` (FR-010), `plan.md:L17` vs `spec.md:L130` (SC-006) | Nuance mineure sur la largeur d'écran mobile minimale de référence. FR-010 et `plan.md` mentionnent une adaptation fluide dès 320px (« mobiles étroits 320px »), tandis que SC-006 et le test indépendant de l'US5 fixent le critère mesurable à 360px. | Harmoniser la formulation du critère SC-006 pour mentionner explicitement une absence de défilement horizontal et une ergonomie tactile préservée de 320px à 360px. |
| D1 | Duplication | LOW | `spec.md:L104` (FR-004) et `spec.md:L105` (FR-005) | Redondance conceptuelle partielle : FR-004 régit la bascule interactive de marquage d'une date (cocher/décocher), tandis que FR-005 régit l'affichage de l'indicateur visuel associé (empreinte de patte 🐾). Il s'agit des deux aspects (action et retour d'état) d'une même fonctionnalité. | Conserver les deux exigences pour la granularité des tests, mais documenter qu'elles sont traitées conjointement au sein de la même interaction utilisateur dans l'US2. |
| U2 | Underspecification | LOW | `plan.md:L34`, `tasks.md:L202` (T037) vs `tasks.md:L92` (T016) | Périmètre de la dégradation gracieuse sans JavaScript insuffisamment détaillé pour l'action de cochage. `plan.md` cite la dégradation gracieuse et T016 mentionne le traitement de formulaire POST, mais les tâches de gabarits (T011, T017, T033) ne précisent pas si chaque jour comporte un formulaire HTML autonome avec redirection Post/Redirect/Get ou si l'action de cochage requiert obligatoirement JavaScript. | Préciser dans `plan.md` ou la tâche T037 que la navigation entre les mois est 100% fonctionnelle sans JavaScript via liens GET standard, tandis que le basculement asynchrone instantané (< 150 ms) des dates cochées est rehaussé par JavaScript. |

---

## 2. Coverage Summary Table

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|
| **FR-001** (Grille mensuelle 7 colonnes lundi à dimanche) | Oui | T004, T006, T009, T011, T012 | Rendu serveur Jinja2 avec module standard `calendar` de Python et CSS Grid. |
| **FR-002** (Intitulé du mois et année au-dessus du calendrier) | Oui | T008, T010, T011 | Affichage dynamique (ex: « Novembre 2026 ») dans l'en-tête de la section calendrier. |
| **FR-003** (Mise en évidence visuelle et textuelle « Aujourd'hui ») | Oui | T009, T010, T012, T025 | Date serveur par défaut avec réajustement dynamique local par `calendar.js` (`new Date()`). |
| **FR-004** (Cocher / décocher une date d'un clic ou au clavier) | Oui | T013, T014, T015, T016, T018, T034 | Traitement interactif réversible par clic souris ou touches Espace / Entrée. |
| **FR-005** (Indicateur visuel patte canine 🐾 et contraste) | Oui | T017, T019 | Classe CSS `.is-checked` avec icône patte canine et couleur d'accentuation contrastée. |
| **FR-006** (Persistance durable des dates cochées) | Oui | T001, T002, T003, T007, T013, T015, T016 | Stockage JSON dédié dans `data/calendar.json` administré par `CalendarManager`. |
| **FR-007** (Commandes de navigation mois précédent / suivant / Aujourd'hui) | Oui | T020, T021, T022, T023, T024 | Paramètres d'URL `GET /?year=YYYY&month=MM` avec validation défensive et repli silencieux. |
| **FR-008** (Compteur synthétique des jours cochés dans le mois) | Oui | T026, T027, T028, T029, T030, T031 | Accord grammatical strict (0 jour, 1 jour, N jours) et message d'encouragement canin. |
| **FR-009** (Accessibilité clavier, `aria-pressed`, libellé vocal complet) | Oui | T032, T033, T034, T035 | Attributs `role="button"`, `tabindex="0"`, `aria-pressed`, libellé date complet en `aria-label`. |
| **FR-010** (Responsive mobile sans défilement horizontal de 320px à bureau) | Oui | T035, T037 | Media queries fluides adaptées aux petits écrans sans débordement horizontal. |
| **FR-011** (Zéro dépendance JavaScript / CSS externe) | Oui | T018, T037, T038 | Utilisation exclusive de JavaScript Vanilla ES6+ natif et CSS3 standard sans npm. |
| **SC-001** (Affichage du calendrier et réactivité au chargement < 1s) | Oui | T008, T010, T011, T037 | Rendu SSR immédiat et léger, temps de chargement estimé < 100 ms. |
| **SC-002** (Bascule visuelle de date < 150 ms) | Oui | T014, T016, T018 | Mise à jour optimiste du DOM en < 20 ms via `calendar.js` et requête `fetch` asynchrone. |
| **SC-003** (100% de conservation des dates après redémarrage/réouverture) | Oui | T003, T007, T013, T015, T036 | Sérialisation JSON atomique et tests unitaires / d'intégration avec `pytest`. |
| **SC-004** (Navigation vers le mois précédent/suivant en 1 action) | Oui | T021, T022, T023, T024 | Boutons directs de navigation temporelle avec rechargement ciblé ou fluide. |
| **SC-005** (100% des éléments utilisables au clavier : Tab, Entrée, Espace) | Oui | T032, T033, T034, T035 | Prise en charge native du focus et écouteurs d'événements clavier `keydown`. |
| **SC-006** (Affichage sans défilement horizontal à 360px de largeur) | Oui | T035, T037 | Grille flexible testée sous différents viewports avec cibles tactiles >= 40x40px. |
| **SC-007** (95% des utilisateurs comprennent immédiatement l'interaction) | N/A *(KPI UX)* | T037 | Critère d'évaluation ergonomique utilisateur post-déploiement ; validé indirectement par l'ergonomie visuelle et la dégradation gracieuse en T037. |

---

## 3. Constitution Alignment Issues

**Résultat : 0 conflit constitutionnel.**

- **Principe I (Simplicité et Vocation Pédagogique)** : **CONFORME**. Architecture linéaire KISS/YAGNI, classe compacte `CalendarManager`, utilisation idiomatique du module standard `calendar` de Python et script JavaScript Vanilla clair sans abstraction superflue.
- **Principe II (Stack Web Épurée - HTML/CSS Natif & Backend Python avec Flask)** : **CONFORME**. Rendu côté serveur assuré par Flask et Jinja2, balisage HTML5 sémantique, CSS natif modulaire, et script interactif client Vanilla pur (aucun framework lourd type React, Vue ou Alpine.js).
- **Principe III (Lisibilité et Documentation)** : **CONFORME**. Prévu explicitement en tâche T038 avec docstrings PEP 257 exhaustives et commentaires pédagogiques sur les calculs matriciels de semaines et l'accessibilité WAI-ARIA.
- **Principe IV (Tests Automatisés Obligatoires avec pytest)** : **CONFORME**. Approche TDD rigoureuse : 10 tâches de tests automatisés (T003, T004, T008, T009, T013, T014, T020, T021, T026, T027, T032) précèdent systématiquement les tâches d'implémentation de chaque phase.
- **Principe V (Minimalisme des Dépendances)** : **CONFORME**. Aucune dépendance externe additionnelle. `requirements.txt` conserve exclusivement `Flask` et `pytest`. L'implémentation repose entièrement sur la bibliothèque standard de Python (`calendar`, `datetime`, `json`, `pathlib`, `dataclasses`).
- **Principe VI (Hygiène de Sécurité et Absence Totale de Données Sensibles)** : **CONFORME**. Zéro secret manipulé, assainissement strict des paramètres d'URL (`year`, `month`), validation du format de date ISO `YYYY-MM-DD`, et isolation des données de test via fixtures temporaires.

---

## 4. Unmapped Tasks

Toutes les tâches de `tasks.md` (T001 à T038) sont directement justifiées, ordonnées et rattachées aux exigences fonctionnelles ou aux impératifs constitutionnels :

- **Phase 1 (Setup - Infrastructure partagée)** :
  - `T001` : Configuration de `CALENDAR_DATA_FILE` dans `app/__init__.py` (rattaché à FR-006).
  - `T002` : Configuration des fixtures hermétiques dans `tests/conftest.py` (rattaché au Principe IV).
- **Phase 2 (Foundational - Socle bloquant & Modèle)** :
  - `T003`, `T004` : Tests TDD unitaires du modèle et du calcul de grille (rattachés à FR-001, FR-006, SC-003).
  - `T005`, `T006`, `T007` : Implémentation de `CheckedDate`, du calcul matriciel et de `CalendarManager` (rattachés à FR-001, FR-006).
- **Phase 3 (User Story 1 - P1 - MVP Affichage)** :
  - `T008`, `T009` : Tests d'intégration HTTP du calendrier mensuel (rattachés à FR-001, FR-002, FR-003, SC-001).
  - `T010`, `T011`, `T012` : Contrôleur Flask `index()`, template HTML5 et feuille de style (rattachés à FR-001, FR-002, FR-003).
- **Phase 4 (User Story 2 - P1 - Cochage persistant)** :
  - `T013`, `T014` : Tests unitaire et d'intégration HTTP pour `POST /calendar/toggle` (rattachés à FR-004, FR-006, SC-002).
  - `T015`, `T016`, `T017`, `T018`, `T019` : Méthode `toggle_date`, route API, script Vanilla JS et CSS de cochage (rattachés à FR-004, FR-005, FR-006, SC-002, SC-003).
- **Phase 5 (User Story 3 - P2 - Navigation temporelle)** :
  - `T020`, `T021` : Tests unitaire et d'intégration de navigation et de repli défensif (rattachés à FR-007, SC-004).
  - `T022`, `T023`, `T024`, `T025` : Validation défensive d'URL, boutons de navigation, styles et surlignage « Aujourd'hui » local (rattachés à FR-003, FR-007, SC-004).
- **Phase 6 (User Story 4 - P3 - Compteur bienveillant)** :
  - `T026`, `T027` : Tests du calcul et de l'affichage du compteur avec accords grammaticaux (rattachés à FR-008).
  - `T028`, `T029`, `T030`, `T031` : Méthode de comptage, gabarit Jinja2, rafraîchissement JS et styles (rattachés à FR-008).
- **Phase 7 (User Story 5 - P4 - Accessibilité & Mobile)** :
  - `T032` : Tests d'intégration HTTP des attributs d'accessibilité WAI-ARIA (rattaché à FR-009, SC-005).
  - `T033`, `T034`, `T035` : Attributs ARIA, gestion des touches Espace/Entrée et styles responsifs mobiles (rattachés à FR-009, FR-010, SC-005, SC-006).
- **Phase 8 (Polish & Transversal)** :
  - `T036` : Exécution complète de la suite `pytest` sans régression (rattaché au Principe IV).
  - `T037` : Validation manuelle multi-navigateurs et dégradation gracieuse (rattaché à FR-010, SC-001, SC-006).
  - `T038` : Documentation PEP 257 et commentaires pédagogiques didactiques (rattaché au Principe III).

---

## 5. Metrics

- **Total Functional Requirements (FR)** : 11
- **Total Success Criteria (SC)** : 7 (dont 6 nécessitant du travail de réalisation logicielle / tests automatisables et 1 KPI ergonomique)
- **Total Requirements & Criteria** : 18
- **Total Tasks** : 38
- **Coverage %** : **100%** (17/17 exigences et critères de build disposent d'au moins une tâche de réalisation ou de validation)
- **Ambiguity Count** : 1 (A1: largeur mobile 320px vs 360px)
- **Duplication Count** : 1 (D1: FR-004 action vs FR-005 rendu visuel de cochage)
- **Inconsistency Count** : 3 (I1: inclusion conditionnelle dans plan.md; I2: CalendarMonth vs CalendarMonthInfo; I3: payload de POST /calendar/toggle)
- **Underspecification Count** : 2 (U1: étanchéité de app_instance dans conftest.py; U2: périmètre exact du cochage sans JS)
- **Critical Issues Count** : **0**

---

## 6. Next Actions

Le dossier de spécification `specs/006-calendar-date-picker` présente un niveau de maturité, de complétude et d'alignement architectural exceptionnel :
- **0 conflit constitutionnel** : respect absolu des principes de stack épurée, minimalisme des dépendances et pédagogie.
- **100% de couverture** : chaque exigence fonctionnelle et critère mesurable est directement couvert par des tâches précises.
- **TDD rigoureusement respecté** : chaque bloc fonctionnel est précédé de ses tests `pytest` obligatoires.
- **Isolation des données** : séparation claire entre `data/calendar.json` et `data/tasks.json`.

### Recommandations avant le démarrage de l'implémentation (`/speckit.implement`) :

1. **Sécuriser T002 (Point U1 - HIGH)** : S'assurer lors de la réalisation de la tâche T002 que la fixture `app_instance` dans `tests/conftest.py` est mise à jour pour surcharger `"CALENDAR_DATA_FILE": temp_calendar_storage_path`. Cela garantira qu'aucune requête HTTP de test n'écrive dans le fichier `data/calendar.json` du dépôt.
2. **Clarifier l'inclusion de `calendar.js` (Point I1 - MEDIUM)** : Charger systématiquement `app/static/js/calendar.js` via `{% block scripts %}` dans `app/templates/index.html` (sans conditionner son inclusion à `tasks`, car le calendrier est toujours présent).
3. **Harmoniser le retour JSON (Point I3 - LOW)** : Renvoyer systématiquement `{ "date": date_str, "checked": new_state, "month_checked_count": count }` dans la route `@bp.route("/calendar/toggle")`.

La fonctionnalité est **prête pour la phase d'implémentation**.

---

*Souhaitez-vous que je propose des modifications de remédiation concrètes pour les points identifiés ?*
