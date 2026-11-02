# Specification Analysis Report: Compte à Rebours de Fin de Journée

**Feature**: `005-end-of-day-countdown`  
**Date d'analyse** : 2026-11-02  
**Documents analysés** : `spec.md`, `plan.md`, `tasks.md`, `data-model.md`, `contracts/web-routes.md`, `research.md`, `clarifications.md`, `quickstart.md`, `checklists/requirements.md`  
**Référentiel constitutionnel** : `.specify/memory/constitution.md` (Version 1.1.0)

---

## 1. Findings Table

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| I1 | Inconsistency | MEDIUM | `tasks.md:L70-71` (T007) vs `tasks.md:L42` (T005), `contracts/web-routes.md:L41-45`, `app/templates/base.html` | Incohérence d'emplacement pour la balise `<script>`. La description de T007 mentionne la présence de la balise `<script defer src=".../countdown.js"> à l'intérieur de .quote-card`, tandis que T005 prévoit d'introduire le bloc `{% block scripts %}` en fin de `base.html` (avant `</body>`) et que `contracts/web-routes.md` préconise l'inclusion en fin de corps via ce bloc. Imbriquer un `<script>` dans un bloc de contenu `.quote-card` est contraire aux bonnes pratiques et contradictoire avec T005. | Harmoniser la description de la tâche T007 pour spécifier que `<script defer src=".../countdown.js">` est injecté via `{% block scripts %}` en fin de page (ou dans le document HTML), et non imbriqué à l'intérieur de `.quote-card`. |
| I2 | Inconsistency | LOW | `clarifications.md:L77` vs `contracts/web-routes.md:L35, L68`, `tasks.md:L71`, `research.md:L51` | Divergence mineure de nommage de classe CSS : `clarifications.md` utilise `<span class="countdown-caption">Temps restant :</span>`, tandis que `contracts/web-routes.md`, `tasks.md`, `research.md` et les définitions de styles CSS utilisent systématiquement `.countdown-label` (`<span class="countdown-label">Temps restant :</span>`). | Aligner `clarifications.md` sur `contracts/web-routes.md` et `tasks.md` en retenant la classe définitive `.countdown-label`. |
| D1 | Duplication | LOW | `tasks.md:L74` (T010) vs `tasks.md:L120` (T020) et `contracts/web-routes.md:L30-40` | Édition itérative redondante du gabarit `app/templates/index.html`. La tâche T010 intègre le balisage partiel du compte à rebours pour satisfaire le MVP (US1), puis la tâche T020 réédite le même fichier pour y injecter les attributs d'accessibilité WAI-ARIA (`role="region"`, `aria-label`, `aria-live="off"`, `aria-hidden="true"`, et `<span class="sr-only">`), pourtant déjà figés dans le contrat d'interface. | Bien que ce découpage reflète la progression par User Story, il est recommandé d'insérer d'emblée la structure HTML accessible complète dès T010 afin d'éviter une double retouche du template Jinja2. |
| D2 | Duplication | LOW | `spec.md:L89-90` (FR-001, FR-002) et `spec.md:L114-115` (SC-001, SC-002) | Redondance conceptuelle entre affichage conditionnel (`FR-001` / `SC-001` dès qu'une tâche existe) et masquage à l'état vide (`FR-002` / `SC-002` si aucune tâche), qui relèvent en réalité d'une seule et même condition logique binaire `len(tasks) > 0` dans Jinja2. | Conserver la distinction pour la clarté pédagogique et l'orientation des tests d'état vide, tout en notant dans l'implémentation qu'une seule conditionnelle `{% if tasks %}` régit les deux états. |
| U1 | Underspecification | LOW | `spec.md:L116` (SC-003) vs `tasks.md:L67, L102` (T006, T016) | Le critère SC-003 requiert une précision de mise à jour à la seconde avec un décalage inférieur à 1s par rapport à l'horloge locale. Les tests automatisés sous `pytest` valident statiquement la présence de l'algorithme dans le script JavaScript sans exécuter un moteur de rendu browser (respect de la Constitution V interdisant npm/Playwright). | Documenter explicitement que la validation dynamique temporelle à la seconde repose sur la procédure de vérification interactive (Scénarios 2 et 5 de `quickstart.md`), la couverture automatisée `pytest` garantissant l'intégrité algorithmique, les contrats ARIA et le rendu SSR. |

---

## 2. Coverage Summary Table

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|
| **FR-001** (Affichage dynamique dans `.quote-card` si `tasks >= 1`) | Oui | T007, T010, T011, T020 | Conteneur `#countdown-container` positionné à côté de la mascotte canine dans la carte de motivation. |
| **FR-002** (Masquage complet à l'état vide `tasks == 0`) | Oui | T012, T013, T014, T015 | Rendu conditionné côté serveur par `{% if tasks %}` dans Jinja2 et garde défensive dans `initCountdown()`. |
| **FR-003** (Indication du temps restant jusqu'à minuit local du jour suivant) | Oui | T008, T016, T017 | Calcul dynamique basé sur l'horloge locale (`now = new Date()`) ciblant `00:00:00` du jour calendaire suivant. |
| **FR-004** (Formatage textuel standardisé « HH h MM min SS s » avec zéros) | Oui | T008, T010, T016, T017 | Fonction pure `formatCountdown` avec `padStart(2, '0')` pour une largeur visuelle fixe sans décalage. |
| **FR-005** (Actualisation automatique chaque seconde sans rechargement) | Oui | T009, T010, T017, T025 | Boucle `setInterval` à 1 000 ms avec mise à jour immédiate au chargement initial. |
| **FR-006** (Continuité à minuit, 0 valeur négative, sans rechargement) | Oui | T016, T017, T025 | Algorithme `Math.max(0, target - now)` avec bascule autonome à 00:00:00 vers 23 h 59 min 59 s. |
| **FR-007** (Libellé WAI-ARIA explicite et interdiction d'annonces vocales par seconde) | Oui | T004, T018, T020 | Balise `<time>`, `aria-label`, `aria-live="off"`, `aria-hidden="true"` sur les chiffres et classe utilitaire `.sr-only`. |
| **FR-008** (Disposition responsive mobile et style chaleureux) | Oui | T011, T019, T021 | Flexbox adaptatif avec point de rupture `@media (max-width: 600px)` reprenant la palette chaleureuse. |
| **FR-009** (Exclusions : pas de chrono, alarme, choix de fuseau, persistance serveur) | Oui | T008, T017, T024 | Respecté nativement par conception : zéro persistance en base, zéro logique de chronomètre individuel. |
| **FR-010** (Exclusions : pas de réinitialisation ni modification des tâches à minuit) | Oui | T013, T017, T023 | Respecté nativement : l'écoulement temporel n'a aucun effet de bord sur le cycle de vie des tâches en base. |
| **SC-001** (100% des utilisateurs avec tâche voient le compte à rebours dès chargement) | Oui | T007, T010, T025 | Validé par test d'intégration HTTP Jinja2 et Scénario manuel 2. |
| **SC-002** (100% des utilisateurs sans tâche ne voient aucun compte à rebours) | Oui | T012, T014, T025 | Validé par tests HTTP d'état vide initial / suppression de dernière tâche et Scénarios manuels 1 et 3. |
| **SC-003** (Mise à jour chaque seconde avec écart < 1s par rapport à l'heure locale) | Oui | T008, T009, T017, T025 | Calcul instantané basé sur l'horloge système sans dérive cumulée, validé par Scénarios 2 et 5. |
| **SC-004** (Transition continue à minuit avec 0 valeur négative) | Oui | T016, T017, T025 | Validé par assertions algorithmiques dans `test_routes.py` et Scénario manuel 6. |
| **SC-005** (Affichage lisible et sans rupture visuelle de 320px à 2560px) | Oui | T019, T021, T025 | Validé par test de conformité CSS et validation sur émulateur mobile (Scénario 7). |
| **SC-006** (100% des utilisateurs de lecteurs d'écran ont accès au libellé sans annonce intempestive) | Oui | T018, T020, T025 | Validé par assertions WAI-ARIA (`aria-live="off"`, `aria-hidden="true"`) et Scénario manuel 7. |

---

## 3. Constitution Alignment Issues

**Résultat : 0 conflit constitutionnel.**

- **Principe I (Simplicité et Vocation Pédagogique)** : **CONFORME**. Architecture linéaire KISS/YAGNI, code JavaScript Vanilla épuré en fonctions pures modulaires (`calculateRemainingTime`, `formatCountdown`, `initCountdown`), absence totale de sur-ingénierie.
- **Principe II (Stack Web Épurée - HTML/CSS Natif & Backend Python avec Flask)** : **CONFORME**. Rendu principal assuré côté serveur par Flask SSR et Jinja2, balisage HTML5 sémantique, CSS natif sans préprocesseur, JavaScript Vanilla pur sans framework lourd (ni React, Vue, ou Alpine.js).
- **Principe III (Lisibilité et Documentation)** : **CONFORME**. Prévu en tâche T022 avec docstrings PEP 257 exhaustives, commentaires didactiques sur la gestion du temps absolu et l'accessibilité WAI-ARIA.
- **Principe IV (Tests Automatisés Obligatoires avec pytest)** : **CONFORME**. Approche TDD rigoureuse : toutes les tâches de tests automatisés (T003, T006, T007, T012, T013, T016, T018, T019) précèdent systématiquement l'implémentation du code correspondant.
- **Principe V (Minimalisme des Dépendances)** : **CONFORME**. Aucune dépendance externe additionnelle. `requirements.txt` conserve exclusivement `Flask` et `pytest`. Aucun outillage npm, bundler ou bibliothèque tierce n'est introduit (validé en T024).
- **Principe VI (Hygiène de Sécurité et Absence Totale de Données Sensibles)** : **CONFORME**. Zéro secret manipulé, calcul temporel strictement confiné au navigateur client, aucune persistance serveur de données d'horodatage.

---

## 4. Unmapped Tasks

Toutes les tâches définies dans `tasks.md` sont directement justifiées et rattachées :

- **Tâches d'infrastructure & configuration (Setup)** :
  - `T001` : Validation de l'environnement virtuel et de l'état initial des tests pytest (Principe IV).
  - `T002` : Création du sous-répertoire `app/static/js/` pour accueillir les scripts statiques.
- **Tâches fondamentales (Foundational)** :
  - `T003` : Test d'intégration de distribution des ressources statiques JavaScript par Flask.
  - `T004` : Déclaration de la classe universelle d'accessibilité `.sr-only` dans `style.css`.
  - `T005` : Ajout du bloc extensible `{% block scripts %}` dans `base.html` pour l'injection propre de scripts.
- **Tâches User Story 1 (P1 - MVP)** :
  - `T006` à `T011` : Tests TDD et implémentation du calcul temporel, de l'affichage dans `.quote-card` et des styles de base.
- **Tâches User Story 2 (P2)** :
  - `T012` à `T015` : Tests TDD et conditionnement Jinja2 pour l'état vide d'accueil et la persistance lors de la célébration 100%.
- **Tâches User Story 3 (P3)** :
  - `T016`, `T017` : Tests et consolidation algorithmique de la continuité fluide à minuit et de l'immunité au sommeil d'onglet.
- **Tâches User Story 4 (P4)** :
  - `T018` à `T021` : Tests TDD et implémentation du balisage d'accessibilité WAI-ARIA et de l'adaptation responsive mobile.
- **Tâches transversales de finition (Polish)** :
  - `T022` : Vérification PEP 257 et enrichissement didactique de la documentation (Principe III).
  - `T023` : Exécution complète de la suite `pytest` (Principe IV).
  - `T024` : Validation du maintien strict du minimalisme des dépendances dans `requirements.txt` (Principe V).
  - `T025` : Exécution des scénarios de validation manuelle de bout en bout (`quickstart.md`).

---

## 5. Metrics

- **Total Functional Requirements (FR)** : 10
- **Total Success Criteria (SC)** : 6
- **Total Requirements & Criteria** : 16
- **Total Tasks** : 25
- **Coverage %** : **100%** (16/16 exigences et critères disposent d'au moins une tâche de réalisation ou de validation)
- **Ambiguity Count** : 1 (emplacement exact de la balise `<script>` dans T007)
- **Duplication Count** : 2 (D1: double édition du gabarit en T010 et T020 ; D2: FR-001/FR-002 deux faces d'une même condition Jinja2)
- **Inconsistency Count** : 2 (I1: T007 vs T005 sur l'emplacement du script ; I2: `countdown-caption` vs `countdown-label`)
- **Critical Issues Count** : **0**

---

## 6. Next Actions

Le dossier de spécification et d'ingénierie `specs/005-end-of-day-countdown` présente une excellente qualité de conception, une cohérence technique remarquable, une conformité totale avec la Constitution du projet et une traçabilité intégrale (100% de couverture des exigences par les tâches).

- **Statut global** : **PRÊT POUR IMPLÉMENTATION** (`/speckit.implement`).
- **Actions d'amélioration recommandées avant / pendant implémentation** :
  1. *Ajustement T007* : Confirmer lors de l'implémentation que la balise `<script defer src="...">` est injectée via `{% block scripts %}` dans `index.html` (en fin de `base.html`) et non imbriquée dans le conteneur visuel `.quote-card`.
  2. *Optimisation T010 / T020* : Poser directement la structure WAI-ARIA complète dès T010 afin d'éviter une double intervention sur `app/templates/index.html`.
  3. Lancer la phase d'implémentation via `/speckit.implement`.

---

*Souhaitez-vous que je propose des modifications de remédiation concrètes pour les points identifiés ?*
