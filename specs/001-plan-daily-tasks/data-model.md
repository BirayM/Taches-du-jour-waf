# Data Model: Planification des Tâches du Jour

**Feature**: `001-plan-daily-tasks` | **Date**: 2026-10-22

Ce document définit les modèles de données, leurs contraintes de validation, leurs transitions d'état et le schéma de persistance locale pour l'application Tâches du Jour.

## 1. Entité : Tâche (`Task`)

Représente une tâche individuelle planifiée par l'utilisateur pour sa journée.

### Attributs

| Champ | Type Python | Requis | Valeur par défaut | Description |
|-------|-------------|--------|-------------------|-------------|
| `id` | `str` | Oui | Auto-généré (UUID v4 hexadécimal court ou entier sous forme de chaîne) | Identifiant unique de la tâche |
| `title` | `str` | Oui | - | Intitulé ou libellé de l'activité (1 à 200 caractères) |
| `completed` | `bool` | Oui | `False` | Statut d'achèvement de la tâche (`False` = à faire, `True` = terminée) |
| `created_at` | `str` | Oui | Horodatage ISO 8601 (ex. `2026-10-22T08:30:00Z`) | Date et heure de création pour assurer l'ordre chronologique |

### Règles de validation

- **Validation du titre (`title`)** :
  - La chaîne ne DOIT PAS être vide après suppression des espaces en début et fin (`title.strip() != ""`).
  - La longueur DOIT être comprise entre 1 et 200 caractères.
  - Tout caractère spécial HTML (`<`, `>`, `&`, `"`, `'`) DOIT être échappé lors du rendu afin d'empêcher les injections de code.
- **Identifiant unique (`id`)** :
  - Non modifiable après création.
- **Statut (`completed`)** :
  - Booléen strict (`True` ou `False`).

### Machine à états / Transitions

```text
[ Non créée ]
      │
      │ Soumission formulaire valide (POST /tasks)
      ▼
[ État : À FAIRE (completed = False) ]
      │
      │ Action de complétion (POST /tasks/<id>/complete)
      ▼
[ État : TERMINÉE (completed = True) ]
```

*Remarque* : Dans cette première version, la suppression est hors périmètre. La tâche demeure dans la liste avec son statut `completed = True` (affichée barrée).

---

## 2. Entité : Citation Motivante (`MotivationalQuote`)

Représente un message d'encouragement et d'inspiration canine affiché pour soutenir l'utilisateur.

### Attributs

| Champ | Type | Description |
|-------|------|-------------|
| `text` | `str` | Contenu de la phrase motivante |
| `author` | `str` | Nom du chien fictif ou de l'auteur (ex. *"Max le Berger Allemand"*, *"Luna le Golden Retriever"*) |

### Sélection

- Sélection aléatoire via `random.choice(QUOTES)` lors de chaque génération de la page d'accueil (`GET /`).
- En cas de liste de tâches vide, un message d'accueil spécifique et bienveillant est affiché à la place pour encourager l'ajout de la première tâche.

---

## 3. Schéma de Persistance Locale (`data/tasks.json`)

Les tâches sont sérialisées dans un fichier JSON situé par défaut dans `data/tasks.json`.

### Structure JSON

```json
[
  {
    "id": "a1b2c3d4",
    "title": "Préparer la leçon sur les fonctions Python",
    "completed": false,
    "created_at": "2026-10-22T08:30:00"
  },
  {
    "id": "e5f6g7h8",
    "title": "Vérifier les exercices des élèves",
    "completed": true,
    "created_at": "2026-10-22T09:15:00"
  }
]
```

### Règles de manipulation du fichier

1. **Initialisation automatique** : Si le répertoire `data/` ou le fichier `tasks.json` n'existe pas lors du premier appel, le module de persistance crée le dossier et initialise le fichier avec un tableau vide `[]`.
2. **Atomicité et intégrité** : L'écriture réécrit l'intégralité de la liste sérialisée avec indentation (`indent=2`) pour garantir la lisibilité humaine et l'intégrité du document.
3. **Ordre de restitution** : Les tâches sont restituées dans l'ordre chronologique de création (`created_at`).
