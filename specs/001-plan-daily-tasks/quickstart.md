# Quickstart & Validation Guide: Planification des Tâches du Jour

**Feature**: `001-plan-daily-tasks` | **Date**: 2026-10-22

Ce guide présente les instructions pas à pas pour initialiser l'environnement, lancer les tests automatisés et valider manuellement de bout en bout la fonctionnalité de planification quotidienne des tâches.

---

## 1. Prérequis & Installation

- **Python** : Version 3.10 ou supérieure installée sur la machine (`python3 --version`).
- **Environnement virtuel (`venv`)** :
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```
- **Installation des dépendances autorisées** :
  ```bash
  pip install -r requirements.txt
  ```
  *(Seuls `flask` et `pytest` sont autorisés conformément à la constitution).*

---

## 2. Exécution des Tests Automatisés

Avant tout lancement manuel, la suite de tests automatisés DOIT être au vert :

```bash
pytest
```

**Résultats attendus** :
- `tests/test_models.py` : Valide la création, la validation du champ `title`, la sauvegarde et la lecture du fichier JSON local.
- `tests/test_routes.py` : Valide les codes de réponse HTTP (200, 302), l'affichage de la liste, l'échappement HTML, la redirection après ajout et le passage d'une tâche à l'état terminée.

---

## 3. Lancement du Serveur de Développement

```bash
python run.py
```
ou :
```bash
flask --app run run
```

L'application est accessible à l'adresse : [http://localhost:5000](http://localhost:5000).

---

## 4. Scénarios de Validation de Bout en Bout

### Scénario 1 : État initial (aucun tâche)
1. Ouvrir le navigateur sur `http://localhost:5000`.
2. **Vérification** :
   - L'en-tête présente le titre de l'application et une illustration canine accueillante.
   - Un message d'accueil bienveillant invite à ajouter sa première tâche.
   - Le formulaire comporte un champ texte prêt pour la saisie et un bouton d'ajout.

### Scénario 2 : Ajout successif de plusieurs tâches (enchaînement fluide)
1. Saisir `"Préparer le cours de programmation"` dans le champ et cliquer sur **Ajouter**.
2. **Vérification** :
   - La page se réactualise instantanément (redirection PRG).
   - Le champ de saisie est de nouveau vide, prêt pour la saisie suivante.
   - La tâche apparaît dans la liste des tâches à faire.
   - Une citation de motivation canine est affichée.
3. Saisir immédiatement `"Enregistrer la vidéo explicative"` et valider.
4. **Vérification** :
   - Les deux tâches sont affichées dans leur ordre de saisie.

### Scénario 3 : Tentative de soumission d'un champ vide
1. Laisser le champ texte vide (ou taper seulement des espaces) et cliquer sur **Ajouter**.
2. **Vérification** :
   - Le système bloque l'ajout (validation HTML5 et validation côté serveur Flask).
   - Aucune tâche vide n'apparaît dans la liste.

### Scénario 4 : Marquer une tâche comme terminée
1. Cliquer sur le bouton ou la case à cocher en regard de `"Préparer le cours de programmation"`.
2. **Vérification** :
   - La tâche passe visuellement à l'état complétée (texte barré, style validé).
   - Son état `completed: true` est sauvegardé.

### Scénario 5 : Persistance après redémarrage du serveur
1. Arrêter le serveur dans le terminal (`Ctrl+C`).
2. Vérifier que le fichier `data/tasks.json` contient bien les tâches saisies.
3. Redémarrer le serveur (`python run.py`).
4. Recharger la page dans le navigateur.
5. **Vérification** :
   - La liste et les statuts des tâches sont fidèlement restitués.
