# Research & Technical Decisions: Suppression de Tâche Individuelle

**Feature**: `004-delete-task` | **Date**: 2026-10-24

Ce document synthétise les analyses techniques et les décisions architecturales retenues pour mettre en œuvre la suppression individuelle d'une tâche quotidienne. Tous les choix sont rigoureusement alignés avec la constitution du projet (simplicité didactique, Flask SSR, HTML5/CSS3 natif sans JavaScript, absence de dépendances superflues et couverture exhaustive par `pytest`).

---

## Décision 1 : Point d'accès HTTP et Patron Post/Redirect/Get (PRG)

- **Décision** : Déclarer un point d'accès dédié `POST /tasks/<task_id>/delete` dans `app/routes.py`, restreint strictement à la méthode `POST`, appliquant le patron Post/Redirect/Get avec une redirection HTTP 302 vers la racine (`/`).
- **Détails techniques** :
  - Décorateur de route : `@bp.route("/tasks/<task_id>/delete", methods=["POST"])`.
  - Toute requête utilisant une autre méthode (notamment `GET`) est automatiquement rejetée par Flask avec le code `405 Method Not Allowed`.
  - La redirection s'effectue via `return redirect(url_for("main.index"))`.
  - Aucune notification temporaire (message flash) n'est émise : la suppression est immédiate et silencieuse (conformément à la clarification #3 et à l'ergonomie de la route `/complete`).
- **Rationale** :
  - Respecte scrupuleusement le patron Post/Redirect/Get (FR-006, SC-004) pour prévenir toute re-soumission accidentelle lors d'un rafraîchissement navigateur (F5).
  - L'interdiction absolue de la méthode `GET` protège contre la suppression involontaire de tâches causée par les mécanismes de préchargement des navigateurs ou les robots d'indexation.
  - S'intègre directement avec les formulaires HTML5 natifs sans aucun script JavaScript.
- **Alternatives considérées** :
  - *Méthode HTTP `DELETE` (`DELETE /tasks/<task_id>`)* : Rejetée car les formulaires HTML natifs ne supportent que `GET` et `POST`. L'utilisation de `DELETE` nécessiterait soit du JavaScript (`fetch`), soit un middleware de réécriture de méthode (`_method=DELETE`), ce qui violerait le principe constitutionnel II (stack web épurée) et I (KISS).
  - *Lien hypertexte simple (`<a href="/tasks/.../delete">`)* : Rejeté car les requêtes `GET` doivent être sûres (*safe* au sens RFC 7231) et ne doivent jamais déclencher de mutation destructrice de données.
  - *Notification Flash après suppression* : Rejetée car la mise à jour visuelle immédiate de la liste et de la jauge est auto-porteuse ; l'affichage d'un message flash superflu encombrerait l'interface.

---

## Décision 2 : Persistance et Couche Modèle (`TaskManager`)

- **Décision** : Exploiter la méthode `delete_task(task_id: str) -> bool` de la classe `TaskManager` dans `app/models.py`.
- **Détails techniques** :
  - La méthode filtre la liste des tâches existantes : `tasks = [task for task in tasks if task.id != task_id]`.
  - Si la longueur de la liste est réduite, la persistance locale dans `data/tasks.json` est réécrite de manière synchrone et la méthode retourne `True`.
  - Si l'identifiant n'est pas trouvé, le fichier n'est pas modifié et la méthode retourne `False`.
- **Rationale** :
  - Réutilise la logique métier native et unitaire déjà implémentée dans `app/models.py`.
  - Garantit une suppression définitive de la persistance locale conformément à l'exigence fonctionnelle FR-002.
  - Préserve l'intégrité et l'ordre chronologique de création des autres tâches.
- **Alternatives considérées** :
  - *Suppression logique ("Soft Delete" avec indicateur `deleted: bool`)* : Rejetée car la spécification exige formellement une suppression définitive sans corbeille de récupération, et l'entité JSON doit rester minimaliste.

---

## Décision 3 : Traitement des Cas d'Erreur et Idempotence

- **Décision** : Traiter les identifiants de tâches inexistants, déjà supprimés ou mal formés par une redirection silencieuse HTTP 302 vers `/`, sans déclencher d'exception non gérée ni d'erreur HTTP 500, ni afficher d'écran 404.
- **Détails techniques** :
  - Dans la vue Flask `delete_task(task_id)` :
    ```python
    manager = get_task_manager()
    manager.delete_task(task_id)
    return redirect(url_for("main.index"))
    ```
  - Que la méthode renvoie `True` ou `False`, la réponse est identique (redirection vers `main.index`).
- **Rationale** :
  - Garantit l'idempotence fonctionnelle pour l'utilisateur final : si la tâche ciblée a déjà été supprimée (double-clic rapide, onglet de navigateur ouvert en parallèle), l'état final attendu (la tâche n'est plus visible dans la liste) est déjà atteint.
  - Conforme aux exigences FR-007 et SC-006 (zéro crash applicatif ou erreur 500).
- **Alternatives considérées** :
  - *Retourner un code HTTP 404 Not Found* : Rejeté car cela interromprait inutilement la session de l'utilisateur sur une page d'erreur alors que l'application peut simplement réafficher la liste à jour.
  - *Émettre un message flash d'erreur* : Rejeté car un double-clic involontaire ou une suppression normale ne doit pas générer d'alerte agressive.

---

## Décision 4 : Ergonomie, Accessibilité ARIA et Présentation UI

- **Décision** : Intégrer sur chaque carte de tâche (`<li class="task-item">`) un formulaire HTML autonome avec un bouton d'action dédié à la suppression, accessible au clavier et doté d'un attribut `aria-label` individualisé.
- **Détails techniques** :
  - Structure HTML dans `app/templates/index.html` :
    ```html
    <form action="{{ url_for('main.delete_task', task_id=task.id) }}" method="POST" class="delete-form">
        <button type="submit" 
                class="btn-delete" 
                aria-label="Supprimer la tâche : {{ task.title }}"
                title="Supprimer la tâche">
            <span class="delete-icon" aria-hidden="true">🗑️</span>
        </button>
    </form>
    ```
  - Le bouton est focalisable au clavier via la touche Tabulation et activable via Entrée ou Espace (comportement standard HTML `<button type="submit">`).
  - Le bouton de suppression reste **toujours actif** (`disabled` n'est jamais posé), y compris sur les tâches complétées (`is-completed`), pour permettre de retirer une tâche déjà accomplie (clarification #5).
  - Absence délibérée de boîte de dialogue modale de confirmation (conformément au périmètre exclu FR-009).
- **Rationale** :
  - Conforme aux critères d'accessibilité numérique WAI-ARIA (FR-008, SC-005).
  - Respecte la constitution : zéro dépendance JavaScript externe, ergonomie directe.
  - Styles CSS sobres et harmonieux alignés avec la charte graphique canin-pédagogique existante (`style.css`).
- **Alternatives considérées** :
  - *Boîte modale de confirmation JavaScript (`confirm()`)* : Rejetée car formellement hors périmètre (FR-009) et contraire à la règle d'absence de JS superflu.
  - *Bouton désactivé sur les tâches terminées* : Rejeté car l'utilisateur doit pouvoir faire le ménage parmi ses tâches terminées sans contrainte.

---

## Décision 5 : Interaction avec le Suivi de Progression et l'État Vide

- **Décision** : S'appuyer sur le cycle de vie naturel du rendu côté serveur (SSR) : lors de la redirection sur `GET /`, `TaskManager.get_progress()` et `TaskManager.get_all_tasks()` recalculent instantanément les indicateurs.
- **Comportements garantis** :
  - **Suppression d'une tâche quelconque** : `total` diminue de 1. Si la tâche était complétée, `completed` diminue de 1. Le pourcentage `percentage` est recalculé immédiatement.
  - **Suppression de la dernière tâche restante** : `total` passe à 0. L'application réaffiche l'état vide d'accueil avec `dog-resting.svg` et la citation initiale `WELCOME_QUOTE`. La barre de progression est masquée (`progress.total == 0`).
  - **Suppression menant à 100% de complétion** : Si la suppression d'une tâche non complétée laisse uniquement des tâches complétées (ex. 2 tâches dont 1 terminée, suppression de la tâche non terminée restante -> 1/1 = 100%), `is_all_completed` devient `True` et la bannière festive avec `dog-cheer.svg` s'affiche immédiatement.
- **Rationale** :
  - Cohérence totale et immédiate sans duplication de code ou d'état en cache.
  - Répond directement aux exigences fonctionnelles FR-003, FR-004, FR-005.

---

## Décision 6 : Stratégie de Couverture de Tests avec pytest

- **Décision** : Couvrir l'intégralité des flux nominaux et des cas limites par des tests automatisés dans `tests/test_models.py` et `tests/test_routes.py`.
- **Cas couverts** :
  1. **Tests unitaires (`test_models.py`)** :
     - Suppression réussie d'une tâche existante : vérification du retour `True`, disparition de la tâche, intégrité des tâches restantes.
     - Tentative de suppression d'un identifiant inexistant : vérification du retour `False` sans exception.
     - Recalcul de `get_progress()` après suppression d'une tâche non terminée, d'une tâche terminée, et de la dernière tâche restante.
  2. **Tests d'intégration HTTP (`tests/test_routes.py`)** :
     - `POST /tasks/<id>/delete` : redirection 302 vers `/`, absence de la tâche dans le HTML rendu (PRG).
     - `POST /tasks/inconnu/delete` : redirection 302 vers `/` sans erreur 500.
     - `GET /tasks/<id>/delete` : retour HTTP 405 Method Not Allowed.
     - Suppression de la dernière tâche : vérification du retour à l'état vide (`dog-resting.svg`, masquage de `progress-section`).
     - Suppression d'une tâche non complétée portant le total à 100% : vérification de l'activation de `celebration-card` et `dog-cheer.svg`.
     - Présence de l'attribut `aria-label="Supprimer la tâche : {titre}"` sur les boutons rendus.
- **Rationale** :
  - Respect du principe constitutionnel IV (pytest non-négociable, statut vert obligatoire).
  - Validation empirique continue de toutes les exigences et critères de succès.
