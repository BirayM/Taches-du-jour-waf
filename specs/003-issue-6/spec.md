## 1. Problème / Besoin
Actuellement, un utilisateur ne peut pas retirer une tâche créée par erreur ou devenue obsolète. Il est nécessaire de permettre la suppression individuelle d'une tâche de la liste afin de maintenir un tableau de bord propre et à jour.

## 2. Utilisateurs concernés
Tous les utilisateurs de l'application « Tâches du jour ».

## 3. Critères d'acceptation (Exigences fonctionnelles)
- [ ] **Bouton de suppression :** Chaque carte ou ligne de tâche affiche un bouton de suppression clair (ex: icône poubelle ou bouton "Supprimer") facilement accessible.
- [ ] **Action de suppression :** Un clic sur le bouton supprime définitivement la tâche ciblée via son identifiant unique.
- [ ] **Mise à jour des statistiques :** Après la suppression, le compteur de tâches (X sur Y) ainsi que la barre de progression sont immédiatement recalculés et mis à jour.
- [ ] **Gestion de l'état vide :** Si la dernière tâche est supprimée, l'application repasse sur l'état vide initial (pas de barre de progression, affichage du message d'accueil).
- [ ] **Rétrocompatibilité HTTP :** L'action utilise le patron Post/Redirect/Get (PRG) pour éviter les re-soumissions accidentelles lors d'un rafraîchissement de page.

## 4. Hors périmètre (Non inclus)
- Fenêtre modale ou pop-up de confirmation avant suppression.
- Corbeille de récupération ou système d'annulation (Undo / Redo).
- Suppression groupée de plusieurs tâches à la fois.

## 5. Contraintes techniques & Accessibilité
- Prise en charge dans `app/routes.py` (nouvelle route POST) et `app/models.py`.
- Bouton accessible au clavier avec libellé `aria-label` explicite (ex: `aria-label="Supprimer la tâche : {nom}"`).
- Suite de tests `pytest` complète couvrant le cas nominal et le cas d'un identifiant de tâche inexistant.
