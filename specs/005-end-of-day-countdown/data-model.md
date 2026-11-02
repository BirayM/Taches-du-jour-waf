# Data Model: Compte à Rebours de Fin de Journée

**Feature**: `005-end-of-day-countdown` | **Date**: 2026-11-02

Ce document définit les modèles de données, les états éphémères d'exécution, les règles de validation et la matrice de transition relatifs au compte à rebours de fin de journée de l'application « Tâches du Jour ».

---

## 1. Entités du Domaine

La fonctionnalité introduit un état dynamique côté client sans altérer le schéma persistant des tâches (`data/tasks.json`). Les entités manipulées se décomposent entre l'état d'affichage éphémère du timer et l'agrégat visuel de la carte de motivation.

### 1.1 Entité Éphémère : Compte à Rebours (`DailyCountdown`)

Représente l'état en mémoire vive du décompte temporel calculé à chaque seconde par le script client.

| Attribut | Type | Plage de valeurs | Obligatoire | Description |
|----------|------|------------------|-------------|-------------|
| `now` | `Date` | Horodatage valide | Oui | Instant présent selon l'horloge système locale du dispositif client. |
| `targetMidnight` | `Date` | Minuit calendaire suivant | Oui | Date cible locale fixée à `00:00:00.000` du jour suivant (`now.getDate() + 1`). |
| `diffMs` | `int` | `>= 0` | Oui | Écart en millisecondes entre `targetMidnight` et `now` (`Math.max(0, target - now)`). |
| `hours` | `int` | `0` à `23` | Oui | Nombre d'heures entières restantes jusqu'à la fin de la journée locale. |
| `minutes` | `int` | `0` à `59` | Oui | Nombre de minutes restantes dans l'heure courante. |
| `seconds` | `int` | `0` à `59` | Oui | Nombre de secondes restantes dans la minute courante. |
| `formattedText` | `str` | Format `HH h MM min SS s` | Oui | Représentation textuelle normalisée avec zéros initiaux (ex. `"05 h 32 min 10 s"`). |
| `ariaLabel` | `str` | Valeur statique | Oui | `"Temps restant avant la fin de la journée"` (fourni aux technologies d'assistance). |
| `isVisible` | `bool` | `True` / `False` | Oui | Conditionné par la présence d'au moins une tâche dans la liste de la journée. |

#### Règles de validation des données temporelles
- **Non-négativité stricte** : `diffMs >= 0`, `hours >= 0`, `minutes >= 0`, `seconds >= 0`. Aucune valeur négative n'est tolérée dans le DOM (FR-006, SC-004).
- **Formatage strict à deux chiffres** : Les composants numériques sont complétés par un zéro à gauche si inférieurs à 10 (`padStart(2, '0')`), garantissant une largeur visuelle invariable et l'absence de sautillement de mise en page.

---

### 1.2 Entité Composite : Carte de Motivation Enseignée (`MotivationCard`)

Composant d'accueil enrichi pour afficher la mascotte canine, la citation philosophique et le temps restant.

| Attribut | Type | Source | Description |
|----------|------|--------|-------------|
| `mascot` | `str` (émoji ou SVG) | Gabarit `index.html` | Repère visuel canin bienveillant (`🐶`). |
| `quote` | `Quote` | `app/quotes.py` | Objet citation contenant le texte inspirant et son auteur. |
| `countdown` | `DailyCountdown` | Rendu conditionnel | Bloc du compte à rebours présent si et seulement si `tasks|length > 0`. |

---

## 2. Matrice des États et Transitions

Le cycle de vie du compte à rebours est étroitement lié aux actions de l'utilisateur sur la liste de tâches et au flux temporel de la journée.

```text
 ┌────────────────────────────────────────────────────────┐
 │                      État Initial                      │
 │                 Aucune tâche existante                 │
 │            (tasks == [], empty-state affiché)          │
 └──────────────────────────┬─────────────────────────────┘
                            │
              Action : POST /tasks/add (1ère tâche)
                            │
                            ▼
 ┌────────────────────────────────────────────────────────┐
 │                État Décompte Actif                     │
 │          tasks >= 1, compte à rebours visible          │
 │             Format « HH h MM min SS s »               │
 └─────────────┬──────────────────────────┬───────────────┘
               │                          │
  Écoulement d'une seconde        Passage de minuit
        (Tick régulier)              (00:00:00)
               │                          │
               ▼                          ▼
 ┌──────────────────────────┐    ┌─────────────────────────┐
 │   Mise à jour DOM JS     │    │   Nouveau jour calendaire│
 │ - Décrémentation calculée│    │ - targetMidnight = J+1  │
 │ - Horloge système absolue│    │ - Décompte = 23h 59m 59s│
 └─────────────┬────────────┘    └────────────┬────────────┘
               │                              │
               └──────────────┬───────────────┘
                              │
               Action : POST /tasks/<id>/delete
                     (Dernière tâche retirée)
                              │
                              ▼
 ┌────────────────────────────────────────────────────────┐
 │                    Retour État Vide                    │
 │               tasks == [], décompte masqué             │
 │          Timer arrêté / élément absent du DOM          │
 └────────────────────────────────────────────────────────┘
```

---

## 3. Table des Transitions d'Interface

| Événement déclencheur | État avant événement | État après événement | Effet sur le Compte à Rebours |
|-----------------------|----------------------|----------------------|--------------------------------|
| **Chargement initial** sans tâche | Aucun | `tasks == []` | **Masqué** : Aucun conteneur `#countdown-container` dans le DOM. Aucun timer actif. |
| **Ajout de la 1ère tâche** (`POST /tasks/add`) | `tasks == []` | `tasks == [T1]` | **Affiché** : Le conteneur s'affiche dans `.quote-card`. L'heure restante exacte apparaît immédiatement. |
| **Ajout d'une tâche supplémentaire** | `len(tasks) >= 1` | `len(tasks) + 1` | **Maintenu** : Le compte à rebours poursuit son écoulement sans interruption ni clignotement. |
| **Complétion d'une tâche** | Tâche en cours | Tâche complétée | **Maintenu** : Le compte à rebours poursuit son écoulement. |
| **Complétion de la dernière tâche non faite** (100%) | `percentage < 100%` | `percentage == 100%` (`is_all_completed == True`) | **Maintenu** : La bannière festive de célébration apparaît, et le compte à rebours **demeure visible et actif** (Edge Case 4). |
| **Suppression d'une tâche intermédiaire** | `len(tasks) > 1` | `len(tasks) - 1` | **Maintenu** : Le compte à rebours reste visible et synchronisé avec l'heure locale. |
| **Suppression de la toute dernière tâche** | `len(tasks) == 1` | `len(tasks) == 0` | **Masqué** : L'interface revient à l'état vide. Le conteneur disparaît du DOM (FR-002, SC-002). |
| **Passage de minuit en direct** (`23:59:59` → `00:00:00`) | Fin de journée | Début de nouvelle journée | **Continuité** : La cible avance au minuit du lendemain. Affichage instantané de `23 h 59 min 59 s` sans valeur négative ni rechargement (FR-006, SC-004). |
| **Réveil après mise en veille prolongée** | Onglet en arrière-plan | Onglet réactivé | **Resynchronisation instantanée** : Calcul direct sur `new Date()` locale. Aucun retard cumulatif (Edge Case 1). |

---

## 4. Règles d'Invariance et Contraintes de Persistance

1. **Aucune persistance côté serveur** : Le temps restant ne fait l'objet d'aucune écriture dans `data/tasks.json` ni d'aucune variable de session serveur (FR-009).
2. **Indépendance vis-à-vis du statut des tâches** : Tant que le nombre total de tâches est supérieur ou égal à 1, le compte à rebours s'exécute, même si toutes les tâches sont achevées.
3. **Absence de pollution sonore** : L'état d'accessibilité `aria-live="off"` et le libellé statique masqué garantissent qu'aucune mutation de l'entité ne déclenche d'émission vocale intempestive.
