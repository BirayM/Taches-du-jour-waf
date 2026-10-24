# Quickstart & Validation Guide: Suppression de Tâche Individuelle

**Feature**: `004-delete-task` | **Date**: 2026-10-24

Ce guide fournit les instructions opérationnelles pour exécuter les tests automatisés et valider manuellement de bout en bout la suppression individuelle d'une tâche ainsi que l'actualisation dynamique du tableau de bord.

Pour les spécifications des routes et gabarits, se référer au document [contracts/web-routes.md](contracts/web-routes.md). Pour les détails sur les transitions d'états, consulter [data-model.md](data-model.md).

---

## 1. Prérequis & Environnement

- **Python** : Version 3.10 ou supérieure installée (`python3 --version`).
- **Activation de l'environnement virtuel** :
  ```bash
  source .venv/bin/activate
  ```
- **Vérification des dépendances** :
  ```bash
  pip install -r requirements.txt
  ```

---

## 2. Exécution des Tests Automatisés avec pytest

Exécuter la suite complète de tests via `pytest` :

```bash
.venv/bin/pytest
```

**Comportements validés** :
- `tests/test_models.py` :
  - Suppression unitaire d'une tâche existante (`delete_task` retourne `True`, retrait du fichier JSON).
  - Tentative de suppression d'un identifiant inexistant (`delete_task` retourne `False` sans exception).
  - Recalcul des indicateurs `TaskManager.get_progress()` post-suppression.
- `tests/test_routes.py` :
  - Route `POST /tasks/<task_id>/delete` appliquant le patron Post/Redirect/Get avec statut HTTP 302 vers `/`.
  - Rejet des requêtes `GET /tasks/<task_id>/delete` avec code HTTP 405 Method Not Allowed.
  - Résilience lors d'une suppression d'identifiant inconnu (redirection 302 sans erreur 500).
  - Retour à l'état vide d'accueil lors de la suppression de la dernière tâche restante.
  - Déclenchement de la célébration festive (`dog-cheer.svg`) si la suppression amène le taux à 100%.
  - Présence des attributs d'accessibilité `aria-label="Supprimer la tâche : {nom}"`.

---

## 3. Lancement du Serveur Web Local

```bash
python run.py
```

L'application est accessible à l'adresse : [http://localhost:5000](http://localhost:5000).

---

## 4. Scénarios de Validation Manuelle de Bout en Bout

### Scénario 1 : Suppression d'une tâche parmi plusieurs et recalcul de progression
1. Ajouter 3 tâches :
   - `"Tâche 1"`
   - `"Tâche 2"`
   - `"Tâche 3"`
2. Marquer `"Tâche 1"` comme terminée (compteur : **« 1 sur 3 terminées (33%) »**).
3. Cliquer sur le bouton de suppression (🗑️) de la `"Tâche 2"`.
4. **Résultat attendu** :
   - La `"Tâche 2"` disparaît immédiatement de la liste.
   - Les tâches restantes sont `"Tâche 1"` (terminée) et `"Tâche 3"` (à faire).
   - Le compteur s'actualise immédiatement à **« 1 sur 2 terminées (50%) »**.
   - La barre de progression s'ajuste visuellement à 50%.

### Scénario 2 : Suppression de la dernière tâche et retour à l'état vide
1. À partir d'une seule tâche restante dans l'application (ex. `"Tâche 3"`).
2. Cliquer sur le bouton de suppression (🗑️) de cette tâche.
3. **Résultat attendu** :
   - La dernière tâche disparaît de la vue.
   - La section de progression (compteur et jauge) est masquée.
   - L'écran affiche l'état vide initial avec l'illustration du chiot au repos (`dog-resting.svg`) et le message invitant à planifier sa journée.

### Scénario 3 : Suppression menant à 100% d'achèvement (Célébration festive)
1. Créer 2 tâches : `"Rédiger le rapport"` et `"Envoyer le courriel"`.
2. Marquer `"Rédiger le rapport"` comme terminée (compteur : **« 1 sur 2 terminées (50%) »**).
3. Supprimer la tâche non terminée `"Envoyer le courriel"`.
4. **Résultat attendu** :
   - La seule tâche restante est terminée : le ratio devient 1 sur 1 (100%).
   - La jauge de progression s'affiche à 100%.
   - La bannière festive de félicitations s'active instantanément avec l'illustration canine joyeuse (`dog-cheer.svg`).

### Scénario 4 : Suppression d'une tâche déjà complétée
1. Disposer d'une tâche marquée comme terminée.
2. Vérifier que son bouton de suppression 🗑️ n'est pas grisé/désactivé (contrairement à la case à cocher).
3. Cliquer sur le bouton de suppression.
4. **Résultat attendu** :
   - La tâche terminée est retirée définitivement.
   - Le compteur de tâches complétées et le total sont décrémentés en cohérence.

### Scénario 5 : Résilience, patron PRG et rafraîchissement navigateur
1. Supprimer une tâche quelconque.
2. Une fois redirigé sur `/`, actualiser la page avec la touche `F5` ou le bouton de rechargement du navigateur.
3. **Résultat attendu** :
   - La page se recharge instantanément sans afficher d'avertissement de re-soumission de formulaire (*Confirm Form Resubmission*).
   - Aucun crash ni doublon de traitement.

### Scénario 6 : Accessibilité au clavier et lecteur d'écran
1. Recharger la page avec au moins une tâche.
2. Utiliser exclusivement la touche `Tab` pour naviguer jusqu'au bouton de suppression 🗑️.
3. Vérifier via l'inspecteur d'éléments que le bouton dispose de l'attribut `aria-label="Supprimer la tâche : {titre}"`.
4. Appuyer sur la touche `Entrée` ou `Espace`.
5. **Résultat attendu** :
   - La tâche ciblée est supprimée de façon identique à un clic de souris.
