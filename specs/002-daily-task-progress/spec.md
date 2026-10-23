# Feature Specification: Suivi de la Progression Quotidienne

**Feature Branch**: `002-daily-task-progress`

**Created**: 2026-10-23

**Status**: Draft

**Input**: User description: "Afficher la progression de la journée : combien de tâches sont terminées sur le total, avec une barre de progression, et un message de félicitations spécial quand toutes les tâches sont terminées."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Affichage du compteur de tâches et de la barre de progression (Priority: P1)

En tant qu'utilisateur organisant sa journée, je veux voir en un coup d'œil combien de tâches sont terminées par rapport au nombre total de tâches prévues, ainsi qu'une barre de progression graphique qui se remplit au fur et à mesure, afin d'évaluer concrètement mon avancement et de rester motivé.

**Why this priority**: C'est le cœur de la fonctionnalité demandée. Donner une visibilité chiffrée et graphique immédiate sur l'effort accompli apporte une valeur directe et continue tout au long de la journée.

**Independent Test**: Planifier plusieurs tâches (par exemple 4 tâches) et en marquer une comme terminée. L'interface affiche immédiatement "1 sur 4 tâches terminées" avec un pourcentage de 25% et une barre de progression visuelle remplie au quart.

**Acceptance Scenarios**:

1. **Given** l'utilisateur a 4 tâches enregistrées pour sa journée dont 1 est marquée comme terminée, **When** il consulte la page d'accueil, **Then** un indicateur textuel affiche "1 sur 4 tâches terminées (25%)" et la barre de progression est remplie à 25%.
2. **Given** l'utilisateur a 4 tâches enregistrées dont 1 terminée, **When** il marque une seconde tâche comme terminée, **Then** le compteur indique immédiatement "2 sur 4 tâches terminées (50%)" et la barre de progression avance à la moitié (50%).
3. **Given** l'utilisateur a 3 tâches enregistrées dont aucune n'est terminée, **When** il consulte l'interface, **Then** le compteur affiche "0 sur 3 tâches terminées (0%)" et la barre de progression est vide (0%).

---

### User Story 2 - Message de félicitations spécial à l'achèvement complet (Priority: P2)

En tant qu'utilisateur ayant mené à bien toutes les tâches planifiées pour la journée, je veux recevoir un message de félicitations chaleureux et festif dès que la totalité de mes tâches est terminée, afin de savourer l'accomplissement de mes objectifs et de clore ma journée dans une ambiance réconfortante.

**Why this priority**: Apporte la récompense psychologique et la touche affective propre à l'application dès que l'objectif de 100% de complétion est atteint.

**Independent Test**: Marquer successivement toutes les tâches d'une liste comme terminées. Dès que la dernière tâche est validée, un message de félicitations dédié apparaît en évidence avec un visuel canin festif.

**Acceptance Scenarios**:

1. **Given** l'utilisateur a 3 tâches planifiées et 2 déjà terminées, **When** il marque la 3ème et dernière tâche comme terminée, **Then** la barre de progression atteint 100%, le compteur affiche "3 sur 3 tâches terminées (100%)", et un message spécial de félicitations ("Félicitations ! Toutes les tâches du jour sont accomplies !") apparaît en évidence avec une illustration canine joyeuse et festive.
2. **Given** toutes les tâches étaient terminées (100%) avec le message de félicitations affiché, **When** l'utilisateur ajoute une nouvelle tâche non terminée, **Then** le décompte passe à "3 sur 4 tâches terminées (75%)", la barre repasse à 75%, et le message de félicitations spécial laisse place à l'indicateur d'avancement normal et aux encouragements ordinaires.

---

### User Story 3 - Prise en compte de l'état initial sans tâche (Priority: P3)

En tant qu'utilisateur commençant une nouvelle journée sans tâche encore enregistrée, je veux que la zone de progression adopte un état neutre et bienveillant sans afficher de félicitations prématurées, afin de comprendre clairement que je dois d'abord définir mes activités du jour.

**Why this priority**: Garantit la cohérence de l'interface et évite d'induire l'utilisateur en erreur avec un faux sentiment d'accomplissement (0 tâche sur 0 ne doit pas être célébré comme un succès).

**Independent Test**: Ouvrir l'application lorsqu'aucune tâche n'est enregistrée. La page invite à créer une première tâche sans afficher le message de félicitations.

**Acceptance Scenarios**:

1. **Given** aucune tâche n'est encore enregistrée pour la journée (0 tâche au total), **When** l'utilisateur consulte la page, **Then** aucun message de félicitations n'est affiché et le compteur n'indique pas de complétion trompeuse (la barre de progression est absente ou à 0% au profit de l'invitation à créer une tâche).

---

### Edge Cases

- **Division par zéro (liste vide)** : Lorsque le total des tâches est égal à zéro, le calcul du pourcentage ne doit pas provoquer d'erreur mathématique. Le système traite le taux comme 0% et n'affiche pas les félicitations spéciales.
- **Pourcentage non entier** : Lorsque le ratio de complétion donne un nombre décimal (ex: 1 tâche sur 3 = 33,333...), le pourcentage affiché textuellement doit être arrondi à l'entier le plus proche (ex: 33%) pour une lecture simple, tandis que la jauge graphique reflète fidèlement cette proportion.
- **Grand nombre de tâches** : Si l'utilisateur planifie un nombre important de tâches (ex: plus de 30), le compteur textuel et la barre de progression doivent conserver un rendu net et lisible sans déborder de leur conteneur.
- **Persistance après rechargement** : Lorsque l'utilisateur actualise la page du navigateur ou redémarre son application, le total, le nombre de tâches achevées et le statut de félicitations doivent être fidèlement restitués à partir des tâches enregistrées.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT calculer dynamiquement le nombre total de tâches de la journée ainsi que le nombre de tâches marquées comme terminées.
- **FR-002**: Le système DOIT afficher un indicateur textuel clair indiquant le nombre de tâches terminées par rapport au nombre total de tâches (ex. "X sur Y tâches terminées") dès lors qu'au moins une tâche existe.
- **FR-003**: Le système DOIT afficher une barre de progression visuelle dont la longueur de remplissage reflète proportionnellement le pourcentage de complétion des tâches de la journée (de 0% à 100%).
- **FR-004**: Le système DOIT afficher le pourcentage d'avancement arrondi à l'entier le plus proche pour une lisibilité optimale.
- **FR-005**: Le système DOIT mettre à jour l'indicateur textuel et la barre de progression à chaque action modifiant l'état ou le volume des tâches (marquage d'une tâche comme terminée, ajout d'une nouvelle tâche).
- **FR-006**: Le système DOIT afficher un message de félicitations spécial et chaleureux lorsque 100% des tâches sont accomplies, à condition qu'au moins une tâche ait été planifiée (total > 0).
- **FR-007**: Le message de félicitations spécial DOIT être accompagné d'une illustration canine festive et valorisante marquant la réussite de la journée.
- **FR-008**: Le système NE DOIT PAS afficher le message de félicitations spécial lorsqu'aucune tâche n'est enregistrée pour la journée (total = 0).
- **FR-009**: Le système DOIT retirer automatiquement le message de félicitations spécial et réajuster la barre de progression dès qu'une nouvelle tâche non terminée est ajoutée alors que la liste était à 100% de complétion.

### Key Entities *(include if feature involves data)*

- **Progression Quotidienne (Daily Progress)** :
  - *Total des tâches* : Entier positif ou nul représentant l'ensemble des activités prévues pour la journée.
  - *Tâches terminées* : Entier positif ou nul représentant le nombre d'activités accomplies.
  - *Taux d'accomplissement* : Pourcentage compris entre 0% et 100%, correspondant au ratio des tâches terminées sur le total (vaut 0% si aucune tâche n'est enregistrée).
  - *Statut de complétion totale* : Indicateur booléen vrai si et seulement si le total des tâches est strictement supérieur à zéro et que toutes les tâches sont marquées comme terminées.
- **Message de Félicitations Spécial (Celebration Message)** :
  - *Texte* : Message positif, chaleureux et félicitant l'utilisateur pour avoir accompli l'intégralité de sa to-do list du jour.
  - *Illustration associée* : Visuel canin festif et joyeux célébrant le succès.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Le décompte des tâches et la barre de progression sont immédiatement visibles et identifiables en moins de 2 secondes dès l'affichage de la page.
- **SC-002**: L'actualisation de la jauge et du compteur après avoir coché une tâche ou ajouté une tâche se fait en moins d'une seconde.
- **SC-003**: 100% des situations où toutes les tâches prévues sont terminées (total > 0) déclenchent l'affichage du message de félicitations spécial et de son illustration canine festive.
- **SC-004**: 0% de faux positifs : aucune félicitation n'est affichée lorsqu'aucune tâche n'a été saisie pour la journée.
- **SC-005**: 100% des rechargements ou redémarrages de l'application restituent l'état d'avancement exact calculé à partir des données de tâches sauvegardées.
- **SC-006**: Au moins 95% des utilisateurs interrogés estiment que la barre de progression et le message de félicitations renforcent leur clarté d'esprit et leur motivation quotidienne.

## Assumptions

- La fonctionnalité s'appuie sur le dispositif existant de gestion des tâches quotidiennes (création et marquage d'une tâche comme terminée) sans altérer la structure élémentaire d'une tâche.
- L'affichage de la progression prend place sur la page principale de manière à être visible avant ou en tête de la liste des activités du jour.
- L'illustration canine festive fait appel aux ressources graphiques locales disponibles dans l'application (ex. illustrations de chiens enthousiastes déjà présentes dans le projet).
- Aucune notion d'archivage ou d'historique sur plusieurs jours n'est introduite dans cette version ; la progression s'applique exclusivement à la journée courante.
