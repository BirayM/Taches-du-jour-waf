# Interface Contract: Web Routes & Progress Display

**Feature**: `002-daily-task-progress` | **Date**: 2026-10-23

Ce document spécifie les contrats d'interface pour l'intégration de la progression quotidienne et du message de célébration dans les routes web Flask en rendu côté serveur (SSR).

---

## 1. `GET /` - Affichage de l'interface principale avec Progression

Affiche la page d'accueil enrichie du module de progression quotidienne et, le cas échéant, de la bannière de célébration.

### Paramètres de requête
- Aucun.

### Données injectées dans le template (`index.html`)

```python
render_template(
    "index.html",
    tasks=tasks,            # List[Task] ordonnée
    quote=quote,            # MotivationalQuote
    progress=progress       # ProgressStats (total, completed, percentage, is_all_completed)
)
```

| Variable Jinja2 | Type | Attributs exposés | Description |
|-----------------|------|-------------------|-------------|
| `progress` | `ProgressStats` | `total` (`int`)<br>`completed` (`int`)<br>`percentage` (`int`)<br>`is_all_completed` (`bool`) | Objet contenant l'ensemble des métriques de complétion de la journée |
| `tasks` | `List[Task]` | `id`, `title`, `completed`, `created_at` | Liste ordonnée des tâches |
| `quote` | `MotivationalQuote` | `text`, `author` | Citation de motivation |

### Contrat de Rendu HTML5 & Accessibilité

#### Bloc Progression (`{% if progress.total > 0 %}`)

Le fragment HTML généré DOIT respecter les balises sémantiques et attributs d'accessibilité ARIA suivants :

```html
<section class="progress-section" aria-label="Progression de la journée">
    <div class="progress-header">
        <span class="progress-title">Progression de la journée</span>
        <span class="progress-counter">
            {{ progress.completed }} sur {{ progress.total }} terminée{% if progress.completed > 1 %}s{% endif %} ({{ progress.percentage }}%)
        </span>
    </div>
    <div class="progress-track" 
         role="progressbar" 
         aria-valuenow="{{ progress.percentage }}" 
         aria-valuemin="0" 
         aria-valuemax="100" 
         aria-label="Pourcentage des tâches accomplies : {{ progress.percentage }}%">
        <div class="progress-fill" style="width: {{ progress.percentage }}%;"></div>
    </div>
</section>
```

#### Bloc Célébration Festive (`{% if progress.is_all_completed %}`)

Lorsque toutes les tâches sont achevées (`is_all_completed == True`), une bannière festive dédiée DOIT être rendue :

```html
<section class="celebration-card" aria-label="Célébration des tâches accomplies">
    <img src="{{ url_for('static', filename='images/dogs/dog-cheer.svg') }}" 
         alt="Chien heureux célébrant la réussite" 
         class="celebration-dog">
    <div class="celebration-content">
        <h3>Bravo ! Toutes les missions du jour sont terminées ! 🎉</h3>
        <p>Tu as accompli l'intégralité de tes objectifs du jour. Profite bien de ta journée ! 🐾</p>
    </div>
</section>
```

### Codes de Réponse HTTP
- **Code 200 OK** : Rendu complet de la page HTML5 (`text/html; charset=utf-8`).

---

## 2. Routes de Mutation (`POST /tasks` et `POST /tasks/<id>/complete`)

Ces routes conservent leur contrat existant (Post/Redirect/Get avec code 302 vers `/`).
Leur exécution modifie l'état de la collection dans `data/tasks.json`, ce qui met immédiatement à jour les valeurs calculées de `progress` lors de la redirection suivante sur `GET /`.
