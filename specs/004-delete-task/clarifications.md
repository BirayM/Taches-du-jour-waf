# Clarifications de Spécification : Suppression de Tâche Individuelle

**Dossier de fonctionnalité** : `specs/004-delete-task`  
**Date** : 2026-10-24  
**Statut** : Clôturé (Mode non interactif)  
**Document source analysé** : `specs/004-delete-task/spec.md`

---

### 1. Point d'entrée HTTP et signature d'URL pour l'action de suppression (FR-006)

**Question :** Quel doit être le chemin d'URL et la méthode HTTP exacte du point d'entrée dédié à la suppression d'une tâche ? (FR-006)

- **Pourquoi c'est important :** La spécification indique la nécessité d'une nouvelle route POST dans `app/routes.py` appliquant le patron Post/Redirect/Get (PRG), mais ne formalise pas la signature d'URL exacte, indispensable pour lier les formulaires HTML natifs, implémenter la fonction de vue Flask et cibler précisément les requêtes dans la suite de tests `pytest`.
- **Réponse par défaut proposée :** La route dédiée sera `POST /tasks/<task_id>/delete`. Ce motif est directement aligné sur la convention déjà établie dans l'application avec la route `POST /tasks/<task_id>/complete`, respecte le principe didactique et de simplicité (KISS) de la Constitution du projet, et fonctionne parfaitement avec les formulaires HTML5 standards sans dépendance JavaScript.
- **Impact :**
  - *Architecture & Backend* : Déclaration de `@bp.route("/tasks/<task_id>/delete", methods=["POST"]) def delete_task(task_id: str):` dans `app/routes.py`.
  - *Frontend & Contrat d'interface* : Ajout dans `app/templates/index.html` d'un formulaire `<form action="{{ url_for('main.delete_task', task_id=task.id) }}" method="POST" class="delete-form">`.
  - *Tests* : Test d'intégration automatisé simulant un appel `client.post(f"/tasks/{task.id}/delete")`.

---

### 2. Comportement applicatif et statut HTTP lors du ciblage d'un identifiant inexistant ou déjà supprimé (FR-007, SC-006)

**Question :** Quel code de statut HTTP précis et quelle réaction visuelle le système doit-il retourner lorsqu'une requête de suppression cible un identifiant de tâche inexistant ou déjà supprimé ? (FR-007)

- **Pourquoi c'est important :** La spécification requiert d'ignorer la demande de manière sûre et de rediriger sans erreur serveur ni blocage de l'interface, mais ne tranche pas entre une redirection silencieuse (HTTP 302), un message d'avertissement Flash, ou une réponse d'erreur client standard (HTTP 404).
- **Réponse par défaut proposée :** Redirection immédiate HTTP 302 vers l'accueil (`/`) de manière transparente et silencieuse, sans message flash d'erreur et sans générer de code 404. Si la tâche n'existe plus (suppression concurrente, double clic rapide ou onglet obsolète), l'état final désiré (la tâche n'est plus dans la liste) est d'ores et déjà atteint, garantissant l'idempotence fonctionnelle pour l'utilisateur.
- **Impact :**
  - *Architecture & Modèle* : La méthode `TaskManager.delete_task(task_id)` renvoie un booléen `False` si la tâche n'est pas trouvée, sans lever d'exception ; la vue Flask intercepte ce retour et exécute simplement `return redirect(url_for("main.index"))`.
  - *Tests* : Le test pytest pour un identifiant inconnu vérifiera l'obtention d'un statut `302 Found` redirigeant vers `/`, sans code `500 Internal Server Error` ni écran `404 Not Found`.

---

### 3. Présence d'un message temporaire de notification (Flash message) après suppression réussie (FR-002, User Story 1)

**Question :** Une notification temporaire (message flash Flask) doit-elle être affichée à l'utilisateur après la suppression nominale d'une tâche ? (FR-002)

- **Pourquoi c'est important :** Savoir si une notification textuelle doit être injectée dans la session conditionne l'utilisation du mécanisme `flash()` de Flask, l'affichage potentiel d'une bannière d'information dans le template `index.html`, ainsi que les assertions de contenu dans les tests de rendu.
- **Réponse par défaut proposée :** Aucune notification flash (suppression silencieuse). La suppression immédiate de la carte de la tâche dans la liste et l'ajustement instantané du compteur et de la jauge constituent un retour visuel suffisant et auto-porteur. Cette approche évite de polluer l'interface visuelle et reste strictement cohérente avec la route `complete_task` existante qui ne génère aucun message flash.
- **Impact :**
  - *Architecture & Vues* : Aucun appel à `flash("Tâche supprimée", "info")` dans la fonction `delete_task` de `app/routes.py`.
  - *Frontend* : Pas d'élément visuel additionnel à intégrer dans le gabarit au-delà de la suppression de l'élément de liste `<li>`.
  - *Tests* : Les scénarios de tests valident la disparition de l'intitulé de la tâche dans le corps HTML de la réponse sans vérifier la présence d'un message flash spécifique.

---

### 4. Restriction stricte de la méthode HTTP contre le déclenchement accidentel par GET (FR-006, Sécurité)

**Question :** Le point de terminaison de suppression doit-il interdire strictement la méthode HTTP GET et répondre par un code HTTP 405 Method Not Allowed en cas de tentative d'accès direct ? (FR-006)

- **Pourquoi c'est important :** Si l'action de suppression pouvait être déclenchée ou accessible via la méthode GET, des mécanismes de préchargement de liens de navigateurs, des accélérateurs web ou des robots d'indexation pourraient supprimer involontairement des tâches utilisateur.
- **Réponse par défaut proposée :** Oui, la route doit être déclarée exclusivement avec `methods=["POST"]`. Toute requête `GET` sur `/tasks/<task_id>/delete` doit être automatiquement rejetée par Flask avec un code d'état HTTP `405 Method Not Allowed`. Cela préserve l'intégrité des données tout en évitant l'introduction de bibliothèques tierces superflues (ex: Flask-WTF), conformément au principe de minimalisme des dépendances (Constitution, Principe V).
- **Impact :**
  - *Sécurité & Routage* : Restriction stricte au niveau du décorateur Flask `@bp.route(..., methods=["POST"])`.
  - *Tests* : Ajout d'un test spécifique vérifiant que `client.get("/tasks/<id>/delete")` retourne explicitement le code HTTP `405`.

---

### 5. Accessibilité et opérabilité du bouton de suppression sur les tâches déjà complétées (FR-001, FR-008)

**Question :** Le bouton de suppression doit-il être disponible et pleinement opérable de manière identique sur les tâches marquées comme terminées ? (FR-001)

- **Pourquoi c'est important :** Dans l'interface actuelle, le bouton de complétion d'une tâche terminée est verrouillé (`disabled`). Il est essentiel de préciser si la suppression suit la même restriction ou si elle demeure active afin de permettre le nettoyage des activités accomplies.
- **Réponse par défaut proposée :** Le bouton de suppression reste toujours actif et cliquable (aucun attribut `disabled`), quel que soit l'état d'achèvement de la tâche (`completed=False` ou `completed=True`). Un utilisateur doit pouvoir retirer une tâche terminée de sa journée pour ajuster sa liste, ce qui recalcule proportionnellement le compteur restant (ex. passer de "1 sur 1 (100%)" à "0 sur 0" état vide).
- **Impact :**
  - *Frontend & Accessibilité* : Le bouton de suppression dans le template `index.html` ne comporte pas d'attribut conditionnel `disabled` et conserve son attribut `aria-label="Supprimer la tâche : {{ task.title }}"` même lorsque la classe `is-completed` est appliquée sur l'élément parent.
  - *Tests* : Test d'acceptation dédié validant la suppression d'une tâche déjà complétée et vérifiant la mise à jour arithmétique correcte des statistiques de progression.
