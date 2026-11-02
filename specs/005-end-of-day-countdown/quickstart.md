# Quickstart & Validation Guide: Compte à Rebours de Fin de Journée

**Feature**: `005-end-of-day-countdown` | **Date**: 2026-11-02

Ce guide fournit la méthodologie opérationnelle et les scénarios de test pour valider de bout en bout le bon fonctionnement du compte à rebours de fin de journée, tant par tests automatisés `pytest` que par vérification visuelle et interactive.

Pour les détails d'intégration HTML/CSS/JS, consulter [contracts/web-routes.md](contracts/web-routes.md). Pour les modèles de données et transitions temporelles, se référer à [data-model.md](data-model.md).

---

## 1. Prérequis & Environnement

- **Python** : Version 3.10 ou supérieure installée (`python3 --version`).
- **Navigateur moderne** : Chrome, Firefox, Safari ou Edge avec support ECMAScript 6+ standard.
- **Activation de l'environnement virtuel** :
  ```bash
  source .venv/bin/activate
  ```
- **Dépendances** :
  ```bash
  pip install -r requirements.txt
  ```

---

## 2. Exécution des Tests Automatisés avec pytest

Lancer la suite complète de tests de l'application :

```bash
pytest
```

**Comportements validés dans `tests/test_routes.py`** :
1. **Condition de visibilité Jinja2** :
   - Requête `GET /` sans tâche en base : vérification de l'absence totale de l'élément `#countdown-container` et de l'inclusion de `countdown.js` (SC-002).
   - Requête `GET /` avec au moins une tâche créée : présence de `#countdown-container` et de la balise `<script defer src=".../countdown.js">` (SC-001).
   - Requête `GET /` avec 100% des tâches terminées : présence conjointe de la carte de célébration festive `.celebration-card` et du compte à rebours `#countdown-container` (Edge Case 4).
2. **Accessibilité numérique et ARIA** :
   - Présence de `aria-label="Temps restant avant la fin de la journée"`.
   - Présence de `aria-live="off"`.
   - Présence de la balise `<time>` et du libellé `.sr-only`.
3. **Disponibilité des fichiers statiques** :
   - `GET /static/js/countdown.js` retourne un statut HTTP 200 avec le type MIME adéquat.
   - Présence des identifiants et fonctions nécessaires dans le contenu distribué.

---

## 3. Lancement du Serveur Web Local

```bash
python run.py
```

L'application est accessible à l'adresse locale : [http://localhost:5000](http://localhost:5000).

---

## 4. Scénarios de Validation Manuelle de Bout en Bout

### Scénario 1 : Absence du compte à rebours à l'état vide initial (FR-002, SC-002)
1. Ouvrir l'application sur [http://localhost:5000](http://localhost:5000) sans tâche enregistrée (au besoin supprimer les tâches existantes).
2. Observer la carte de motivation (`.quote-card`) contenant la mascotte canine 🐶 et la citation.
3. **Résultat attendu** :
   - Aucun compte à rebours n'est affiché.
   - Inspecter le code source du DOM (F12) : l'élément `#countdown-container` n'existe pas dans le DOM.

### Scénario 2 : Apparition et défilement dynamique du compte à rebours dès la 1ère tâche (FR-001, FR-004, FR-005, SC-001, SC-003)
1. Saisir une tâche dans le formulaire : `"Préparer la réunion de projet"` et valider.
2. Observer immédiatement la carte de motivation à côté du chien 🐶.
3. **Résultat attendu** :
   - Le bloc de décompte apparaît immédiatement.
   - Le texte affiche le temps restant sous le format strict `HH h MM min SS s` (ex. `06 h 42 min 18 s`), avec des zéros initiaux si les valeurs sont inférieures à 10.
   - À chaque seconde écoulée, les secondes diminuent d'une unité de façon fluide, sans aucun rechargement ou clignotement de la page.

### Scénario 3 : Disparition immédiate lors de la suppression de la dernière tâche (FR-002, SC-002)
1. Disposer d'une seule tâche dans la liste.
2. Cliquer sur le bouton de suppression (🗑️) de cette tâche.
3. **Résultat attendu** :
   - La liste repasse à l'état vide d'accueil avec le chiot au repos (`dog-resting.svg`).
   - Le compte à rebours est automatiquement masqué.

### Scénario 4 : Maintien du compte à rebours lors de la célébration à 100% (Edge Case 4)
1. Créer une tâche et la marquer comme terminée via la case à cocher ✓.
2. La bannière festive s'affiche (`dog-cheer.svg` avec « Bravo ! Toutes les missions du jour sont terminées ! »).
3. **Résultat attendu** :
   - Le compte à rebours reste visible et continue d'égrener les secondes normalement dans la carte de motivation.

### Scénario 5 : Résilience à la mise en arrière-plan et au sommeil d'onglet (Edge Case 1)
1. Ouvrir la page avec une tâche active.
2. Noter l'heure affichée par le compte à rebours.
3. Basculer sur un autre onglet du navigateur ou minimiser la fenêtre pendant 2 à 3 minutes.
4. Revenir sur l'onglet de l'application.
5. **Résultat attendu** :
   - Le décompte affiche instantanément l'heure exacte réelle calée sur l'horloge système, sans aucun décalage cumulatif dû au bridage de minuterie du navigateur.

### Scénario 6 : Continuité fluide lors du passage de minuit (FR-006, SC-004)
1. Dans la console développeur du navigateur (F12 > Console), tester le passage de minuit ou simuler un instant à 23:59:58 :
   ```javascript
   // Vérification de la fonction de calcul
   const t1 = calculateRemainingTime(new Date(2026, 10, 2, 23, 59, 59));
   console.log(formatCountdown(t1.hours, t1.minutes, t1.seconds)); // "00 h 00 min 01 s"
   const t2 = calculateRemainingTime(new Date(2026, 10, 3, 0, 0, 0));
   console.log(formatCountdown(t2.hours, t2.minutes, t2.seconds)); // "23 h 59 min 59 s"
   ```
2. **Résultat attendu** :
   - Au passage de minuit (00:00:00), le décompte passe immédiatement à `23 h 59 min 59 s` sans valeur négative et sans nécessiter de rafraîchissement manuel de la page.

### Scénario 7 : Accessibilité aux lecteurs d'écran et adaptabilité responsive (FR-007, FR-008, SC-005, SC-006)
1. Inspecter l'élément `#countdown-container` :
   - Il dispose de l'attribut `aria-label="Temps restant avant la fin de la journée"`.
   - Il ne possède pas `aria-live="polite"` ni `aria-live="assertive"` (ou possède `aria-live="off"`).
   - Le texte changeant chaque seconde possède `aria-hidden="true"`.
2. Tester le comportement sur émulateur mobile (largeur 360px) :
   - Le compte à rebours s'adapte sans déborder, la carte reste harmonieuse et lisible.
