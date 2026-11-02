# Feature Specification: Compte à Rebours de Fin de Journée

**Feature Branch**: `005-end-of-day-countdown`

**Created**: 2026-11-02

**Status**: Draft

**Input**: User description: "Ajouter un compte à rebours de fin de journée à côté du chien qui encourage ## 1. Problème / Besoin Aujourd'hui, l'utilisateur n'a aucun repère du temps qu'il lui reste dans la journée pour accomplir ses tâches. Afficher un compte à rebours près du chien qui l'encourage renforce la motivation et l'aide à rester concentré. ## 2. Utilisateurs concernés Tous les utilisateurs de l'application « Tâches du jour ». ## 3. Critères d'acceptation - **Affichage** : un compte à rebours est visible dans la carte du message de motivation, à côté de l'illustration du chien qui encourage, dès qu'au moins une tâche existe. - **Calcul** : il indique le temps restant avant la fin de la journée (minuit, heure locale de l'utilisateur), au format « 05 h 32 min 10 s ». - **Mise à jour automatique** : il se met à jour chaque seconde, sans recharger la page. - **Changement de jour** : à minuit, il repart sur la nouvelle journée sans que l'utilisateur ait à recharger la page. - **État vide** : lorsqu'il n'y a aucune tâche, le compte à rebours n'est pas affiché. - **Accessibilité** : le compte à rebours a un libellé explicite pour les lecteurs d'écran (par exemple « Temps restant avant la fin de la journée ») et n'est pas annoncé seconde par seconde. - **Lisibilité** : l'affichage reste lisible sur mobile et dans le style chaleureux existant. ## 4. Hors périmètre (non inclus) - Minuteur ou chronomètre personnalisable, ou durée par tâche. - Alarme, son ou notification. - Réinitialisation des tâches à minuit. - Choix de l'heure de fin de journée ou de plusieurs fuseaux horaires. - Enregistrement de l'heure côté serveur. ## 5. Contraintes - Respecter la constitution du projet. - Aucune nouvelle dépendance ni bibliothèque. - La logique Python éventuelle est couverte par des tests pytest."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Affichage dynamique du temps restant jusqu'à la fin de la journée (Priority: P1)

En tant qu'utilisateur ayant des tâches planifiées pour ma journée, je veux visualiser en temps réel le temps qu'il me reste avant minuit à côté du chien qui m'encourage, afin d'évaluer sereinement le temps disponible et de maintenir mon engagement pour accomplir mes missions.

**Why this priority**: Il s'agit du besoin principal de l'utilisateur : disposer d'un repère temporel vivant et encourageant pour rythmer sa journée sans stress inutile.

**Independent Test**: Créer au moins une tâche dans l'application, observer la carte de motivation : le compte à rebours s'affiche immédiatement au format « HH h MM min SS s » (ex: « 05 h 32 min 10 s ») à proximité de l'illustration canine d'encouragement et se met à jour chaque seconde sans rechargement de la page.

**Acceptance Scenarios**:

1. **Given** l'utilisateur possède au moins une tâche enregistrée, **When** il affiche la page d'accueil, **Then** un compte à rebours apparaît dans la carte de motivation à côté du chien encourageant et indique le temps restant jusqu'à minuit (heure locale de l'utilisateur) au format « 05 h 32 min 10 s ».
2. **Given** le compte à rebours est visible à l'écran, **When** une seconde s'écoule, **Then** la valeur des secondes diminue d'une unité de façon fluide sans nécessiter de rafraîchissement de la page.
3. **Given** l'utilisateur navigue ou laisse la page ouverte pendant plusieurs minutes, **When** il consulte à nouveau l'affichage, **Then** le compte à rebours reflète fidèlement le temps restant réel selon l'heure locale de l'appareil.

---

### User Story 2 - Masquage automatique du compte à rebours en l'absence de tâches (Priority: P2)

En tant qu'utilisateur ouvrant l'application sans tâche active ou venant de supprimer toutes ses tâches, je veux que le compte à rebours ne soit pas affiché, afin de conserver un espace d'accueil bienveillant et apaisant qui ne met pas de pression horaire tant que mes objectifs ne sont pas posés.

**Why this priority**: Préserve la clarté et l'esprit pédagogique de l'application en évitant d'afficher une contrainte de temps lorsqu'aucune activité n'est encore planifiée.

**Independent Test**: Ouvrir l'application avec une liste vide (état initial) : vérifier l'absence totale du compte à rebours. Créer une tâche : vérifier son apparition. Supprimer la tâche : vérifier sa disparition immédiate.

**Acceptance Scenarios**:

1. **Given** aucune tâche n'est présente dans l'application (état vide initial), **When** l'utilisateur visualise l'écran d'accueil, **Then** le compte à rebours n'est pas affiché dans la carte de motivation.
2. **Given** l'utilisateur est sur l'état vide sans tâche, **When** il ajoute sa première tâche, **Then** le compte à rebours s'affiche dans la carte de motivation dès que la page présente la liste de tâches.
3. **Given** l'utilisateur ne possède qu'une seule tâche, **When** il supprime cette dernière tâche et que l'interface repasse à l'état vide, **Then** le compte à rebours est automatiquement masqué.

---

### User Story 3 - Continuité fluide lors du passage à minuit (Priority: P3)

En tant qu'utilisateur consultant l'application en fin de soirée au moment de minuit, je veux que le décompte passe naturellement au jour suivant sans bloquer, sans afficher de valeur négative et sans obliger à recharger la page, afin de garantir une expérience continue et sans rupture.

**Why this priority**: Évite un comportement dégradé ou erroné (ex: affichage de valeurs négatives ou blocage à zéro) pour les utilisateurs actifs en fin de journée ou travaillant tard.

**Independent Test**: Simuler le passage de 23:59:59 à 00:00:00 (heure locale) : vérifier que le compte à rebours passe de « 00 h 00 min 00 s » à « 23 h 59 min 59 s » pour la nouvelle journée de manière transparente.

**Acceptance Scenarios**:

1. **Given** l'application est ouverte et que l'heure locale atteint 23:59:59, **When** l'horloge passe à minuit pile (00:00:00), **Then** le compte à rebours repart immédiatement sur le décompte de la nouvelle journée (23 h 59 min 59 s) sans nécessiter de rechargement manuel de la page.

---

### User Story 4 - Accessibilité numérique et lisibilité mobile (Priority: P4)

En tant qu'utilisateur de lecteur d'écran ou utilisateur sur smartphone, je veux disposer d'un libellé explicite sans être submergé d'annonces vocales chaque seconde, et bénéficier d'une présentation claire adaptée aux écrans étroits, afin de profiter du compte à rebours dans les mêmes conditions de confort que les autres utilisateurs.

**Why this priority**: L'accessibilité et la réactivité mobile sont indispensables pour assurer une utilisation inclusive et agréable pour tous les profils d'utilisateurs.

**Independent Test**: Examiner le composant avec un lecteur d'écran pour vérifier la présence d'un libellé explicite (« Temps restant avant la fin de la journée ») et l'absence de vocalisation cadencée seconde par seconde. Tester l'affichage sur écran étroit (360px de large) pour vérifier la bonne intégration visuelle à côté du chien.

**Acceptance Scenarios**:

1. **Given** un utilisateur navigue à l'aide d'un lecteur d'écran, **When** le composant du compte à rebours est vocalisé, **Then** il fournit un libellé clair désignant sa finalité (par exemple « Temps restant avant la fin de la journée ») sans déclencher de notification sonore ou vocale à chaque seconde écoulée.
2. **Given** un utilisateur consulte l'application sur un smartphone ou un écran de faible largeur, **When** la carte de motivation est affichée, **Then** le compte à rebours reste lisible, ne déborde pas et conserve l'harmonie visuelle chaleureuse de l'application.

---

### Edge Cases

- **Mise en veille ou onglet inactif prolongé** : Lorsque l'onglet du navigateur est mis en arrière-plan pendant plusieurs minutes ou heures puis réactivé, le compte à rebours se recalcule immédiatement dès sa reprise pour afficher l'heure exacte restante, sans cumul de retard.
- **Passage à l'heure d'été ou à l'heure d'hiver** : Lors des nuits de changement d'heure saisonnier (nuit de 23 heures ou de 25 heures), le décompte s'ajuste pour refléter fidèlement le temps jusqu'au prochain minuit local sans rupture d'affichage.
- **Modification de l'horloge système locale** : Si l'utilisateur modifie manuellement l'heure de son appareil, le compte à rebours s'adapte automatiquement dès la seconde suivante en se basant sur le nouvel horaire système.
- **Toutes les tâches terminées (célébration de succès)** : Lorsque l'utilisateur a achevé l'ensemble de ses tâches (100% de complétion avec affichage de la célébration festive), le compte à rebours reste visible dans la carte de motivation tant qu'au moins une tâche existe dans la liste.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT afficher un compte à rebours dynamique dans la carte de motivation, placé à côté de l'illustration du chien encourageant, dès lors qu'au moins une tâche existe dans la liste quotidienne.
- **FR-002**: Le système DOIT masquer complètement le compte à rebours lorsqu'aucune tâche n'existe (état d'accueil vide initial).
- **FR-003**: Le compte à rebours DOIT indiquer la durée restante jusqu'à la fin de la journée calendaire, définie par minuit (00:00:00 du jour suivant) selon l'heure locale de l'appareil de l'utilisateur.
- **FR-004**: Le compte à rebours DOIT afficher le temps restant selon le format textuel standardisé « HH h MM min SS s » (ex: « 05 h 32 min 10 s »), en incluant des zéros initiaux pour conserver une largeur visuelle stable.
- **FR-005**: Le compte à rebours DOIT actualiser son affichage automatiquement chaque seconde sans requérir de rechargement ou de rafraîchissement de la page par l'utilisateur.
- **FR-006**: Lors du passage de minuit (00:00:00), le compte à rebours DOIT enchaîner de manière autonome et continue sur le décompte de la nouvelle journée sans rechargement de page et sans afficher de valeur négative.
- **FR-007**: Le compte à rebours DOIT être doté d'un libellé textuel descriptif pour les technologies d'assistance (ex: « Temps restant avant la fin de la journée ») et NE DOIT PAS générer d'annonces vocales automatiques à chaque seconde.
- **FR-008**: La disposition visuelle du compte à rebours DOIT être adaptée aux écrans d'ordinateurs comme aux appareils mobiles, en préservant le style chaleureux et bienveillant de l'application.
- **FR-009**: Le système NE DOIT PAS intégrer de chronomètre ou minuteur paramétrable, de durée allouée par tâche individuelle, de notification sonore ou alarme, de sélection de fuseaux horaires manuelle, ni d'enregistrement d'horodatage côté serveur.
- **FR-010**: Le système NE DOIT PAS supprimer, réinitialiser ou modifier l'état des tâches existantes lors du passage à minuit dans le cadre de cette fonctionnalité.

### Key Entities *(include if feature involves data)*

- **Compte à rebours de fin de journée (Daily Countdown)** :
  - *Heures restantes* : Nombre d'heures avant le prochain minuit local (00 à 23).
  - *Minutes restantes* : Nombre de minutes restantes dans l'heure en cours (00 à 59).
  - *Secondes restantes* : Nombre de secondes restantes dans la minute en cours (00 à 59).
  - *Libellé d'accessibilité* : Texte descriptif explicitant la nature de l'indicateur pour les lecteurs d'écran.
  - *État de visibilité* : Visibilité activée si au moins une tâche existe, masquée si la liste est vide.
- **Carte de motivation (Motivation Card)** :
  - *Mascotte canine* : Illustration du chien qui encourage l'utilisateur dans son parcours quotidien.
  - *Citation du jour* : Message inspirant invitant à l'action.
  - *Zone de décompte* : Emplacement dédié accueillant le compte à rebours à proximité immédiate du chien.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% des utilisateurs ayant au moins une tâche enregistrée visualisent le compte à rebours dans la carte de motivation dès le chargement de la page.
- **SC-002**: 100% des utilisateurs sans tâche (état vide) ne voient aucun compte à rebours affiché sur leur interface.
- **SC-003**: Le compte à rebours se met à jour toutes les secondes avec un écart temporel maximal de moins de 1 seconde par rapport à l'heure locale de l'appareil.
- **SC-004**: Lors du passage de minuit, 100% des sessions actives effectuent la transition vers la nouvelle journée de manière continue et sans rechargement de la page, avec 0 valeur négative constatée.
- **SC-005**: L'affichage du compte à rebours demeure lisible et sans rupture visuelle sur l'ensemble des largeurs d'écran comprises entre 320px et 2560px.
- **SC-006**: 100% des utilisateurs de lecteurs d'écran ont accès à un libellé d'accessibilité explicite sans subir d'interruptions ou d'annonces vocales intempestives à chaque seconde.

## Assumptions

- L'heure de référence pour le calcul du temps restant est l'heure locale fournie par le dispositif client de l'utilisateur.
- La « fin de journée » correspond conventionnellement à minuit pile (00:00:00) au passage à la date calendaire suivante.
- Le compte à rebours reste visible tant qu'au moins une tâche existe dans la liste, indépendamment du fait que ces tâches soient terminées ou en attente.
- L'habillage visuel du compte à rebours reprend les polices, teintes douces et motifs chaleureux existants de l'application « Tâches du jour ».
- Aucune communication réseau ni synchronisation d'heure avec un serveur n'est nécessaire pour le fonctionnement du compte à rebours.
