# Feature Specification: Calendrier et Marquage de Dates

**Feature Branch**: `006-calendar-date-picker`

**Created**: 2026-11-23

**Status**: Draft

**Input**: User description: "Afficher un calendrier Afficher un calendrier et permettre de cocher des date"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Affichage du calendrier mensuel interactif (Priority: P1)

En tant qu'utilisateur de l'application « Tâches du jour », je veux afficher un calendrier mensuel clair et accueillant, afin d'avoir une vue d'ensemble du mois en cours et de repérer instantanément la date d'aujourd'hui.

**Why this priority**: L'affichage du calendrier constitue la base visuelle et fonctionnelle indispensable de la fonctionnalité. Sans cette vue mensuelle, aucune interaction de repérage ou de cochage de dates n'est possible.

**Independent Test**: Accéder à l'application et visualiser la section calendrier : le mois et l'année en cours s'affichent correctement, les jours de la semaine sont alignés du lundi au dimanche, chaque jour du mois occupe sa case et la date du jour (« aujourd'hui ») est mise en valeur par un indicateur visuel distinctif.

**Acceptance Scenarios**:

1. **Given** l'utilisateur ouvre l'application, **When** il consulte la section du calendrier, **Then** le calendrier affiche le mois et l'année courants avec une grille de 7 colonnes correspondant aux jours de la semaine (lundi à dimanche).
2. **Given** le calendrier du mois courant est affiché, **When** l'utilisateur regarde le jour correspondant à la date actuelle, **Then** cette case est visuellement distincte des autres jours (mise en valeur dédiée « Aujourd'hui »).
3. **Given** le premier jour du mois ne commence pas un lundi, **When** la grille mensuelle est générée, **Then** les cases d'alignement précédant le 1er du mois sont positionnées harmonieusement pour respecter les jours de la semaine.

---

### User Story 2 - Cocher et décocher des dates (Priority: P1)

En tant qu'utilisateur, je veux pouvoir cliquer sur n'importe quel jour du calendrier pour cocher ou décocher cette date, afin de marquer mes journées actives, de suivre mes réussites ou d'organiser mes repères temporels.

**Why this priority**: Le besoin explicite exprimé par l'utilisateur est de « permettre de cocher des dates ». Cette capacité de marquage interactif et réversible apporte la valeur métier centrale attendue.

**Independent Test**: Cliquer sur une date non cochée (ex: le 15 du mois) : la case prend immédiatement l'état « coché » avec un symbole distinctif (empreinte de patte 🐾 ou coche verte). Cliquer à nouveau sur cette même date : la case repasse immédiatement à l'état « non coché ». Recharger la page : l'état coché ou décoché est fidèlement conservé.

**Acceptance Scenarios**:

1. **Given** une date du mois affiché est actuellement non cochée, **When** l'utilisateur clique sur cette date, **Then** la date bascule à l'état « coché », un marqueur visuel clair s'affiche sur la case, et cet état est sauvegardé de manière persistante.
2. **Given** une date du mois affiché est déjà cochée, **When** l'utilisateur clique à nouveau sur cette date, **Then** la date bascule à l'état « non coché », le marqueur visuel disparaît, et la mise à jour est immédiatement enregistrée de manière persistante.
3. **Given** l'utilisateur a coché plusieurs dates et recharge la page ou quitte l'application, **When** il revient sur le calendrier, **Then** toutes les dates précédemment cochées s'affichent avec leur statut coché préservé.

---

### User Story 3 - Navigation entre les mois (Priority: P2)

En tant qu'utilisateur, je veux pouvoir naviguer vers le mois précédent et le mois suivant, et pouvoir revenir rapidement au mois en cours, afin de consulter et marquer des dates sur différentes périodes.

**Why this priority**: La navigation temporelle permet à l'utilisateur de préparer les mois à venir ou de consulter l'historique des dates cochées au cours des mois passés.

**Independent Test**: Cliquer sur le bouton « Mois précédent » : le calendrier bascule sur le mois antérieur avec ses jours et ses dates cochées respectives. Cliquer sur « Mois suivant » : le calendrier avance d'un mois. Cliquer sur un bouton de retour rapide (« Mois en cours » ou « Aujourd'hui ») : le calendrier se repositionne immédiatement sur le mois courant.

**Acceptance Scenarios**:

1. **Given** l'utilisateur consulte le mois en cours, **When** il active le contrôle « Mois précédent », **Then** le calendrier affiche le mois antérieur avec le bon nombre de jours et l'état des dates cochées de ce mois.
2. **Given** l'utilisateur consulte un mois quelconque, **When** il active le contrôle « Mois suivant », **Then** le calendrier avance d'un mois en mettant à jour le libellé du mois, de l'année et la disposition de la grille.
3. **Given** l'utilisateur navigue sur un mois passé ou futur, **When** il clique sur « Revenir à aujourd'hui », **Then** le calendrier affiche à nouveau le mois en cours et met en valeur la date actuelle.

---

### User Story 4 - Compteur de dates cochées et bienveillance visuelle (Priority: P3)

En tant qu'utilisateur, je veux visualiser un récapitulatif du nombre de dates cochées pour le mois en cours, accompagné d'un message chaleureux dans l'esprit canin de l'application, afin de me sentir encouragé dans ma régularité.

**Why this priority**: Renforce la dimension motivante, positive et pédagogique de l'application conformément à son identité de marque et à sa constitution.

**Independent Test**: Cocher 3 dates dans le mois : un badge récapitulatif affiche « 3 jours cochés ce mois-ci » à proximité du calendrier avec un mot d'encouragement canin. Décocher une date : le compteur passe instantanément à « 2 jours cochés ce mois-ci ».

**Acceptance Scenarios**:

1. **Given** aucune date n'est cochée dans le mois affiché, **When** l'utilisateur regarde le calendrier, **Then** un indicateur discret mentionne « Aucun jour coché ce mois-ci » invitant à marquer une première journée.
2. **Given** une ou plusieurs dates sont cochées dans le mois affiché, **When** l'utilisateur consulte la section, **Then** le compteur indique le nombre exact de jours cochés (ex: « 5 jours cochés ce mois-ci ») avec une formulation grammaticale correcte au singulier et au pluriel.

---

### User Story 5 - Accessibilité au clavier et affichage adapté aux écrans mobiles (Priority: P4)

En tant qu'utilisateur naviguant au clavier, sur mobile ou avec un lecteur d'écran, je veux pouvoir parcourir les jours et cocher des dates facilement sans contrainte motrice ou visuelle, afin d'avoir une expérience inclusive et fluide sur tout appareil.

**Why this priority**: L'accessibilité numérique et l'adaptabilité mobile garantissent que l'application reste utilisable par tous les apprenants et utilisateurs, quel que soit leur terminal.

**Independent Test**: Naviguer dans la grille du calendrier avec la touche Tab et les touches fléchées : le focus visuel est clairement visible sur chaque date. Appuyer sur Entrée ou Espace : la date sélectionnée change d'état (cochée/décochée). Réduire la largeur de l'écran à 360px : la grille du calendrier reste proportionnée, sans débordement horizontal, avec des zones tactiles confortables (au moins 40x40px).

**Acceptance Scenarios**:

1. **Given** un utilisateur navigue exclusivement à l'aide du clavier, **When** il se déplace sur une case de date et presse la touche Espace ou Entrée, **Then** l'état de la date bascule entre coché et décoché avec une annonce sémantique appropriée (`aria-pressed="true"` ou `aria-pressed="false"`).
2. **Given** un utilisateur utilise un lecteur d'écran, **When** il survole ou sélectionne une case de date, **Then** la synthèse vocale énonce le nom complet du jour, de la date, du mois et de l'année (ex: « Lundi 23 novembre 2026, coché »).
3. **Given** la fenêtre du navigateur est redimensionnée sur un format mobile étroit (360px de largeur), **When** le calendrier s'affiche, **Then** les 7 colonnes s'ajustent sans provoquer de barre de défilement horizontal et chaque cellule reste facilement cliquable au doigt.

---

### Edge Cases

- **Transition d'année lors de la navigation (décembre <-> janvier)** : Lorsque l'utilisateur recule depuis janvier, le calendrier passe correctement à décembre de l'année précédente (ex: janvier 2026 -> décembre 2025). Inversement, avancer depuis décembre bascule sur janvier de l'année suivante.
- **Gestion des années bissextiles pour février** : Le mois de février doit afficher exactement 29 jours lors des années bissextiles (ex: 2024, 2028) et 28 jours les autres années (ex: 2026), sans décalage dans la grille.
- **Affichage des jours hors du mois en cours (cases vides ou jours atténués)** : Si un mois commence un vendredi, les 4 cases précédentes (lundi à jeudi) doivent être présentées comme des cellules neutres non cochables ou grisées, pour que le 1er du mois s'aligne fidèlement sous la colonne Vendredi.
- **Cochage de dates futures ou passées** : L'utilisateur est libre de cocher aussi bien des dates passées (pour enregistrer un historique) que des dates futures (pour planifier un rendez-vous ou une échéance) sans blocage artificiel.
- **Rechargement intempestif ou coupure réseau** : L'enregistrement d'une date cochée doit être résilient ; si l'utilisateur recharge la page immédiatement après un clic, l'état enregistré au moment de l'interaction doit être fidèlement restitué.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT afficher un calendrier mensuel structuré sous forme de grille hebdomadaire de 7 colonnes correspondant aux jours de la semaine, du lundi au dimanche.
- **FR-002**: Le système DOIT afficher l'intitulé du mois et l'année en cours de consultation au-dessus de la grille du calendrier (ex: « Novembre 2026 »).
- **FR-003**: Le système DOIT mettre en évidence de façon visuelle et textuelle la date correspondant au jour actuel (« Aujourd'hui ») lorsqu'elle figure dans le mois affiché.
- **FR-004**: Le système DOIT permettre à l'utilisateur de marquer une date comme cochée d'un simple clic ou appui clavier, et d'annuler ce marquage (décocher) par une action identique.
- **FR-005**: Le système DOIT afficher un indicateur visuel explicite et chaleureux sur chaque date cochée (symbole de coche ou empreinte de patte canine 🐾, couleur d'accentuation contrastée).
- **FR-006**: Le système DOIT persister l'ensemble des dates cochées de manière durable, de sorte qu'elles demeurent conservées après rafraîchissement de la page ou réouverture de l'application.
- **FR-007**: Le système DOIT proposer des commandes de navigation permettant d'afficher le mois précédent, le mois suivant, ainsi qu'un bouton de retour direct au mois courant (« Aujourd'hui »).
- **FR-008**: Le système DOIT afficher un compteur synthétique indiquant le nombre de jours cochés pour le mois actuellement affiché à l'écran.
- **FR-009**: Chaque cellule de date interactive du calendrier DOIT être accessible au clavier et comporter un attribut sémantique d'accessibilité (`aria-pressed` ou rôle équivalent) indiquant son état coché ou non coché, ainsi qu'un libellé complet lisible par synthèse vocale (ex: « Lundi 23 novembre 2026 »).
- **FR-010**: L'interface du calendrier DOIT être responsive et s'adapter harmonieusement aux formats d'écran allant des mobiles étroits (largeur 320px) aux écrans de bureau, sans provoquer de défilement horizontal indésirable.
- **FR-011**: Le système NE DOIT PAS dépendre de bibliothèques JavaScript externes, de frameworks CSS ou de polices tierces distantes, conformément aux principes de minimalisme et de stack épurée de la constitution du projet.

### Key Entities *(include if feature involves data)*

- **Date Cochée (CheckedDate)** :
  - *date_string* : Chaîne identifiant la date au format ISO 8601 calendaire standard `YYYY-MM-DD` (ex: `"2026-11-23"`).
  - *checked* : Booléen indiquant si la date est activement cochée (`True`) ou non (`False`).
  - *updated_at* : Horodatage ISO 8601 UTC de la dernière modification d'état.
- **Mois Calendaire (CalendarMonth)** :
  - *year* : Année calendaire représentée sous forme d'entier (ex: `2026`).
  - *month* : Numéro du mois sous forme d'entier compris entre 1 et 12 (ex: `11` pour novembre).
  - *total_days* : Nombre de jours dans le mois considéré (28, 29, 30 ou 31).
  - *checked_count* : Nombre total de dates cochées dans ce mois spécifique.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Le calendrier du mois s'affiche et est immédiatement prêt à l'interaction en moins d'une seconde lors du chargement de la vue.
- **SC-002**: L'état visuel d'une date (cochée ou décochée) bascule en moins de 150 millisecondes suite au clic de l'utilisateur.
- **SC-003**: 100% des dates cochées par l'utilisateur sont conservées et restituées à l'identique après redémarrage du serveur ou réouverture de l'application.
- **SC-004**: L'utilisateur peut naviguer vers le mois précédent ou suivant en une seule action (1 clic ou 1 touche clavier) sans rechargement lourd ou désagréable de la page.
- **SC-005**: 100% des éléments interactifs du calendrier (navigation et sélection des jours) sont utilisables au clavier seul via Tab, Entrée et Espace.
- **SC-006**: La grille du calendrier s'affiche sans défilement horizontal ni troncature de texte sur un écran d'une largeur de 360 pixels.
- **SC-007**: 95% des utilisateurs testeurs comprennent immédiatement comment cocher et décocher une date dès leur première consultation du calendrier, sans notice explicative.

## Assumptions

- Le calendrier utilise le fuseau horaire local du navigateur ou de la machine de l'utilisateur pour déterminer quelle date correspond à « Aujourd'hui ».
- Les semaines débutent le lundi et se terminent le dimanche, conformément aux normes en vigueur en France (ISO 8601).
- Le cochage d'une date n'est soumis à aucune restriction temporelle : l'utilisateur peut cocher n'importe quelle date passée, présente ou future.
- Les dates cochées sont enregistrées localement dans le système de persistance du projet (ex. fichier JSON dans le répertoire de données), sans nécessiter de compte utilisateur ni d'authentification.
- Le calendrier est accessible directement depuis l'application principale « Tâches du jour », sous la forme d'un composant intégré sur la page d'accueil ou d'une section dédiée claire.
