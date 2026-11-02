# Research & Technical Decisions: Compte à Rebours de Fin de Journée

**Feature**: `005-end-of-day-countdown` | **Date**: 2026-11-02

Ce document consigne les analyses techniques et les choix d'architecture retenus pour implémenter le compte à rebours dynamique de fin de journée dans l'application « Tâches du Jour ». Tous les choix sont rigoureusement alignés avec la Constitution du projet (simplicité didactique, stack HTML5/CSS3 native avec Flask, minimalisme des dépendances, accessibilité WAI-ARIA et tests automatisés `pytest`).

---

## Décision 1 : Architecture Script Client & Respect de la Constitution

- **Décision** : Implémenter le comportement dynamique en JavaScript natif moderne (Vanilla JS ES6+), sans aucun framework, bundler, bibliothèque tierce ou dépendance npm. Le code sera hébergé dans un fichier statique dédié `app/static/js/countdown.js` et chargé dans `app/templates/index.html` via une balise `<script defer src="{{ url_for('static', filename='js/countdown.js') }}"></script>`.
- **Détails techniques** :
  - Découpage en fonctions pures et modulaires : calcul du temps restant (`calculateRemainingTime`), formatage standardisé (`formatCountdown`), et boucle d'actualisation du DOM (`initCountdown`).
  - Utilisation de `defer` pour garantir le non-blocage de l'analyse du DOM HTML et l'exécution immédiate dès que le document est prêt.
  - Dégradation gracieuse : en cas de désactivation de JavaScript, l'interface HTML/CSS s'affiche et fonctionne normalement (ajout, complétion et suppression de tâches préservés).
- **Rationale** :
  - Respecte scrupuleusement les principes I (KISS), II (stack web épurée) et V (minimalisme des dépendances).
  - Aucune complexité d'outillage de build (aucun package.json, webpack, vite, ou node_modules).
  - Parfaitement didactique pour des apprenants souhaitant observer l'articulation entre Flask SSR et un script Vanilla JS ciblé.
- **Alternatives considérées** :
  - *Framework frontend réactif (React, Vue, Alpine.js)* : Rejeté car formellement proscrit par la Constitution (Principe II) et surdimensionné pour une horloge de quelques lignes.
  - *Bibliothèque de gestion de dates (Moment.js, date-fns, Day.js)* : Rejetée car l'objet standard `Date` de JavaScript fournit nativement toutes les primitives requises (Principe V).
  - *Script inline dans `index.html`* : Rejeté pour maintenir une séparation nette des responsabilités et faciliter la mise en cache navigateur et les tests statiques.

---

## Décision 2 : Emplacement DOM et Intégration Visuelle avec la Mascotte Canine

- **Décision** : Intégrer le composant compte à rebours au sein de la carte de motivation existante (`.quote-card`), positionné à proximité directe du badge de la mascotte canine (`.quote-icon`) et de la citation inspirante (`.quote-body`).
- **Détails techniques** :
  - Structure HTML du conteneur :
    ```html
    <div class="quote-countdown" id="countdown-container" role="region" aria-label="Temps restant avant la fin de la journée">
        <span class="countdown-label">Temps restant :</span>
        <time class="countdown-display" aria-live="off">
            <span id="countdown-text" aria-hidden="true">-- h -- min -- s</span>
            <span class="sr-only">Temps restant avant la fin de la journée</span>
        </time>
    </div>
    ```
  - Agencement CSS (`app/static/css/style.css`) s'appuyant sur Flexbox avec adaptabilité responsive :
    - Sur grand écran : disposition harmonieuse en bloc secondaire équilibré au sein de `.quote-card`.
    - Sur écran mobile (< 600px) : réalignement vertical fluide sans débordement ni rupture typographique (SC-005).
    - Palette visuelle : couleurs chaudes, bordures douces et typographie fidèle à la charte graphique existante.
- **Rationale** :
  - Répond directement à l'exigence fonctionnelle FR-001 (« visible dans la carte du message de motivation, à côté de l'illustration du chien qui encourage »).
  - Associe sémantiquement l'encouragement du chien à la notion de temps restant pour accomplir ses objectifs du jour.
- **Alternatives considérées** :
  - *Bannière flottante distincte ou en-tête fixe* : Rejetée car elle encombrerait l'interface, générerait une pression visuelle excessive et s'éloignerait de l'esprit bienveillant du projet.
  - *Intégration dans la barre de progression* : Rejetée car la jauge mesure le volume des tâches accomplies (pourcentage), alors que le décompte mesure le temps calendaire restant.

---

## Décision 3 : Pilotage de la Visibilité (Jinja2 Serveur vs Masquage Client)

- **Décision** : Piloter la présence du compte à rebours côté serveur via le moteur Jinja2 avec la condition `{% if tasks %}...{% endif %}`, complétée par une garde défensive côté JavaScript.
- **Détails techniques** :
  - Côté serveur : le bloc `#countdown-container` et l'inclusion du script `countdown.js` sont encapsulés dans la condition `{% if tasks %}`. Si `len(tasks) == 0` (état vide), le balisage du décompte n'est pas injecté dans le flux HTML.
  - Côté client : la fonction d'initialisation `initCountdown()` vérifie d'emblée la présence de l'élément dans le DOM (`const container = document.getElementById('countdown-container'); if (!container) return;`).
- **Rationale** :
  - Garantit l'absence totale de compte à rebours à l'état vide d'accueil (FR-002, SC-002).
  - Évite tout clignotement d'affichage (*Flash of Unstyled Content* - FOUC) au chargement de la page.
  - Économise les ressources système : aucun `setInterval` n'est déclenché en arrière-plan lorsque la liste de tâches est vide.
  - Cohérence avec le patron Post/Redirect/Get : lors de l'ajout de la première tâche ou de la suppression de la dernière, Flask régénère la page complète avec le bon état de rendu.
- **Alternatives considérées** :
  - *Masquage 100% en JavaScript via `style.display = 'none'`* : Rejeté car cela impliquerait d'injecter du balisage inutile sur l'état vide et risquerait de laisser subsister des fuites de timer.

---

## Décision 4 : Accessibilité ARIA et Prévention de la Pollution Vocale

- **Décision** : Structurer le composant avec la balise sémantique HTML5 `<time>`, un attribut d'accessibilité statique `aria-label="Temps restant avant la fin de la journée"`, l'exclusion stricte de tout mode `aria-live` dynamique (`aria-live="off"`), et le masquage des chiffres itératifs aux lecteurs d'écran via `aria-hidden="true"`.
- **Détails techniques** :
  - Utilisation d'un texte statique caché pour les synthèses vocales : `<span class="sr-only">Temps restant avant la fin de la journée</span>`.
  - La valeur textuelle actualisée chaque seconde (`05 h 32 min 10 s`) est isolée dans un `<span id="countdown-text" aria-hidden="true">`.
  - Exclusion formelle de `role="timer"` combiné avec `aria-live="polite"` ou `aria-live="assertive"`.
- **Rationale** :
  - Conforme aux exigences FR-007 et SC-006.
  - Si un composant dynamique utilisait `aria-live="polite"`, les lecteurs d'écran vocaliseraient le changement de valeur à chaque seconde, rendant l'application inaudible et inexploitable pour les personnes déficientes visuelles.
  - Les utilisateurs de lecteurs d'écran entendent le libellé clair de l'indicateur lors de leur parcours tabulaire ou linéaire sans être perturbés en continu.
- **Alternatives considérées** :
  - *Attribut `role="timer"` standard* : Beaucoup de navigateurs et aides techniques associent automatiquement `role="timer"` à un canal d'alerte, provoquant des annonces intempestives selon les configurations. La balise `<time>` avec `aria-live="off"` est plus fiable et universellement supportée.

---

## Décision 5 : Algorithme Temporel, Résilience au Bridage et Transition à Minuit

- **Décision** : Calculer à chaque seconde l'écart temporel en valeur absolue par rapport à l'horloge système locale (`new Date()`), cibler dynamiquement le minuit local suivant, et formater le résultat en `HH h MM min SS s` avec complétion par zéros (`padStart(2, '0')`).
- **Détails techniques** :
  - Détermination de l'instant courant : `const now = new Date()`.
  - Calcul de l'échéance cible (minuit local du jour suivant) :
    `const target = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1, 0, 0, 0, 0)`.
  - Différence en millisecondes : `const diff = Math.max(0, target.getTime() - now.getTime())`.
  - Décomposition arithmétique :
    - `hours = Math.floor(diff / (1000 * 60 * 60)) % 24`
    - `minutes = Math.floor(diff / (1000 * 60)) % 60`
    - `seconds = Math.floor(diff / 1000) % 60`
  - Chaîne formatée : `${String(hours).padStart(2, '0')} h ${String(minutes).padStart(2, '0')} min ${String(seconds).padStart(2, '0')} s`.
  - Transition continue à minuit (00:00:00) : Dès que `now` passe à 00:00:00, `target` calcule automatiquement le minuit du jour d'après (+1 jour), affichant directement `23 h 59 min 59 s` sans valeur négative (FR-006, SC-004).
  - Gestion du bridage des navigateurs (*timer throttling*) lors de la mise en veille ou en arrière-plan d'onglet : Le calcul n'étant pas une décrémentation incrémentale d'un compteur interne mais une différence instantanée sur l'horloge système, le décompte affiche instantanément l'heure exacte dès le réveil de l'onglet sans retard cumulé (Edge Case 1).
- **Rationale** :
  - Zéro dérive temporelle : exactitude absolue à chaque rafraîchissement d'affichage.
  - Résilience totale face aux changements d'heure saisonniers (DST) ou ajustements d'horloge locale par l'utilisateur.
  - Simplicité mathématique limpide ne nécessitant aucun composant externe.
- **Alternatives considérées** :
  - *Décrémenter un entier `secondsLeft--` à chaque seconde via `setInterval`* : Rejeté car les onglets inactifs subissent un bridage d'exécution (ralentissement à 1 tick par minute), provoquant un décalage massif de plusieurs dizaines de minutes lors de la reprise.
  - *Requête Ajax/API vers le backend pour obtenir l'heure du serveur* : Rejetée car la spécification exige explicitement l'heure locale de l'utilisateur (FR-003, FR-009) et aucune synchronisation réseau superflue.

---

## Décision 6 : Stratégie de Test et Contrôle Qualité avec pytest

- **Décision** : Tester la logique applicative et l'intégration des gabarits Flask avec `pytest` (`tests/test_routes.py`), complété par des tests de distribution des ressources statiques et de conformité du balisage ARIA.
- **Cas couverts** :
  1. **Condition de visibilité Jinja2** :
     - Vérifier que `GET /` sans tâche ne contient ni `#countdown-container`, ni `countdown.js`.
     - Vérifier que `GET /` avec au moins une tâche contient l'élément `#countdown-container` et la balise de script.
     - Vérifier la persistance du compte à rebours même lorsque toutes les tâches sont complétées (100% avec bannière de fête).
  2. **Vérification des contrats d'accessibilité et de sémantique** :
     - Vérifier la présence de `aria-label="Temps restant avant la fin de la journée"`.
     - Vérifier la présence de `aria-live="off"`.
     - Vérifier la présence de la classe `.sr-only` et de l'attribut `aria-hidden="true"`.
  3. **Vérification de la distribution des fichiers statiques** :
     - `GET /static/js/countdown.js` retourne HTTP 200 avec le type MIME `text/javascript` ou `application/javascript`.
     - Vérification de la présence des fonctions clés (`calculateRemainingTime`, `formatCountdown`, `initCountdown`) dans le script statique.
- **Rationale** :
  - Respect strict du principe constitutionnel IV (tests pytest obligatoires et statut vert).
  - Permet d'assurer une couverture CI complète sans introduire d'exécuteur de test JavaScript lourd (comme Jest ou Vitest), en cohérence avec le minimalisme des dépendances.
