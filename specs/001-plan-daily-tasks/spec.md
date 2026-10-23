# Feature Specification: Planification des Tâches du Jour

**Feature Branch**: `001-plan-daily-tasks`

**Created**: 2026-10-22

**Status**: Draft

**Input**: User description: "Une application web pour planifier ses tâches de la journée. Un formulaire permet d'ajouter une tâche et de la valider, puis d'en ajouter une autre. Une fois les tâches saisies, elles s'affichent en liste avec un petit message de motivation. Le design est chaleureux, avec des illustrations de chiens un peu partout."

## Clarifications

### Session 2026-10-22
- Q: Les tâches affichées dans la liste peuvent-elles être cochées comme terminées ou supprimées dans cette première version ? → A: Cocher comme terminée uniquement (sans option de suppression).
- Q: Comment le message de motivation doit-il évoluer au cours de la journée ? → A: Message aléatoire tiré d'une liste prédéfinie de citations positives et canines.
- Q: Les tâches saisies doivent-elles être conservées après l'arrêt ou le redémarrage du serveur ? → A: Persistance locale simple (fichier local préservant les tâches entre redémarrages).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Saisie et enchaînement d'ajout de tâches (Priority: P1)

En tant qu'utilisateur souhaitant organiser ma journée, je veux pouvoir saisir l'intitulé d'une tâche dans un formulaire, valider son ajout et pouvoir immédiatement saisir la tâche suivante sans friction, afin de lister rapidement toutes mes activités quotidiennes.

**Why this priority**: C'est le flux d'entrée principal sans lequel aucune planification n'est possible (MVP absolu).

**Independent Test**: L'utilisateur accède à la page d'accueil, saisit le titre d'une tâche dans le champ de saisie, valide le formulaire. La page confirme l'enregistrement, conserve ou réinitialise le champ de saisie prêt pour la tâche suivante.

**Acceptance Scenarios**:

1. **Given** l'utilisateur est sur la page de planification avec le formulaire vide, **When** il saisit "Préparer le cours de programmation" et valide l'ajout, **Then** la tâche est enregistrée, le formulaire est réinitialisé et le champ reste disponible pour saisir immédiatement une nouvelle tâche.
2. **Given** l'utilisateur est sur le formulaire d'ajout, **When** il soumet le formulaire avec un champ vide ou uniquement composé d'espaces, **Then** le système refuse la soumission et affiche un avertissement clair demandant de renseigner un intitulé.

---

### User Story 2 - Affichage de la liste des tâches, suivi et message de motivation (Priority: P2)

En tant qu'utilisateur ayant planifié mes tâches, je veux visualiser l'ensemble de mes tâches du jour sous forme de liste claire, pouvoir marquer une tâche comme terminée et lire un message bienveillant et motivant, afin de rester encouragé et concentré sur mes objectifs.

**Why this priority**: Permet à l'utilisateur de consulter son planning, de suivre l'avancement de sa journée et d'obtenir un encouragement positif pendant son travail.

**Independent Test**: Après avoir ajouté une ou plusieurs tâches, l'utilisateur voit apparaître la liste ordonnée des tâches saisies, peut cocher une tâche comme terminée pour voir son statut mis à jour, et voit un message de motivation bien visible.

**Acceptance Scenarios**:

1. **Given** aucune tâche n'est encore enregistrée pour la journée, **When** l'utilisateur consulte la page, **Then** un message d'accueil invitant à créer sa première tâche s'affiche, accompagné d'une illustration canine amicale.
2. **Given** au moins une tâche a été ajoutée (ex: "Relire les exercices"), **When** la page se réactualise après l'ajout, **Then** la liste affiche la tâche "Relire les exercices" et un message de motivation sélectionné aléatoirement parmi une liste de citations positives et canines est affiché en évidence.
3. **Given** une tâche non terminée est affichée dans la liste, **When** l'utilisateur coche la tâche pour la marquer comme terminée, **Then** la tâche prend visuellement l'état terminé (intitulé barré ou indicateur visuel complété) et son état est préservé.
4. **Given** des tâches ont été enregistrées, **When** le serveur ou l'application est redémarré, **Then** la liste et les statuts des tâches sont fidèlement rechargés à partir du stockage local.

---

### User Story 3 - Expérience visuelle chaleureuse avec illustrations canines (Priority: P3)

En tant qu'utilisateur, je veux profiter d'une interface graphique chaleureuse et réconfortante, enrichie d'illustrations de chiens bien intégrées, afin de rendre la planification quotidienne agréable, déstressante et ludique.

**Why this priority**: Renforce l'engagement émotionnel et concrétise l'identité visuelle demandée ("chaleureux, avec des illustrations de chiens un peu partout").

**Independent Test**: Vérifier visuellement la présence d'une palette de couleurs chaleureuses, d'une typographie accueillante et d'illustrations de chiens adaptées à l'état de la page (bannière, zone vide, liste des tâches).

**Acceptance Scenarios**:

1. **Given** l'utilisateur navigue sur n'importe quel écran de l'application, **When** la page s'affiche, **Then** les éléments graphiques (illustrations de chiens, tons chauds, cartes conviviales) sont visibles et harmonieusement agencés sans gêner la lisibilité du texte.

---

### Edge Cases

- **Tâche avec texte très long** : Lorsque l'utilisateur saisit une description de plus de 200 caractères, le système doit tronquer ou encapsuler proprement le texte dans la carte d'affichage pour préserver la mise en page sans déborder.
- **Caractères spéciaux et balises** : Si l'utilisateur saisit des caractères spéciaux (`<`, `>`, `&`, guillemets, émojis), le texte doit être échappé et rendu fidèlement sous forme de texte brut pour éviter toute anomalie d'affichage.
- **Liste vide au démarrage** : Lorsque la journée commence et qu'aucune tâche n'est créée, l'interface doit afficher un état vide (*empty state*) bienveillant avec une illustration canine au repos plutôt qu'une zone vide et abrupte.
- **Périmètre des actions** : La suppression de tâches est expressément exclue de cette version initiale ; seules la création et la complétion (cochage) sont supportées.
- **Fichier de stockage inexistant ou vide** : Si le fichier local de persistance n'existe pas encore lors du premier lancement, le système doit le créer automatiquement sans lever d'erreur bloquante.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT fournir un formulaire de saisie permettant d'entrer l'intitulé d'une nouvelle tâche du jour.
- **FR-002**: Le système DOIT valider l'intitulé d'une tâche à la soumission (refus des entrées vides ou composées exclusivement d'espaces) et afficher un message d'aide explicite en cas d'erreur.
- **FR-003**: Le système DOIT enregistrer la tâche et réinitialiser automatiquement le champ de saisie afin de permettre l'ajout successif de plusieurs tâches sans rechargement lourd ni navigation complexe.
- **FR-004**: Le système DOIT afficher la liste ordonnée des tâches enregistrées pour la journée en cours avec leur état (à faire ou terminée).
- **FR-005**: Le système DOIT afficher un message d'encouragement et de motivation sélectionné aléatoirement parmi une liste prédéfinie de citations positives et canines dès qu'au moins une tâche est enregistrée.
- **FR-006**: Le système DOIT afficher un état d'attente convivial lorsqu'aucune tâche n'est encore planifiée.
- **FR-007**: L'interface DOIT adopter une charte graphique chaleureuse (tons doux et accueillants) et intégrer des illustrations de chiens de manière cohérente à travers les différentes sections de la page.
- **FR-008**: Les utilisateurs DOIVENT pouvoir cocher/marquer une tâche comme terminée directement depuis la liste, sans option de suppression dans cette première version.
- **FR-009**: Le système DOIT persister les tâches de manière simple dans un stockage local (fichier dédié) garantissant leur conservation en cas de rechargement ou de redémarrage de l'application.

### Key Entities *(include if feature involves data)*

- **Tâche (Daily Task)** :
  - *Identifiant* : Référence unique de la tâche.
  - *Intitulé* : Texte descriptif de l'activité à accomplir (court et explicite).
  - *Date de création / Ordre* : Position ou horodatage permettant de restituer les tâches dans l'ordre de saisie.
  - *Statut* : État de la tâche (`à faire` ou `terminée`).
  - *Stockage* : Persisté dans un fichier local dédié, lisible et manipulable simplement.
- **Message de Motivation (Motivational Quote)** :
  - *Texte* : Citation positive et canine issue d'une collection prédéfinie.
  - *Comportement* : Sélection aléatoire parmi la liste prédéfinie lors de l'affichage.
- **Illustration Canine (Dog Asset)** :
  - *Rôle contextuel* : Visuel chaleureux associé aux différents états (accueil, liste active, tâche terminée).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Un utilisateur peut saisir et valider une nouvelle tâche en moins de 10 secondes.
- **SC-002**: L'enchaînement de la saisie de 3 tâches consécutives peut être réalisé en moins de 30 secondes sans perte de contexte.
- **SC-003**: 100 % des tâches ajoutées avec un intitulé valide apparaissent instantanément dans la liste affichée à l'écran.
- **SC-004**: Le changement d'état d'une tâche (cochée comme terminée) est répercuté visuellement en moins d'une seconde.
- **SC-005**: 100 % des tâches créées ou complétées sont récupérées intactes après redémarrage du serveur.
- **SC-006**: 95 % des utilisateurs testés perçoivent l'ambiance visuelle comme chaleureuse, déstressante et motivante lors de leur première session.
- **SC-007**: Aucune erreur de saisie (champ vide, caractères spéciaux) ne provoque de plantage ou de rupture d'affichage sur l'interface.

## Assumptions

- L'application est utilisée localement ou dans un cadre individuel mono-utilisateur pour la journée courante ; la gestion de comptes utilisateurs multiples ou d'authentification n'est pas requise pour cette première version.
- Les illustrations de chiens utilisées sont libres de droits ou intégrées sous forme d'éléments vectoriels/images légères intégrées localement, sans dépendre de services externes en ligne.
- Les tâches sont persistées localement dans un fichier dédié, garantissant la conservation de la liste entre les sessions et les redémarrages.
- La suppression de tâches n'est pas active dans cette version initiale afin de préserver la simplicité d'apprentissage.
