<!--
# Sync Impact Report
- Version change: 1.0.0 → 1.1.0
- List of modified principles:
  - II. Stack Web Épurée (HTML/CSS Natif & Backend Python) → II. Stack Web Épurée (HTML/CSS Natif & Backend Python avec Flask)
  - V. Minimalisme des Dépendances (autorise explicitement Flask comme unique dépendance backend)
- Added sections:
  - None
- Removed sections:
  - None
- Follow-up TODOs:
  - None
-->

# Tâches du Jour Constitution

## Core Principles

### I. Simplicité et Vocation Pédagogique
Le projet DOIT demeurer accessible, didactique et facile à appréhender pour des apprenants.
- L'architecture et l'organisation du code DOIVENT privilégier la clarté conceptuelle plutôt que des abstractions prématurées ou des motifs de conception superflus.
- Les principes KISS (*Keep It Simple, Stupid*) et YAGNI (*You Aren't Gonna Need It*) s'appliquent rigoureusement : aucune fonctionnalité non expressément requise ne DOIT être implémentée.
- *Rationale* : Dans un projet d'apprentissage, la lisibilité et la compréhension des flux de données priment sur la complexité d'ingénierie logicielle avancée.

### II. Stack Web Épurée (HTML/CSS Natif & Backend Python avec Flask)
La pile technologique DOIT reposer strictement sur les standards fondamentaux du web et le langage Python avec Flask.
- Le frontend DOIT être conçu exclusivement en HTML5 et CSS3 natifs, sans dépendance à des frameworks JavaScript lourds (React, Vue, Angular, etc.) ni préprocesseurs CSS superflus.
- Le backend DOIT être implémenté en Python (version 3.10 ou supérieure) en s'appuyant sur le micro-framework **Flask**, qui est l'unique dépendance backend autorisée pour le serveur web, le routage et le traitement des requêtes HTTP.
- Les mécanismes de communication entre frontend et backend DOIVENT rester directs, simples et transparents (ex. formulaires HTML standards et endpoints Flask lisibles).
- *Rationale* : La bibliothèque standard Python (`http.server`) rend le routage d'URL, la gestion des requêtes et le traitement des formulaires disproportionnément complexes et verbeux pour un projet pédagogique. Flask offre une abstraction légère, didactique et robuste tout en préservant la simplicité et la clarté du code pour des apprenants.

### III. Lisibilité et Documentation Systématique
Le code DOIT être auto-porteur, idiomatique et soigneusement documenté.
- Tout composant, fonction ou module Python DOIT comporter une docstring explicite décrivant sa responsabilité, ses paramètres d'entrée et ses valeurs de retour.
- Les sections clés du code frontend (structure sémantique HTML, organisation CSS) et backend DOIVENT comporter des commentaires explicatifs précisant *pourquoi* une solution technique spécifique est retenue.
- Le nommage des variables, fonctions, fichiers et classes DOIT être explicite et refléter sans ambiguïté le domaine fonctionnel.
- *Rationale* : Le code sert de support pédagogique ; il doit pouvoir être lu et compris comme un exemple de référence par des apprenants.

### IV. Tests Automatisés Obligatoires avec pytest (NON-NÉGOCIABLE)
La couverture de la logique applicative Python par des tests automatisés est obligatoire.
- Tout développement, correction ou refactorisation de la logique Python DOIT obligatoirement s'accompagner de tests automatisés exécutables via `pytest`.
- Aucun code backend ne DOIT être considéré comme achevé ou validé si la suite de tests `pytest` associée n'est pas exécutée avec un statut vert.
- Les cas nominaux ainsi que les cas limites ou d'erreur DOIVENT être testés de manière unitaire et explicite.
- *Rationale* : L'automatisation des tests avec `pytest` garantit la non-régression, inculque les bonnes pratiques de développement logiciel et offre un feedback immédiat aux apprenants.

### V. Minimalisme des Dépendances
Le projet DOIT minimiser drastiquement l'usage de dépendances tierces.
- À l'exception de **Flask** pour le backend applicatif et de **pytest** pour la suite de tests, la bibliothèque standard de Python (`standard library`) DOIT être privilégiée pour toutes les opérations courantes.
- Aucune autre dépendance externe ne DOIT être ajoutée sans une justification argumentée prouvant l'impossibilité ou la complexité disproportionnée d'une implémentation standard.
- Les dépendances autorisées (`flask`, `pytest`) DOIVENT être légères, stables et explicitement référencées avec leurs versions dans un fichier `requirements.txt`.
- *Rationale* : La limitation stricte des dépendances externes simplifie l'installation, facilite la maintenance, limite la surface d'attaque et garantit la maîtrise intégrale du code par les apprenants.

### VI. Hygiène de Sécurité et Absence Totale de Données Sensibles
Le dépôt de code DOIT rester strictement exempt de tout secret ou donnée sensible.
- Aucun mot de passe, jeton d'authentification, clé d'API, certificat ou donnée personnelle réelle ne DOIT être consigné dans le code source ou archivé dans le gestionnaire de versions.
- Toute variable de configuration sensible ou d'environnement DOIT transiter par des variables d'environnement documentées dans un modèle d'exemple non sensible (ex. `.env.example`).
- La configuration `.gitignore` DOIT empêcher l'ajout accidentel de secrets, de bases de données locales de test ou d'artefacts temporaires (`__pycache__`, `.pytest_cache`, `.env`, `instance/`).
- *Rationale* : L'apprentissage des réflexes de sécurité et de gestion des secrets est primordial dès les premiers projets pour prévenir toute fuite ou faille en production.

## Contraintes Techniques et Directives d'Architecture

- **Frontend** :
  - HTML5 sémantique garantissant accessibilité de base et clarté structurelle.
  - CSS3 moderne et modulaire, favorisant les variables CSS (*Custom Properties*) et la lisibilité sans framework externe.
- **Backend** :
  - Python 3 standard (3.10+), conforme aux recommandations de style PEP 8.
  - Micro-framework Flask comme unique dépendance serveur et moteur de routes.
  - Architecture modulaire claire distinguant la persistance/gestion des données, la logique métier et les routes Flask / contrôleurs.
- **Environnement & Déploiement** :
  - Utilisation d'un environnement virtuel Python (`venv`) pour l'isolation des dépendances.
  - Dépendances déclarées dans un fichier `requirements.txt` minimaliste.
  - Démarrage et exécution simples, reproductibles sur toute plateforme courante (Linux, macOS, Windows) sans configuration complexe.

## Workflow de Développement et Contrôle Qualité

- **Cycle de validation** :
  1. Spécification de la fonctionnalité ou de l'étape pédagogique.
  2. Implémentation du code et ajout systématique des commentaires explicatifs.
  3. Rédaction et exécution locale des tests `pytest` sur la logique Python.
  4. Revue de conformité : absence de données sensibles, absence de dépendances superflues au-delà de Flask et pytest, respect des règles de style.
- **Portes de qualité (*Quality Gates*)** :
  - Exécution réussie et complète de la suite `pytest`.
  - Dépôt propre (aucun fichier temporaire, cache ou secret présent).
  - Lisibilité pédagogique validée du code et de sa documentation.

## Governance

Cette constitution constitue la norme de référence du projet Tâches du Jour et prévaut sur toute décision d'implémentation ou pratique ponctuelle.
- **Autorité** : Tout ajout de code, fonctionnalité ou contribution DOIT se conformer strictement aux principes énoncés dans ce document. Toute complexité non justifiée ou dépendance superflue DOIT être refusée.
- **Procédure d'amendement** :
  - Tout amendement à la constitution DOIT être argumenté et documenté, en expliquant son impact pédagogique et technique.
  - Toute révision majeure DOIT faire l'objet d'un accord explicite sur les orientations didactiques du projet.
- **Politique de versionnement** :
  - **MAJOR** : Modification rétro-incompatible d'un principe fondamental (ex. changement de pile technologique imposée, abandon de pytest).
  - **MINOR** : Ajout d'un nouveau principe, d'une nouvelle contrainte directrice ou d'une section méthodologique, ou élargissement encadré de l'architecture.
  - **PATCH** : Clarifications rédactionnelles, corrections typographiques ou reformulations non sémantiques.

**Version**: 1.1.0 | **Ratified**: 2026-10-22 | **Last Amended**: 2026-10-22
