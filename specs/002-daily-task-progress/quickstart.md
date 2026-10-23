# Quickstart & Validation Guide: Suivi de la Progression Quotidienne

**Feature**: `002-daily-task-progress` | **Date**: 2026-10-23

Ce guide fournit les étapes concrètes pour exécuter les tests automatisés et valider manuellement de bout en bout l'affichage de la progression et du message de célébration.

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

Exécuter la suite complète de tests via pytest :

```bash
.venv/bin/pytest
```

**Comportements validés** :
- `tests/test_models.py` :
  - Calcul de progression avec 0 tâche (`total=0`, `percentage=0`, `is_all_completed=False`).
  - Calcul du pourcentage arrondi (ex: 1/3 = 33%, 2/3 = 67%).
  - Déclenchement du statut `is_all_completed=True` uniquement quand `total > 0` et `completed == total`.
  - Désactivation de `is_all_completed` lors de l'ajout d'une tâche à une liste terminée.
- `tests/test_routes.py` :
  - Absence de la barre de progression et des félicitations sur liste vide.
  - Présence de la barre avec les attributs ARIA (`aria-valuenow`, `role="progressbar"`) dès qu'une tâche existe.
  - Apparition de la bannière festive et de `dog-cheer.svg` lors de la complétion à 100%.

---

## 3. Lancement du Serveur Web Local

```bash
python run.py
```

L'application est accessible à l'adresse locale : [http://localhost:5000](http://localhost:5000).

---

## 4. Scénarios de Validation Manuelle de Bout en Bout

### Scénario 1 : État initial (0 tâche enregistrée)
1. Ouvrir le navigateur sur `http://localhost:5000`.
2. **Vérification** :
   - L'écran affiche l'état vide d'accueil avec le chiot au repos (`dog-resting.svg`).
   - Aucune barre de progression n'est affichée.
   - Aucun message de félicitations n'apparaît.

### Scénario 2 : Ajout de plusieurs tâches (Progression à 0%)
1. Ajouter successivement trois tâches via le formulaire :
   - `"Préparer le support de cours"`
   - `"Relire les exercices pratiques"`
   - `"Enregistrer la démo vidéo"`
2. **Vérification** :
   - La section de progression apparaît au-dessus ou en tête de la liste des activités.
   - Le compteur textuel indique : **« 0 sur 3 terminée (0%) »**.
   - La barre de progression est vide (largeur `0%`).
   - La citation de motivation standard est affichée. Aucun message de félicitations.

### Scénario 3 : Complétion partielle (Progression à 33% puis 67%)
1. Cocher la première tâche `"Préparer le support de cours"` comme terminée.
2. **Vérification** :
   - Le compteur passe à **« 1 sur 3 terminée (33%) »**.
   - La barre de progression visuelle avance à un tiers de sa largeur (`33%`).
   - La première tâche apparaît barrée / complétée.
3. Cocher la seconde tâche `"Relire les exercices pratiques"`.
4. **Vérification** :
   - Le compteur passe à **« 2 sur 3 terminées (67%) »**.
   - La barre de progression avance aux deux tiers (`67%`).

### Scénario 4 : Complétion à 100% et Célébration Festive
1. Cocher la troisième et dernière tâche `"Enregistrer la démo vidéo"`.
2. **Vérification** :
   - Le compteur indique : **« 3 sur 3 terminées (100%) »**.
   - La barre de progression est entièrement remplie (`100%`).
   - Une bannière festive dédiée apparaît en évidence avec l'illustration joyeuse `dog-cheer.svg`.
   - Le message chaleureux félicite l'utilisateur pour avoir accompli l'intégralité de sa journée.

### Scénario 5 : Ajout d'une tâche après complétion à 100% (Reprise d'activité)
1. Saisir une nouvelle tâche `"Préparer la séance de demain"` et valider.
2. **Vérification** :
   - Le compteur passe immédiatement à **« 3 sur 4 terminées (75%) »**.
   - La barre de progression recule proportionnellement à `75%`.
   - La bannière de célébration festive disparaît au profit du suivi standard.

### Scénario 6 : Persistance et Robustesse après Redémarrage
1. Arrêter le serveur Flask dans le terminal (`Ctrl+C`).
2. Redémarrer le serveur (`python run.py`).
3. Recharger la page dans le navigateur.
4. **Vérification** :
   - Le compteur (3 sur 4) et la barre de progression (75%) sont fidèlement recalculés et restitués.
