# Interface Contract: Web Routes & Endpoints

**Feature**: `001-plan-daily-tasks` | **Date**: 2026-10-22

Ce document spécifie les contrats d'interface HTTP de l'application Tâches du Jour. L'application repose sur le rendu côté serveur (SSR) avec Flask et des formulaires HTML standards suivant le patron Post/Redirect/Get (PRG).

---

## 1. `GET /` - Affichage de l'interface principale

Affiche la page d'accueil contenant le formulaire d'ajout, la liste ordonnée des tâches du jour, le message de motivation et l'univers graphique canin.

### Paramètres de requête
- Aucun.

### Données injectées dans le template (`index.html`)
- `tasks`: Liste des objets `Task` ordonnés par `created_at`.
- `quote`: Objet `MotivationalQuote` sélectionné aléatoirement si des tâches existent, ou message d'accueil initial si la liste est vide.
- `error`: Message d'erreur textuel optionnel (ex. si une soumission invalide a été interceptée via flash message).

### Réponse HTTP
- **Code 200 OK** : Rendu complet de la page HTML5 avec encodage UTF-8 (`text/html; charset=utf-8`).

---

## 2. `POST /tasks` - Ajout d'une nouvelle tâche

Traite la soumission du formulaire d'ajout d'une tâche.

### Corps de la requête (Form Data: `application/x-www-form-urlencoded`)

| Champ | Type | Présence | Contrainte | Description |
|-------|------|----------|------------|-------------|
| `title` | `string` | Requis | 1 à 200 caractères non vides | Intitulé de la tâche à ajouter |

### Comportement & Validation
1. Récupération et nettoyage : `title = request.form.get("title", "").strip()`.
2. Validation :
   - Si `title` est vide ou dépasse 200 caractères : émission d'un message flash d'erreur ou redirection avec paramètre d'erreur.
   - Si `title` est valide : instanciation d'une nouvelle `Task`, persistance dans `data/tasks.json`.
3. Redirection :
   - **Code 302 Found** vers `Location: /`.
   - *Effet* : Réinitialise le champ de saisie du navigateur, garantissant qu'une nouvelle tâche peut être saisie immédiatement et prévenant le double-post lors d'un rafraîchissement.

---

## 3. `POST /tasks/<id>/complete` - Marquage d'une tâche comme terminée

Met à jour l'état d'une tâche pour la passer à `completed = True`.

### Paramètres d'URL

| Paramètre | Type | Description |
|-----------|------|-------------|
| `id` | `string` | Identifiant unique de la tâche |

### Corps de la requête
- Aucun corps obligatoire (formulaire POST simple déclenché par un bouton d'action ou une case à cocher).

### Comportement
1. Recherche de la tâche correspondant à `id` dans `data/tasks.json`.
2. Si la tâche existe :
   - `task.completed = True`
   - Sauvegarde de la liste mise à jour dans `data/tasks.json`.
3. Si la tâche n'existe pas :
   - Ignorer ou émettre un avertissement non bloquant.
4. Redirection :
   - **Code 302 Found** vers `Location: /`.
