# Interface Contract: Web Routes & Suppression de Tâche

**Feature**: `004-delete-task` | **Date**: 2026-10-24

Ce document spécifie le contrat d'interface HTTP et les fragments de gabarit Jinja2 pour l'action de suppression individuelle d'une tâche dans l'application « Tâches du Jour ».

---

## 1. Point d'Accès Web : `POST /tasks/<task_id>/delete`

Supprime définitivement la tâche identifiée par `task_id` du stockage persistant et redirige vers la page d'accueil selon le patron Post/Redirect/Get (PRG).

### Paramètres d'URL

| Paramètre | Emplacement | Type | Requis | Description |
|-----------|-------------|------|--------|-------------|
| `task_id` | Chemin (`path`) | `string` | Oui | Identifiant unique de la tâche à supprimer (ex. chaîne hexadécimale). |

### Méthodes HTTP supportées

- **`POST`** : Unique méthode acceptée pour déclencher l'action.
- **`GET`, `PUT`, `DELETE`, etc.** : Rejetées avec code HTTP `405 Method Not Allowed`.

### Réponses HTTP

#### Cas 1 : Suppression nominale (Tâche existante)
- **Code d'état** : `302 Found`
- **En-têtes** :
  - `Location`: `/`
- **Effet de bord** : La tâche est retirée de `data/tasks.json`. Lors du rechargement de `/`, la liste et les indicateurs (`progress`) sont mis à jour sans la tâche.

#### Cas 2 : Identifiant inexistant ou suppression concurrente (Idempotence)
- **Code d'état** : `302 Found`
- **En-têtes** :
  - `Location`: `/`
- **Effet de bord** : Aucun fichier n'est altéré. L'utilisateur est redirigé de manière fluide sans message d'erreur ni crash `500`.

#### Cas 3 : Tentative d'accès en méthode `GET`
- **Code d'état** : `405 Method Not Allowed`
- **Description** : Flask interdit l'exécution directe en GET pour empêcher tout préchargement ou appel intempestif.

---

## 2. Contrat de Gabarit Jinja2 (`app/templates/index.html`)

Chaque élément de tâche `<li class="task-item">` intègre un formulaire HTML dédié à la suppression, accessible au clavier et aux technologies d'assistance.

### Structure HTML5 Sémantique

```html
<li class="task-item {% if task.completed %}is-completed{% endif %}">
    <div class="task-content">
        <!-- Formulaire de complétion existant -->
        <form action="{{ url_for('main.complete_task', task_id=task.id) }}" method="POST" class="complete-form">
            <button type="submit" 
                    class="checkbox-btn {% if task.completed %}checked{% endif %}" 
                    aria-label="{% if task.completed %}Tâche terminée{% else %}Marquer comme terminée{% endif %}"
                    {% if task.completed %}disabled{% endif %}>
                {% if task.completed %}✓{% endif %}
            </button>
        </form>
        <span class="task-title">{{ task.title }}</span>
    </div>

    <div class="task-actions">
        <span class="task-badge {% if task.completed %}badge-done{% else %}badge-pending{% endif %}">
            {% if task.completed %}Terminée 🎉{% else %}À faire 🐾{% endif %}
        </span>

        <!-- Formulaire de suppression individuel -->
        <form action="{{ url_for('main.delete_task', task_id=task.id) }}" method="POST" class="delete-form">
            <button type="submit" 
                    class="btn-delete" 
                    aria-label="Supprimer la tâche : {{ task.title }}"
                    title="Supprimer la tâche : {{ task.title }}">
                <span class="delete-icon" aria-hidden="true">🗑️</span>
            </button>
        </form>
    </div>
</li>
```

### Règles d'Accessibilité (WAI-ARIA)

- **Attribut `aria-label`** :
  - Valeur dynamique : `"Supprimer la tâche : {{ task.title }}"`.
  - Permet aux lecteurs d'écran (NVDA, VoiceOver, Orca) d'annoncer explicitement quelle tâche sera détruite.
- **Navigabilité au clavier** :
  - Le bouton `<button type="submit" class="btn-delete">` est nativement focalisable dans l'ordre séquentiel du DOM via la touche `Tab`.
  - L'activation est possible au clavier avec la touche `Entrée` ou `Espace`.
- **Indépendance du statut d'achèvement** :
  - Le bouton de suppression NE DOIT PAS comporter d'attribut `disabled`, y compris si `task.completed == True`.

---

## 3. Contrat CSS (`app/static/css/style.css`)

Classes CSS minimales ajoutées pour intégrer harmonieusement l'action de suppression :

```css
.task-actions {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.delete-form {
    display: inline-flex;
    margin: 0;
    padding: 0;
}

.btn-delete {
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 0.35rem 0.5rem;
    border-radius: var(--radius-sm, 6px);
    color: var(--color-text-muted, #718096);
    font-size: 1rem;
    line-height: 1;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s ease, color 0.2s ease, transform 0.1s ease;
}

.btn-delete:hover {
    background-color: var(--color-danger-light, #fee2e2);
    color: var(--color-danger, #ef4444);
}

.btn-delete:focus-visible {
    outline: 2px solid var(--color-primary, #4f46e5);
    outline-offset: 2px;
}
```
