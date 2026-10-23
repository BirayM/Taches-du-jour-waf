# Data Model: Suivi de la Progression Quotidienne

**Feature**: `002-daily-task-progress` | **Date**: 2026-10-23

Ce document décrit les modèles de données, entités métier en mémoire, règles de validation et matrices de transition d'état relatives au calcul de la progression quotidienne et aux félicitations de complétion.

---

## 1. Entité : Statistiques de Progression (`ProgressStats`)

Représente l'état consolidé de la journée de travail à un instant donné. Cette entité est calculée dynamiquement en mémoire vive à partir de la collection des tâches existantes sans requérir de persistance distincte.

### Attributs

| Champ | Type Python | Requis | Valeur par défaut | Description |
|-------|-------------|--------|-------------------|-------------|
| `total` | `int` | Oui | `0` | Nombre total de tâches planifiées pour la journée (`len(tasks)`). |
| `completed` | `int` | Oui | `0` | Nombre de tâches ayant le statut `completed == True`. |
| `percentage` | `int` | Oui | `0` | Pourcentage de complétion arrondi à l'entier le plus proche (entre `0` et `100`). |
| `is_all_completed` | `bool` | Oui | `False` | Vrai si et seulement si `total > 0` et `completed == total`. |

### Règles de Calcul et Validation

1. **Garde de division par zéro** :
   - Si `total == 0` :
     - `completed = 0`
     - `percentage = 0`
     - `is_all_completed = False`
2. **Formule du pourcentage** :
   - Si `total > 0` :
     - `percentage = round((completed / total) * 100)`
     - Bornage garanti : `0 <= percentage <= 100`.
3. **Condition de félicitations totales (`is_all_completed`)** :
   - Strictement évalué à `total > 0 and completed == total`.
   - Ne peut jamais valoir `True` si `total == 0`.
4. **Cohérence arithmétique** :
   - Invariant : `0 <= completed <= total`.

---

## 2. Entité : Célébration Festive (`CelebrationBanner`)

Représente les éléments de contenu affichés pour célébrer la réussite de l'utilisateur lorsque `is_all_completed` est vrai.

### Attributs

| Champ | Type | Description |
|-------|------|-------------|
| `title` | `str` | Titre enthousiaste (ex. *"Mission accomplie !"* ou *"Toutes les tâches sont terminées !"*). |
| `message` | `str` | Message bienveillant et chaleureux félicitant l'utilisateur pour son effort. |
| `dog_image` | `str` | Nom de l'asset SVG local de célébration : `"images/dogs/dog-cheer.svg"`. |

---

## 3. Matrice des États et Transitions

```text
               [ 0 Tâche enregistrée ]
               (total = 0, percentage = 0, is_all_completed = False)
               - Barre de progression : absente / masquée
               - Félicitations : absentes
                          │
                          │ Ajout d'une 1ère tâche (POST /tasks)
                          ▼
            [ Tâches en cours d'accomplissement ]
            (total >= 1, 0 <= completed < total, is_all_completed = False)
            - Barre de progression : visible (0% à 99%)
            - Compteur : "X sur Y tâches terminées (Z%)"
            - Félicitations : absentes, citations de motivation standard
                          │
                          │ Complétion de la dernière tâche (POST /tasks/<id>/complete)
                          ▼
            [ Accomplissement total de la journée ]
            (total >= 1, completed == total, is_all_completed = True)
            - Barre de progression : visible (100%)
            - Compteur : "Y sur Y tâches terminées (100%)"
            - Félicitations : bannière festive active avec dog-cheer.svg
                          │
                          │ Ajout d'une nouvelle tâche (POST /tasks)
                          ▼
            (Retour à l'état "Tâches en cours d'accomplissement")
```

### Table des Transitions

| État Initial | Événement déclencheur | Nouvel État | `percentage` | `is_all_completed` | Visuel affiché |
|--------------|-----------------------|-------------|--------------|--------------------|----------------|
| Aucune tâche (0/0) | Ajout d'une tâche | 1 tâche (0/1) | 0% | `False` | Barre à 0%, citation |
| Tâches partielles (0/1) | Marquage terminé | 1 tâche (1/1) | 100% | `True` | Barre à 100%, célébration `dog-cheer.svg` |
| Complétion totale (1/1) | Ajout d'une tâche | 2 tâches (1/2) | 50% | `False` | Barre à 50%, disparition célébration |
| Tâches partielles (1/3) | Marquage terminé | 3 tâches (2/3) | 67% | `False` | Barre à 67%, citation standard |
| Complétion totale (3/3) | Redémarrage serveur | 3 tâches (3/3) | 100% | `True` | Persistance exacte restituée |
