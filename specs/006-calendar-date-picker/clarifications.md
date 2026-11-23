# Clarifications de Spécification : Calendrier et Marquage de Dates

**Dossier de fonctionnalité** : `specs/006-calendar-date-picker`  
**Date** : 2026-11-23  
**Statut** : Clôturé (Mode non interactif)  
**Document source analysé** : `specs/006-calendar-date-picker/spec.md`

---

### 1. Fichier de persistance et modèle de stockage des dates cochées (FR-006, Entités Clés)

**Question :** Où et sous quelle structure de données les dates cochées doivent-elles être enregistrées côté backend pour assurer leur persistance sans interférer avec la gestion des tâches quotidiennes ? (FR-006)

- **Pourquoi c'est important :** La spécification mentionne une persistance locale dans le système de persistance du projet (fichier JSON dans `data/`), mais ne tranche pas entre une mutualisation au sein de `data/tasks.json` ou la création d'un fichier dédié (ex. `data/calendar.json`). Mutualiser les dates dans le fichier des tâches violerait le principe de responsabilité unique (SRP), compliquerait les schémas de données et risquerait de corrompre l'historique des tâches en cas d'accès concurrent.
- **Réponse par défaut proposée :** Créer un fichier de persistance dédié `data/calendar.json` administré par une classe dédiée `CalendarManager` dans `app/models.py`. Le modèle de données stocke les dates cochées sous la forme d'un dictionnaire indexé par la date au format ISO `YYYY-MM-DD` contenant le statut actif (`checked: True`) et l'horodatage UTC de mise à jour (`updated_at`), ou d'une liste structurée de `CheckedDate`. Lorsqu'une date est décochée, son état bascule à `checked: False` ou elle est purgée du registre actif pour maintenir un fichier compact et lisible.
- **Impact :**
  - *Architecture & Backend* : Ajout de la classe `CalendarManager` et de la dataclass `CheckedDate` dans `app/models.py`, avec gestion de son propre fichier de données (configurable via `current_app.config["CALENDAR_DATA_FILE"]`).
  - *Robustesse & Isolation* : Aucune régression possible sur `TaskManager` ni sur `data/tasks.json`.
  - *Tests* : Tests unitaires dédiés dans `tests/test_models.py` validant la sérialisation, la désérialisation, le basculement d'état et la résilience aux corruptions de fichier pour `CalendarManager`.

---

### 2. Protocole de communication et réactivité du cochage/décochage sous 150 ms (FR-004, SC-002, FR-011)

**Question :** Quelle signature de route HTTP et quel mécanisme d'échange client/serveur doivent être employés pour cocher et décocher une date tout en respectant l'objectif d'interaction sous 150 ms (SC-002) et le minimalisme technique sans framework lourd (FR-011) ? (FR-004)

- **Pourquoi c'est important :** L'application utilise actuellement un rechargement de page complet (patron Post/Redirect/Get) lors de l'ajout ou de la complétion d'une tâche. Cependant, un rechargement synchrone de la page à chaque clic sur une case du calendrier provoquerait un scintillement visuel, une réinitialisation de la position de défilement et dépasserait très probablement le seuil strict de 150 ms fixé par SC-002.
- **Réponse par défaut proposée :** Mettre en place un point de terminaison HTTP `POST /calendar/toggle` acceptant une charge JSON `{"date": "YYYY-MM-DD"}` (ou des paramètres de formulaire standard) et retournant une réponse JSON `{ "date": "YYYY-MM-DD", "checked": true, "month_checked_count": 3 }`. Côté navigateur, un script Vanilla JS moderne (`app/static/js/calendar.js`) écoute les clics/touches clavier sur les cellules de date, applique immédiatement une mise à jour optimiste du DOM (bascule de la classe visuelle et du symbole patte 🐾 en < 20 ms), puis envoie la requête asynchrone via l'API standard `fetch()`. En cas d'erreur réseau, le script restaure l'état visuel précédent et avertit l'utilisateur sans bloquer l'interface.
- **Impact :**
  - *Backend & Routage* : Déclaration de `@bp.route("/calendar/toggle", methods=["POST"])` dans `app/routes.py` retournant une charge utile JSON (`jsonify`).
  - *Frontend & Script* : Création de `app/static/js/calendar.js` en Vanilla JS (ES6+ natif, zéro dépendance tierce conformément au principe V de la Constitution).
  - *Performance & UX* : Respect immédiat du critère SC-002 (< 150 ms) avec mise à jour instantanée du compteur mensuel de jours cochés sans rechargement de page.
  - *Tests* : Tests d'intégration Flask vérifiant la réponse JSON, les codes d'état HTTP (200 en succès, 400 si date invalide, 405 si méthode GET) et la persistance effective.

---

### 3. Stratégie de navigation entre les mois et validation défensive des paramètres temporels (FR-007, SC-004)

**Question :** Comment la navigation entre les mois (précédent, suivant, retour à aujourd'hui) doit-elle être orchestrée techniquement, et quelle stratégie de repli appliquer en cas de paramètres temporels anormaux ou hors limites ? (FR-007)

- **Pourquoi c'est important :** La navigation temporelle peut être gérée soit par rechargement complet de la page via paramètres d'URL (ex: `/?year=2026&month=12`), soit via chargement dynamique asynchrone d'une sous-vue ou de données JSON. Par ailleurs, des valeurs aberrantes ou malveillantes (ex: `month=13`, `year=-50`, `year=abc`) transmises via la requête GET pourraient faire crasher la logique de calcul de date serveur avec une erreur 500.
- **Réponse par défaut proposée :** Adopter une navigation serveur standard basée sur les paramètres d'URL `GET /?year=<YYYY>&month=<MM>` (ou route dédiée `GET /calendar?year=<YYYY>&month=<MM>`), assurant le rendu initial côté serveur (SSR) et permettant le partage ou la mise en favori d'un mois spécifique. Une validation défensive stricte est appliquée : si les paramètres `year` ou `month` sont absents, non convertibles en entiers, ou hors des limites valides (mois non compris entre 1 et 12, année non comprise entre 1970 et 2100), le contrôleur retombe silencieusement et de manière robuste sur l'année et le mois courants (`datetime.now().year`, `datetime.now().month`). Le script `calendar.js` peut intercepter les liens de navigation pour mettre à jour la grille de manière fluide sans à-coup.
- **Impact :**
  - *Robustesse & Sécurité* : Aucun crash serveur (500) sur des requêtes malformées ; assainissement strict des types entiers.
  - *Accessibilité & Dégradation gracieuse* : La navigation fonctionne parfaitement même si JavaScript est désactivé sur le navigateur.
  - *Tests* : Cas de tests automatisés couvrant les paramètres valides, les transitions d'années (décembre <-> janvier), les années bissextiles (février 29 jours), et les valeurs limites/invalides (`month=99`, `year=invalid`).

---

### 4. Positionnement structurel du calendrier dans l'interface `index.html` et ergonomie mobile (FR-001, FR-010)

**Question :** Quel doit être l'emplacement précis du calendrier au sein de la page d'accueil `app/templates/index.html` par rapport aux blocs existants (carte de citation/countdown, formulaire d'ajout, progression, liste des tâches) afin de préserver l'ergonomie globale ? (FR-001)

- **Pourquoi c'est important :** La vocation première de l'application est la planification et le suivi des tâches immédiates du jour. Si le calendrier était inséré en tête de page (au-dessus du formulaire ou de la liste), il monopoliserait l'espace vertical (en particulier sur écran mobile de 360px de large) et repousserait les missions quotidiennes en dehors du champ visuel initial de l'utilisateur.
- **Réponse par défaut proposée :** Positionner la section du calendrier sous la liste des tâches (`.task-list-section`), sous la forme d'une section dédiée `<section class="calendar-section" aria-label="Calendrier et suivi des dates">`. Ce positionnement maintient la priorité ergonomique sur la saisie et le pointage des tâches du jour tout en conférant au calendrier une zone autonome, aérée et bien identifiée. Une ancre ou un bouton d'accès rapide dans l'en-tête peut éventuellement permettre de faire défiler la vue directement vers le calendrier.
- **Impact :**
  - *Frontend & Template* : Intégration d'un bloc `<section class="calendar-section">` propre à la fin du flux principal dans `app/templates/index.html`.
  - *Design CSS Responsive* : Styles spécifiques dans `app/static/css/style.css` garantissant une grille CSS régulière (7 colonnes flexibles) sans dépassement horizontal ni sur mobile (320px-360px) ni sur grand écran (SC-006, FR-010).
  - *Tests* : Vérification de la présence de la balise `<section class="calendar-section">` et de ses attributs d'accessibilité dans les tests de rendu de template.

---

### 5. Harmonisation de la date « Aujourd'hui » entre fuseau serveur et horloge locale client (FR-003, Assumptions)

**Question :** Comment garantir que la date mise en valeur sous l'étiquette « Aujourd'hui » (FR-003) corresponde exactement au jour calendaire réel de l'utilisateur, notamment en cas de décalage de fuseau horaire avec le serveur d'hébergement ? (FR-003)

- **Pourquoi c'est important :** Le serveur Python Flask s'exécute généralement configuré sur l'heure UTC (ou l'heure du système hôte/conteneur Docker). Entre 23h00 et minuit dans le fuseau horaire de l'utilisateur, ou selon la localisation de l'apprenant, la date UTC peut différer de sa date locale. Si la mise en valeur visuelle de « Aujourd'hui » repose exclusivement sur le serveur, l'utilisateur pourrait voir le jour précédent ou suivant mis en surbrillance.
- **Réponse par défaut proposée :** Le serveur génère la grille avec une estimation initiale basée sur la date courante du système serveur (`datetime.now()`). Côté client, le script `calendar.js` lit la date locale réelle du terminal de l'utilisateur via `new Date()`, compare l'identifiant de date calendaire (`YYYY-MM-DD`), et applique dynamiquement la classe CSS `.is-today` ainsi que l'annonce d'accessibilité (`Aujourd'hui`) sur la cellule correspondante du mois affiché. Ainsi, la date mise en relief est garantie 100% fidèle au fuseau local de l'utilisateur.
- **Impact :**
  - *Fiabilité UX* : Élimination de toute confusion calendaire lors des utilisations nocturnes ou en mobilité internationale.
  - *Accessibilité* : L'attribut `aria-label` de la date courante mentionne explicitement « Aujourd'hui » pour les technologies d'assistance.
  - *Tests* : Tests unitaires Python vérifiant le calcul de la date serveur et tests fonctionnels/DOM validant le marquage dynamique de la classe `.is-today`.
