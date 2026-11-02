# Interface Contract: Web Routes, Gabarits & Script Compte à Rebours

**Feature**: `005-end-of-day-countdown` | **Date**: 2026-11-02

Ce document spécifie les contrats d'interface web, les fragments de gabarit Jinja2, le contrat d'API JavaScript client et les règles de mise en page CSS pour l'intégration du compte à rebours de fin de journée dans l'application « Tâches du Jour ».

---

## 1. Route Web Flask : `GET /` (Rendu de l'accueil)

Affiche la page d'accueil de l'application enrichie du compte à rebours conditionnel dans la carte de motivation.

### Paramètres de requête
- Aucun.

### Données injectées dans le gabarit (`index.html`)

```python
render_template(
    "index.html",
    tasks=tasks,            # List[Task] ordonnée
    quote=quote,            # MotivationalQuote
    progress=progress       # ProgressStats
)
```

### Contrat de Rendu Conditionnel Jinja2

Le bloc du compte à rebours et l'inclusion du script client DOIVENT être conditionnés par la présence d'au moins une tâche (`{% if tasks %}` ou `{% if tasks|length > 0 %}`) :

```html
<!-- Au sein de la section .quote-card dans app/templates/index.html -->
<section class="quote-card" aria-label="Message de motivation">
    <div class="quote-icon">🐶</div>
    <div class="quote-body">
        <blockquote class="quote-text">« {{ quote.text }} »</blockquote>
        <cite class="quote-author">— {{ quote.author }}</cite>
    </div>
    {% if tasks %}
    <div class="quote-countdown" id="countdown-container" role="region" aria-label="Temps restant avant la fin de la journée">
        <span class="countdown-label">Temps restant :</span>
        <time class="countdown-display" aria-live="off">
            <span id="countdown-text" aria-hidden="true">-- h -- min -- s</span>
            <span class="sr-only">Temps restant avant la fin de la journée</span>
        </time>
    </div>
    {% endif %}
</section>
```

```html
<!-- En fin de corps ou dans le bloc scripts -->
{% if tasks %}
<script defer src="{{ url_for('static', filename='js/countdown.js') }}"></script>
{% endif %}
```

---

## 2. Contrat d'Accessibilité WAI-ARIA & Balisage HTML5

Pour satisfaire scrupuleusement les critères FR-007 et SC-006 (prévention de la pollution sonore des lecteurs d'écran) :

| Élément / Attribut | Valeur contractuelle | Rôle pour l'accessibilité |
|--------------------|----------------------|---------------------------|
| `role="region"` | `"region"` sur `#countdown-container` | Délimite la zone fonctionnelle du repère temporel. |
| `aria-label` | `"Temps restant avant la fin de la journée"` | Fournit un intitulé sémantique explicite aux technologies d'assistance. |
| `aria-live` | `"off"` (ou absence stricte de polite/assertive) | Interdit formellement toute annonce vocale cadencée à chaque seconde. |
| `aria-hidden="true"` | Posé sur `#countdown-text` | Masque le texte dynamique chiffré aux lecteurs d'écran pour éviter la lecture parasite des secondes. |
| Classe `.sr-only` | Appliquée sur `<span class="sr-only">` | Masque visuellement l'intitulé tout en le rendant lisible pour les synthèses vocales. |

---

## 3. Contrat d'API JavaScript Client (`app/static/js/countdown.js`)

Le script expose des fonctions modulaires en Vanilla JS ES6+ sans effet de bord global incontrôlé :

### 3.1 `calculateRemainingTime(now = new Date())`

Calcule les composants horaires restants jusqu'au minuit local suivant.

- **Entrée** : `now` (`Date`, par défaut instant courant de l'appel).
- **Sortie** : `Object`
  ```javascript
  {
    hours: number,    // 0 à 23
    minutes: number,  // 0 à 59
    seconds: number,  // 0 à 59
    diffMs: number    // millisecondes >= 0
  }
  ```
- **Règles contractuelles** :
  - La date cible est calculée à partir de `now` : `target = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1, 0, 0, 0, 0)`.
  - `diffMs` ne doit JAMAIS être négatif (`Math.max(0, target - now)`).

### 3.2 `formatCountdown(hours, minutes, seconds)`

Formate les composants numériques selon la convention textuelle normalisée.

- **Entrée** :
  - `hours` (`number`)
  - `minutes` (`number`)
  - `seconds` (`number`)
- **Sortie** : `string` respectant l'expression régulière `/^\d{2} h \d{2} min \d{2} s$/` (ex. `"05 h 32 min 10 s"`).
- **Règle de complétion** : Chaque valeur numérique est préfixée par un zéro si elle est inférieure à 10 (`String(val).padStart(2, '0')`).

### 3.3 `initCountdown()`

Initialise le cycle de vie du décompte dans le DOM.

- **Comportement** :
  1. Recherche `#countdown-container` et `#countdown-text` dans le document.
  2. Si le conteneur est absent (`!container`), s'interrompt immédiatement sans lever d'erreur (garde pour l'état vide).
  3. Exécute immédiatement une première mise à jour pour éviter tout délai d'affichage d'une seconde.
  4. Déclenche une minuterie répétée toutes les 1 000 ms (`setInterval(update, 1000)`).
- **Événement d'amorce** : Exécuté au chargement du script (`document.readyState === 'loading' ? addEventListener('DOMContentLoaded', initCountdown) : initCountdown()`).

---

## 4. Contrat CSS (`app/static/css/style.css`)

Règles de style nécessaires pour assurer la lisibilité sur toutes résolutions (SC-005) et l'intégration harmonieuse avec la mascotte canine :

```css
/* Intégration dans la carte de motivation */
.quote-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1.25rem;
}

.quote-countdown {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    background: #FAF5EE;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);
    padding: 0.5rem 0.85rem;
    min-width: 175px;
    box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.03);
}

.countdown-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--color-text-muted);
    margin-bottom: 0.2rem;
}

.countdown-display {
    font-family: monospace, ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--color-primary);
}

/* Règle d'accessibilité utilitaire pour écran */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

/* Adaptation responsive pour écran étroit (< 600px) */
@media (max-width: 600px) {
    .quote-countdown {
        width: 100%;
        align-items: center;
        margin-top: 0.5rem;
    }
}
```

---

## 5. Route de Ressource Statique : `GET /static/js/countdown.js`

- **Méthode** : `GET`
- **Code HTTP attendu** : `200 OK`
- **En-têtes** :
  - `Content-Type`: `text/javascript; charset=utf-8` ou `application/javascript`
