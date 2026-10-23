# Research & Technical Decisions: Suivi de la Progression Quotidienne

**Feature**: `002-daily-task-progress` | **Date**: 2026-10-23

Ce document synthétise les analyses techniques et les décisions architecturales retenues pour mettre en œuvre le suivi de la progression quotidienne et la célébration des tâches terminées. Tous les choix sont rigoureusement alignés avec la constitution du projet (simplicité didactique, Flask SSR, CSS natif et couverture pytest).

---

## Décision 1 : Modélisation et Calcul des Statistiques de Progression

- **Décision** : Introduire une dataclass Python dédiée `ProgressStats` et une méthode `get_progress()` au sein de `TaskManager` dans `app/models.py`.
- **Structure de `ProgressStats`** :
  - `total`: entier représentant le nombre total de tâches de la journée.
  - `completed`: entier représentant le nombre de tâches marquées comme terminées (`completed is True`).
  - `percentage`: entier (0 à 100) correspondant à `round((completed / total) * 100)` si `total > 0`, sinon `0`.
  - `is_all_completed`: booléen vrai si et seulement si `total > 0` et `completed == total`.
- **Rationale** :
  - Isole la responsabilité du calcul mathématique et des règles métiers hors de la couche web et hors des templates de rendu.
  - Prévient de façon déterministe toute division par zéro (`ZeroDivisionError`) grâce à une condition de garde explicite.
  - Rend la logique immédiatement testable unitairement avec `pytest` sous de multiples cas de figure (liste vide, ratios décimaux, 100% de complétion).
  - Très lisible et didactique pour des apprenants en programmation Python.
- **Alternatives rejetées** :
  - *Calcul inline dans les templates Jinja2* : Rejeté car les templates doivent rester focalisés sur la présentation visuelle ; Jinja2 ne permet pas de tester unitairement la formule facilement.
  - *Calcul direct dans la vue `routes.py`* : Rejeté car la manipulation des listes d'entités `Task` appartient naturellement au domaine métier `models.py`.

---

## Décision 2 : Composant Visuel de Barre de Progression et Accessibilité

- **Décision** : Concevoir la barre de progression en HTML5 sémantique avec attributs WAI-ARIA (`role="progressbar"`, `aria-valuenow`, `aria-valuemin="0"`, `aria-valuemax="100"`, `aria-label`) et du CSS3 pur exploitant les variables CSS du projet.
- **Détail technique** :
  - Conteneur de piste : `div.progress-track` avec `role="progressbar"`.
  - Barre de remplissage : `div.progress-fill` avec un style en ligne calculé côté serveur (`style="width: {{ progress.percentage }}%;"`).
  - Transition douce CSS (`transition: width 0.4s ease;`) pour animer l'affichage lors du rechargement.
  - Indicateur textuel adjacent : `span.progress-label` affichant « **{{ progress.completed }} sur {{ progress.total }} tâches terminées ({{ progress.percentage }}%)** ».
- **Rationale** :
  - Respecte scrupuleusement le principe constitutionnel II (zéro framework JavaScript, HTML/CSS pur).
  - Assure une accessibilité numérique irréprochable pour les lecteurs d'écran grâce au rôle ARIA `progressbar`.
  - La balise native HTML `<progress>` a été écartée car ses pseudo-éléments de personnalisation (`::-webkit-progress-bar`, `::-moz-progress-bar`) sont notoirement incompatibles et complexes à styliser de manière uniforme et chaleureuse.
- **Alternatives rejetées** :
  - *Bibliothèque JavaScript de graphes ou jauges (ex: Chart.js)* : Formellement interdite par la constitution.
  - *Balise `<progress>` HTML brute* : Rejetée en raison de son incohérence stylistique multi-navigateurs.

---

## Décision 3 : Affichage du Message de Félicitations Spécial et Illustration Festive

- **Décision** : Lorsque `progress.is_all_completed` est `True`, afficher une section bienveillante dédiée aux félicitations en haut de la page, intégrant l'illustration vectorielle locale `dog-cheer.svg`.
- **Détail technique** :
  - Le fichier `app/static/images/dogs/dog-cheer.svg` est déjà présent dans le projet avec une esthétique festive (étoiles dorées, soleil chaleureux, chiot aux pattes levées).
  - Message de célébration dédié : « Félicitations ! Toutes tes missions du jour sont accomplies ! Tu peux être fier de toi ! 🐾🎉 ».
  - Si de nouvelles tâches sont ajoutées ultérieurement, `progress.is_all_completed` repasse instantanément à `False`, masquant la bannière de célébration sans friction.
- **Rationale** :
  - Répond directement à l'exigence fonctionnelle FR-006 et FR-007 de valorisation émotionnelle de l'utilisateur.
  - Réutilise les ressources existantes sans ajouter de dépendance ni d'appel réseau externe.
- **Alternatives rejetées** :
  - *Pop-up ou boîte modale JavaScript bloquante* : Rejeté (intrusif, requiert du JavaScript alors que le projet privilégie une mise en page claire en SSR).
  - *Redirection vers une page dédiée de fin de journée* : Rejeté car l'utilisateur doit garder accès à sa liste et à la possibilité d'ajouter une nouvelle tâche à tout moment.

---

## Décision 4 : Gestion de l'État Initial et Cas Limites

- **Décision** :
  - Lorsque `total == 0` : la barre de progression n'est pas affichée (ou masquée) afin de ne pas encombrer l'écran, au profit de l'état d'invitation initial (`dog-resting.svg`). Aucun message de félicitations n'est affiché.
  - Pourcentages décimaux : utilisation de la fonction standard Python `round()` pour arrondir à l'entier le plus proche (ex: 1/3 = 33%, 2/3 = 67%).
- **Rationale** :
  - Évite les confusions d'utilisabilité : féliciter un utilisateur qui n'a rien saisi serait un contresens.
  - Garantit une interface propre, sobre et chaleureuse dès la première ouverture de l'application.
- **Alternatives rejetées** :
  - *Afficher "0 sur 0 (100%)"* : Rejeté (aberration arithmétique et ergonomique).

---

## Décision 5 : Stratégie de Couverture de Tests avec pytest

- **Décision** : Développer une suite de tests automatisés exhaustive répartie entre `tests/test_models.py` et `tests/test_routes.py`.
- **Cas couverts** :
  1. **Unitaires (`test_models.py`)** :
     - Calcul avec liste vide -> total=0, completed=0, percentage=0, is_all_completed=False.
     - Calcul avec 0 tâche terminée sur N -> percentage=0.
     - Calcul avec N tâches terminées sur N -> percentage=100, is_all_completed=True.
     - Arrondis stricts (ex: 1/3 = 33, 2/3 = 67, 1/6 = 17).
     - Ajout d'une tâche à une liste déjà terminée -> is_all_completed redevient False.
  2. **Intégration HTTP (`test_routes.py`)** :
     - Vérification de la présence de la balise progressbar et des attributs ARIA dès qu'au moins 1 tâche existe.
     - Vérification de l'absence du message de félicitations sur une liste vide.
     - Vérification de l'apparition de `dog-cheer.svg` et du message festif lorsque toutes les tâches sont cochées.
- **Rationale** :
  - Conforme au principe IV de la constitution (tests automatisés non-négociables).
  - Assure un filet de sécurité complet contre toute régression fonctionnelle.
