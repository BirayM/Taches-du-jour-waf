# Feature Specification: Suppression de Tâche Individuelle

**Feature Branch**: `004-delete-task`

**Created**: 2026-10-24

**Status**: Draft

**Input**: User description: "1. Problème / Besoin Actuellement, un utilisateur ne peut pas retirer une tâche créée par erreur ou devenue obsolète. Il est nécessaire de permettre la suppression individuelle d'une tâche de la liste afin de maintenir un tableau de bord propre et à jour. 2. Utilisateurs concernés Tous les utilisateurs de l'application « Tâches du jour ». 3. Critères d'acceptation (Exigences fonctionnelles) Bouton de suppression : Chaque carte ou ligne de tâche affiche un bouton de suppression clair (ex: icône poubelle ou bouton "Supprimer") facilement accessible. Action de suppression : Un clic sur le bouton supprime définitivement la tâche ciblée via son identifiant unique. Mise à jour des statistiques : Après la suppression, le compteur de tâches (X sur Y) ainsi que la barre de progression sont immédiatement recalculés et mis à jour. Gestion de l'état vide : Si la dernière tâche est supprimée, l'application repasse sur l'état vide initial (pas de barre de progression, affichage du message d'accueil). Rétrocompatibilité HTTP : L'action utilise le patron Post/Redirect/Get (PRG) pour éviter les re-soumissions accidentelles lors d'un rafraîchissement de page. 4. Hors périmètre (Non inclus) Fenêtre modale ou pop-up de confirmation avant suppression. Corbeille de récupération ou système d'annulation (Undo / Redo). Suppression groupée de plusieurs tâches à la fois. 5. Contraintes techniques & Accessibilité Prise en charge dans app/routes.py (nouvelle route POST) et app/models.py. Bouton accessible au clavier avec libellé aria-label explicite (ex: aria-label="Supprimer la tâche : {nom}"). Suite de tests pytest complète couvrant le cas nominal et le cas d'un identifiant de tâche inexistant."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Suppression ciblée d'une tâche et mise à jour du tableau de bord (Priority: P1)

En tant qu'utilisateur organisant ses activités quotidiennes, je veux pouvoir supprimer définitivement une tâche erronée ou obsolète directement depuis sa carte dans la liste, afin que mon tableau de bord reste propre et que le compteur et la barre de progression reflètent fidèlement le travail réellement prévu.

**Why this priority**: C'est le cœur de la valeur utilisateur demandée. Sans cette action, l'utilisateur est contraint de conserver des tâches erronées qui faussent ses statistiques de progression tout au long de la journée.

**Independent Test**: Créer deux tâches (dont une terminée), cliquer sur le bouton de suppression de la tâche non terminée. La tâche ciblée disparaît immédiatement de la liste, le compteur passe instantanément à 1 sur 1 (100%), la barre de progression s'ajuste à 100%, et un rafraîchissement ultérieur de la page ne génère aucune invite de renvoi de données.

**Acceptance Scenarios**:

1. **Given** l'utilisateur a 3 tâches enregistrées (dont 1 terminée), **When** il clique sur le bouton de suppression de l'une des tâches non terminées, **Then** la tâche ciblée est définitivement supprimée, la liste n'affiche plus que les 2 tâches restantes, et l'indicateur de progression passe immédiatement à "1 sur 2 tâches terminées (50%)" avec la barre ajustée à 50%.
2. **Given** l'utilisateur a 2 tâches dont 1 terminée (progression à 50%), **When** il supprime la tâche terminée restante, **Then** la tâche disparaît, le compteur passe à "0 sur 1 tâches terminées (0%)" et la barre de progression se vide (0%).
3. **Given** une tâche vient d'être supprimée avec succès et la page s'affiche à nouveau, **When** l'utilisateur actualise la page dans son navigateur (F5 ou rechargement), **Then** la page se recharge normalement sans afficher d'avertissement de re-soumission de formulaire et la liste des tâches reste stable.

---

### User Story 2 - Retour automatique à l'état vide d'accueil lors de la suppression de la dernière tâche (Priority: P2)

En tant qu'utilisateur ayant une unique tâche dans ma liste, je veux qu'en supprimant cette dernière tâche, l'application repasse sur l'état vide d'accueil initial sans barre de progression ni compteur orphelin, afin de retrouver un écran propre m'invitant à saisir de nouvelles tâches.

**Why this priority**: Garantit la cohérence visuelle et fonctionnelle de l'application lorsqu'aucune tâche ne subsiste, évitant des calculs incohérents ou des zones graphiques vides non adaptées.

**Independent Test**: Disposer d'une seule tâche dans l'application, cliquer sur son bouton de suppression. L'application réaffiche l'écran initial avec l'illustration canine au repos et le message invitant à planifier une première tâche.

**Acceptance Scenarios**:

1. **Given** l'utilisateur n'a qu'une seule tâche dans sa liste quotidienne, **When** il clique sur le bouton de suppression de cette tâche, **Then** la tâche est définitivement supprimée, la jauge de progression et le compteur sont masqués, et le message d'accueil initial ainsi que l'illustration de repos sont réaffichés.

---

### User Story 3 - Accessibilité du bouton de suppression (Priority: P3)

En tant qu'utilisateur naviguant au clavier ou utilisant un lecteur d'écran, je veux pouvoir atteindre aisément chaque bouton de suppression, entendre un libellé clair désignant spécifiquement la tâche concernée, et déclencher la suppression avec la touche clavier appropriée, afin d'utiliser la fonctionnalité de manière autonome et sécurisée.

**Why this priority**: L'accessibilité numérique garantit que tous les utilisateurs, quel que soit leur mode d'interaction, peuvent gérer leurs tâches sans risque de mauvaise manipulation.

**Independent Test**: Utiliser exclusivement la touche Tabulation pour atteindre le bouton de suppression d'une tâche nommée "Sortir le chien", vérifier la présence d'un libellé vocal explicite "Supprimer la tâche : Sortir le chien", et déclencher la suppression avec la touche Entrée ou Espace.

**Acceptance Scenarios**:

1. **Given** une tâche intitulée "Préparer la réunion" est affichée dans la liste, **When** l'utilisateur navigue au clavier ou utilise un lecteur d'écran, **Then** le bouton de suppression est focalisable dans l'ordre séquentiel logique et restitue le libellé explicite `aria-label="Supprimer la tâche : Préparer la réunion"`.
2. **Given** le bouton de suppression d'une tâche a le focus clavier, **When** l'utilisateur appuie sur la touche Entrée ou Espace, **Then** l'action de suppression est exécutée de façon identique à un clic de souris.

---

### Edge Cases

- **Identifiant de tâche inexistant ou déjà supprimé** : Si une requête de suppression cible un identifiant introuvable (par exemple suite à une suppression concurrente, un double-clic rapide ou un signet obsolète), le système doit ignorer la demande de manière sûre et rediriger vers la page d'accueil sans déclencher d'erreur serveur ni bloquer l'interface.
- **Double-clic rapide** : Si l'utilisateur clique rapidement deux fois sur le bouton de suppression, la première requête supprime la tâche et la seconde requête est traitée sans erreur, affichant l'état mis à jour de manière transparente.
- **Suppression amenant à 100% de complétion** : Si la suppression d'une tâche non terminée laisse uniquement des tâches terminées dans la liste (ex: 2 tâches sur 3 terminées, suppression de la seule tâche non terminée restante), le taux passe à 100% et le message spécial de félicitations festif doit s'activer immédiatement.
- **Absence de confirmation** : Conformément au périmètre fonctionnel défini, la suppression est immédiate au clic, sans boîte de dialogue modale ni délai d'annulation.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT fournir un bouton de suppression clairement identifiable (icône explicite ou libellé textuel) sur chaque carte ou ligne de tâche présente dans la liste.
- **FR-002**: Le système DOIT supprimer définitivement et immédiatement la tâche ciblée de la persistance locale lors de l'activation de son bouton de suppression, en s'appuyant sur son identifiant unique.
- **FR-003**: Le système DOIT recalculer immédiatement le compteur de tâches (nombre de tâches terminées sur nombre total de tâches restantes) après chaque suppression.
- **FR-004**: Le système DOIT recalculer et mettre à jour immédiatement la barre de progression graphique ainsi que le pourcentage d'achèvement après chaque suppression.
- **FR-005**: Le système DOIT basculer l'affichage vers l'état vide d'accueil initial (masquage de la barre de progression et du compteur, restitution du message d'accueil et du visuel canin de repos) lorsque la dernière tâche restante est supprimée.
- **FR-006**: Le système DOIT appliquer le patron Post/Redirect/Get (PRG) pour toute action de suppression afin d'éviter tout avertissement de re-soumission de formulaire lors d'un rafraîchissement de la page par l'utilisateur.
- **FR-007**: Le système DOIT gérer sans erreur applicative toute demande de suppression ciblant un identifiant de tâche inexistant ou invalide en redirigeant l'utilisateur de manière transparente vers l'affichage à jour de la liste.
- **FR-008**: Chaque bouton de suppression DOIT être accessible au clavier (focalisable et activable via les touches standard) et comporter un libellé d'accessibilité explicite au format `aria-label="Supprimer la tâche : {nom}"`.
- **FR-009**: Le système NE DOIT PAS afficher de fenêtre modale de confirmation, NE DOIT PAS proposer de corbeille de récupération ou système d'annulation (Undo/Redo), et NE DOIT PAS permettre la suppression groupée de plusieurs tâches à la fois dans ce périmètre.

### Key Entities *(include if feature involves data)*

- **Tâche (Daily Task)** :
  - *Identifiant* : Identifiant unique utilisé pour cibler avec exactitude la tâche à supprimer.
  - *Intitulé* : Libellé textuel de la tâche, injecté dans l'attribut d'accessibilité du bouton de suppression.
  - *Statut* : État (`à faire` ou `terminée`), déterminant le recalcul des statistiques après la suppression.
- **Tableau de bord (Dashboard / Suivi quotidien)** :
  - *Compteur de tâches* : Ratio entre tâches terminées et total des tâches planifiées, recalculé après suppression.
  - *Jauge de progression* : Pourcentage d'avancement reflétant proportionnellement les tâches restantes.
  - *État d'accueil* : Mode d'affichage activé lorsqu'aucune tâche ne subsiste (total = 0).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% des demandes de suppression d'une tâche existante retirent définitivement la tâche ciblée sans altérer l'ordre ni l'intégrité des autres tâches de la liste.
- **SC-002**: Le recalcul et l'actualisation du compteur et de la jauge de progression s'effectuent en moins d'une seconde après le clic de suppression.
- **SC-003**: 100% des suppressions de la dernière tâche restante basculent l'application vers l'état d'accueil initial sans afficher de statistiques résiduelles ou incohérentes.
- **SC-004**: 100% des rafraîchissements de page intervenant après une suppression s'effectuent sans aucune invite ou boîte d'avertissement de re-soumission de formulaire du navigateur (conformité PRG totale).
- **SC-005**: 100% des boutons de suppression sont actionnables au clavier et fournissent un libellé textuel d'accessibilité individualisé intégrant le nom de la tâche.
- **SC-006**: 0 crash applicatif ou erreur bloquante (erreur 500) n'est généré lors d'une tentative de suppression d'un identifiant inexistant ou déjà supprimé.

## Assumptions

- La persistance des tâches s'effectue de manière synchrone dans le mécanisme de stockage local de l'application.
- L'absence de boîte de confirmation est un choix délibéré de simplicité ergonomique conformément au périmètre d'exclusion fonctionnelle.
- Les utilisateurs disposent d'un navigateur web supportant les formulaires HTML et les attributs d'accessibilité ARIA standards.
