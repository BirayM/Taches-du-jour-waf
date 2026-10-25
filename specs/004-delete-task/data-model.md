# Data Model: Suppression de Tâche Individuelle

**Feature**: `004-delete-task` | **Date**: 2026-10-24

Ce document décrit les modèles de données, le cycle de vie de destruction des entités, les règles de validation et la matrice de transition d'état relatives à la suppression individuelle d'une tâche dans l'application « Tâches du Jour ».

---

## 1. Entité : Tâche Quotidienne (`Task`)

Représente une mission planifiée par l'utilisateur. Dans le cadre de la présente fonctionnalité, l'entité n'introduit aucun nouveau champ persistant mais définit son cycle de destruction définitive.

### Attributs de l'entité

| Champ | Type Python | Requis | Immuable | Description |
|-------|-------------|--------|----------|-------------|
| `id` | `str` | Oui | Oui | Identifiant unique (ex. chaîne hexadécimale de 8 caractères) servant de clé de ciblage pour la suppression. |
| `title` | `str` | Oui | Non | Intitulé descriptif (1 à 200 caractères), utilisé pour composer le libellé accessible `aria-label`. |
| `completed` | `bool` | Oui | Non | Statut d'achèvement (`False` = à faire, `True` = terminée). |
| `created_at` | `str` | Oui | Oui | Horodatage de création au format ISO 8601 (UTC). |

### Cycle de Vie et Opération de Destruction

- **Opération** : `DELETE` physique (purge définitive).
- **Règle de persistance** : La tâche est retirée sans archivage intermédiaire, sans corbeille (`recycle bin`) et sans possibilité d'annulation (`undo`).
- **Intégrité référentielle** : Aucune entité dépendante orpheline n'est conservée ; l'ordre chronologique des autres tâches (`created_at`) demeure inchangé.

---

## 2. Entité de Gestion : `TaskManager` (Opérations de persistance)

Assure les manipulations de lecture et d'écriture synchrone dans le fichier `data/tasks.json`.

### Signature de la méthode de suppression

```python
def delete_task(self, task_id: str) -> bool:
    """
    Supprime définitivement une tâche du fichier de persistance via son identifiant unique.

    Args:
        task_id: Identifiant unique de la tâche à supprimer.

    Returns:
        bool: True si la tâche a été trouvée et supprimée, False si elle n'existait pas.
    """
```

### Règles de traitement
1. Si `task_id` correspond à une tâche existante :
   - La tâche est retirée de la liste en mémoire.
   - La nouvelle liste est sérialisée dans `data/tasks.json` avec indentation standard.
   - La fonction retourne `True`.
2. Si `task_id` ne correspond à aucune tâche (inconnu, déjà supprimé, chaîne vide) :
   - Aucun accès en écriture n'est effectué sur le fichier de persistance.
   - La fonction retourne `False` sans lever d'exception.

---

## 3. Entité Calculée : Statistiques de Progression (`ProgressStats`)

À chaque suppression, les statistiques d'avancement de la journée sont recalculées dynamiquement via `TaskManager.get_progress()`.

### Attributs et Formules Dérivées

| Attribut | Type | Formule de recalcul post-suppression |
|----------|------|--------------------------------------|
| `total` | `int` | `len(tasks)` (décrémenté de 1 si la suppression réussit) |
| `completed` | `int` | `sum(1 for t in tasks if t.completed)` (décrémenté de 1 si la tâche supprimée était terminée) |
| `percentage` | `int` | `round((completed / total) * 100)` si `total > 0`, sinon `0` |
| `is_all_completed` | `bool` | `True` si et seulement si `total > 0` et `completed == total` |

---

## 4. Matrice des États et Transitions

```text
               ┌────────────────────────────────────────────────┐
               │         État Initial : Tâches Présentes         │
               │   total = N (>= 1), completed = C (0 <= C <= N) │
               └───────────────────────┬────────────────────────┘
                                       │
                      Action de suppression : POST /tasks/<id>/delete
                                       │
            ┌──────────────────────────┼──────────────────────────┐
            ▼                          ▼                          ▼
   [ N = 1 (Dernière tâche) ]   [ C < N et tâche non finie ]   [ Tâche finie ou ratio < 100% ]
            │                          │                          │
            ▼                          ▼                          ▼
   [ Nouveaux totaux : 0/0 ]   [ Nouveau ratio : C / (N-1) ]  [ Nouveaux totaux : (C-1) / (N-1) ]
     - total = 0                 - Si C == (N-1) > 0 :          - total = N - 1
     - completed = 0               is_all_completed = True      - percentage réévalué
     - percentage = 0              (Célébration festive)        - is_all_completed = False
     - is_all_completed = False  - Sinon :                      - Bandeau de motivation standard
     - État vide d'accueil         is_all_completed = False
       (dog-resting.svg)
```

### Table des Transitions Détaillée

| État avant suppression (`total`, `completed`) | Tâche ciblée | État après suppression (`total`, `completed`) | `percentage` | `is_all_completed` | Vue et visuel affichés |
|---|---|---|---|---|---|
| `(1, 0)` | Tâche non terminée | `(0, 0)` | `0%` | `False` | **État vide d'accueil** : `dog-resting.svg`, barre de progression masquée, citation d'accueil |
| `(1, 1)` | Tâche terminée | `(0, 0)` | `0%` | `False` | **État vide d'accueil** : `dog-resting.svg`, barre et célébration masquées |
| `(3, 1)` (33%) | Tâche non terminée | `(2, 1)` | `50%` | `False` | Liste mise à jour, compteur « 1 sur 2 (50%) », barre à 50% |
| `(3, 2)` (67%) | Tâche terminée | `(2, 1)` | `50%` | `False` | Liste mise à jour, compteur « 1 sur 2 (50%) », barre à 50% |
| `(2, 1)` (50%) | Tâche non terminée | `(1, 1)` | `100%` | `True` | **Complétion à 100%** : barre à 100%, affichage de la bannière de célébration `dog-cheer.svg` |
| `(3, 3)` (100%) | Tâche terminée | `(2, 2)` | `100%` | `True` | Reste à 100%, maintien de la bannière de célébration `dog-cheer.svg` |
| `(3, 1)` | Identifiant inexistant | `(3, 1)` | `33%` | `False` | Aucun changement : redirection silencieuse, état strictement préservé |
