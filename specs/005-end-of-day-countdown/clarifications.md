# Clarifications de Spécification : Compte à Rebours de Fin de Journée

**Dossier de fonctionnalité** : `specs/005-end-of-day-countdown`  
**Date** : 2026-11-02  
**Statut** : Clôturé (Mode non interactif)  
**Document source analysé** : `specs/005-end-of-day-countdown/spec.md`

---

### 1. Modalité d'intégration technique du script côté client et respect de la Constitution (FR-005, Contraintes)

**Question :** Quelle technologie et quelle structure de fichier doivent être employées pour l'actualisation dynamique du compte à rebours chaque seconde, tout en respectant scrupuleusement la Constitution du projet (zéro framework lourd, minimalisme des dépendances) ? (FR-005)

- **Pourquoi c'est important :** Le projet repose actuellement sur une pile 100% HTML5/CSS3 natif et Python/Flask, sans aucun script JavaScript dans le dépôt. La Constitution proscrit les frameworks lourds (React, Vue, Angular) et impose la simplicité pédagogique. Il est indispensable de définir précisément comment le script dynamique est introduit, hébergé et exécuté sans ajouter de dépendance tierce (ni bundler, ni gestionnaire de paquets npm, ni CDN).
- **Réponse par défaut proposée :** Utiliser exclusivement du JavaScript natif (Vanilla JS moderne ES6+), sans aucune bibliothèque externe, compilateur ou dépendance npm. Le code sera consigné dans un fichier statique dédié `app/static/js/countdown.js`, inclus dans le gabarit `app/templates/index.html` via une balise standard `<script defer src="...">`. Si JavaScript est désactivé sur le navigateur du client, la page continue de s'afficher et de fonctionner normalement sans bloquer l'accès aux tâches (dégradation gracieuse).
- **Impact :**
  - *Architecture & Frontend :* Création de l'arborescence `app/static/js/` et du script `app/static/js/countdown.js`. Liaison dans le template `index.html`.
  - *Conformité Constitution :* Respect absolu des principes II (stack web épurée) et V (minimalisme des dépendances).
  - *Tests :* Tests d'intégration Flask validant le bon référencement de la ressource statique dans le template HTML et la conformité du code d'état HTTP 200 sur son téléchargement.

---

### 2. Emplacement précis dans le DOM et articulation visuelle avec la mascotte canine (FR-001, FR-008)

**Question :** Quel doit être le positionnement HTML précis du compte à rebours au sein de la carte de motivation (`.quote-card`) et comment s'articule-t-il visuellement avec l'icône canine existante ? (FR-001)

- **Pourquoi c'est important :** La spécification indique que le compte à rebours est placé « à côté de l'illustration du chien qui encourage » dans la carte de motivation. Actuellement, la section `.quote-card` est composée d'un badge émoji `.quote-icon` (`🐶`) et d'un conteneur `.quote-body` avec la citation. Sans ciblage structurel clair, l'ajout du composant pourrait déstructurer la grille CSS ou entrer en conflit avec les marges et l'alignement sur écran mobile.
- **Réponse par défaut proposée :** Le compte à rebours sera intégré à l'intérieur de la balise `<section class="quote-card">`, sous la forme d'un bloc distinct `<div class="quote-countdown" id="countdown-container">` disposé en regard ou sous la citation, aligné visuellement avec le repère canin `.quote-icon`. Le style CSS s'appuiera sur Flexbox avec une disposition adaptée sur mobile (passage vertical fluide en dessous de 600px de large) tout en reprenant la palette chaleureuse et bienveillante existante.
- **Impact :**
  - *Frontend & Template :* Insertion d'un élément `<div class="quote-countdown" id="countdown-container">...</div>` dans `app/templates/index.html`.
  - *Design & Styles CSS :* Définition de styles dédiés dans `app/static/css/style.css` garantissant la cohérence visuelle, la flexibilité responsive et l'absence de débordement sur petit écran (SC-005).
  - *Tests :* Assertions dans les tests de templates vérifiant la présence du conteneur `#countdown-container` au sein de la section `.quote-card`.

---

### 3. Pilotage de la condition de visibilité : rendu conditionnel serveur (Jinja2) vs masquage client (FR-001, FR-002, SC-002)

**Question :** La condition d'apparition ou de masquage complet du compte à rebours (« visible dès qu'au moins une tâche existe, masqué à l'état vide ») doit-elle être pilotée côté serveur via le moteur Jinja2 ou par manipulation du DOM côté client ? (FR-002)

- **Pourquoi c'est important :** Les opérations de gestion des tâches (création, complétion, suppression) passent toutes par des soumissions de formulaires HTTP POST suivies de redirections (patron PRG) rechargeant la vue principale. Décider si Jinja2 pilote la présence du nœud HTML évite des traitements superflus en JavaScript, supprime tout risque de clignotement visuel (FOUC) et garantit que l'état vide ne charge ni n'exécute d'horloge inutile.
- **Réponse par défaut proposée :** Le contrôle de visibilité est assuré directement côté serveur par le moteur Jinja2 via la condition `{% if tasks %}...{% endif %}`. Lorsque la liste de tâches est vide (`len(tasks) == 0`), le bloc HTML du compte à rebours et le script d'animation ne sont pas insérés dans la page. Dès qu'au moins une tâche est enregistrée, Jinja2 instancie le bloc dans le DOM, déclenchant l'exécution immédiate du timer client.
- **Impact :**
  - *Backend & Gabarit Jinja2 :* Encapsulation du composant dans `{% if tasks %}` au sein de `app/templates/index.html`.
  - *Performance & Fiabilité :* Aucun timer JS actif en état d'accueil vide ; zéro fuite mémoire ou consommation CPU sur une page sans tâche.
  - *Tests automatisés (pytest) :* Validation unitaire simple et déterministe dans `test_routes.py` vérifiant que `client.get("/")` ne contient pas `#countdown-container` lorsque la base est vide, et le contient dès qu'une tâche est ajoutée.

---

### 4. Sémantique HTML5 et politique d'accessibilité ARIA contre la pollution vocale (FR-004, FR-007, SC-006)

**Question :** Quelle structure sémantique HTML5 et quels attributs ARIA doivent être appliqués au compte à rebours pour offrir un libellé clair aux technologies d'assistance sans provoquer de vocalisation intempestive à chaque seconde écoulée ? (FR-007)

- **Pourquoi c'est important :** Les critères FR-007 et SC-006 imposent un libellé explicite (« Temps restant avant la fin de la journée ») tout en interdisant formellement les annonces vocales cadencées seconde par seconde. Si un développeur utilisait par mégarde `role="timer"` avec un attribut `aria-live="polite"` ou `aria-live="assertive"`, les synthèses vocales interrompraient la lecture de l'utilisateur à chaque seconde, rendant l'interface inutilisable pour les personnes malvoyantes.
- **Réponse par défaut proposée :** Utiliser la balise native `<time>` accompagnée d'un attribut `aria-label="Temps restant avant la fin de la journée"` statique, avec omission stricte de tout attribut `aria-live` actif (ou utilisation explicite de `aria-live="off"`). Le texte dynamique mis à jour chaque seconde dans le DOM (ex. `05 h 32 min 10 s`) sera contenu dans un `<span>` balisé avec `aria-hidden="true"`, afin que les lecteurs d'écran lisent uniquement le libellé sémantique lors de l'exploration de la carte sans subir de notifications itératives.
- **Impact :**
  - *Accessibilité & HTML :* Structure conforme :
    ```html
    <div class="quote-countdown" role="region" aria-label="Temps restant avant la fin de la journée">
        <span class="countdown-caption">Temps restant :</span>
        <time class="countdown-display" aria-live="off">
            <span id="countdown-text" aria-hidden="true">-- h -- min -- s</span>
            <span class="sr-only">Temps restant avant la fin de la journée</span>
        </time>
    </div>
    ```
  - *Conformité :* Garantie à 100% du respect des critères SC-006 et FR-007.
  - *Tests :* Vérification dans la suite de tests de la présence de `aria-label`, de l'absence de `aria-live="polite"` et de l'inclusion de la classe d'accessibilité `.sr-only`.

---

### 5. Algorithme de calcul temporel, résilience au bridage d'onglet et transition continue à minuit (FR-003, FR-006, SC-004)

**Question :** Quel algorithme de calcul de la durée restante doit être implémenté côté client pour éviter la dérive temporelle lors de la mise en arrière-plan de l'onglet et assurer une transition fluide à minuit (00:00:00) sans affichage de valeurs négatives ? (FR-006)

- **Pourquoi c'est important :** Un décompte naïf décrémentant une variable entière chaque seconde via `setInterval` subit inévitablement l'étranglement d'exécution (*timer throttling*) imposé par les navigateurs sur les onglets inactifs, générant un retard cumulatif dès que l'utilisateur change d'onglet. Par ailleurs, lors du passage exact de minuit, si la date cible n'est pas recalculée dynamiquement sur le nouveau minuit, le calcul de différence temporelle devient négatif, violant FR-006 et SC-004.
- **Réponse par défaut proposée :** Le calcul sera basé sur l'horloge système absolue à chaque exécution du timer (`new Date()`). À chaque seconde, le script détermine l'instant présent `now = new Date()`, définit l'échéance de fin de journée au minuit suivant `target = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1, 0, 0, 0, 0)`, et calcule l'écart `diff = Math.max(0, target - now)`. Dès que `now` bascule sur le nouveau jour (00:00:00), `target` avance automatiquement sur le minuit d'après, enchaînant instantanément sur `23 h 59 min 59 s` sans valeur négative et sans nécessiter de rafraîchissement. Les composants heures, minutes et secondes sont complétés par un zéro initial (`padStart(2, '0')`) pour respecter scrupuleusement le gabarit `HH h MM min SS s`.
- **Impact :**
  - *Robustesse du script :* Immunité complète contre le throttling des navigateurs lors de la mise en veille ou mise en arrière-plan (reprise immédiate à la seconde exacte lors du réveil de l'onglet).
  - *Continuité :* Respect parfait de FR-004 (formatage avec zéros initiaux) et de FR-006 / SC-004 (zéro valeur négative, continuité parfaite à minuit).
  - *Tests :* Définition de cas de tests exhaustifs pour les fonctions de calcul et de formatage temporel couvrant les cas limites (23:59:59, 00:00:00, et reprises d'onglets inactifs).
