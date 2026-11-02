/**
 * Tâches du Jour - Compte à rebours de fin de journée
 *
 * Conforme à la constitution du projet :
 * - JavaScript Vanilla pur (ES6+), sans dépendance tierce ni bundler (Principe II & V)
 * - Code pédagogique, auto-porteur et documenté (Principe III)
 * - Calculs temporels basés sur l'horloge système absolue du navigateur client
 */

/**
 * Calcule les composants horaires restants jusqu'au minuit calendaire suivant.
 *
 * La date cible est calculée dynamiquement au jour suivant (J+1) à 00:00:00.000.
 * L'usage de Math.max(0, target - now) garantit l'absence stricte de valeurs négatives.
 *
 * @param {Date} [now=new Date()] - Instant présent servant de référence temporelle.
 * @returns {{ hours: number, minutes: number, seconds: number, diffMs: number }}
 *   Composants horaires décomposés et différence en millisecondes.
 */
function calculateRemainingTime(now = new Date()) {
    // Calcul de l'instant minuit de la nuit suivante dans le fuseau horaire local
    const target = new Date(
        now.getFullYear(),
        now.getMonth(),
        now.getDate() + 1,
        0, 0, 0, 0
    );

    // Écart en millisecondes, strictement supérieur ou égal à zéro
    const diffMs = Math.max(0, target.getTime() - now.getTime());

    // Conversion en secondes totales entières plafonnées à 86 399 s (23 h 59 min 59 s)
    // Au passage exact de minuit (00:00:00), le décompte repart instantanément à 23 h 59 min 59 s
    // conformément aux spécifications du modèle de données (heures comprises entre 0 et 23).
    const totalSeconds = Math.min(86399, Math.floor(diffMs / 1000));

    // Décomposition en heures, minutes et secondes
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    return { hours, minutes, seconds, diffMs };
}

/**
 * Formate les composants horaires selon la convention normalisée « HH h MM min SS s ».
 *
 * Chaque composant numérique est préfixé d'un zéro si inférieur à 10 via padStart(2, '0'),
 * assurant une largeur visuelle fixe et évitant les sautillements de disposition (layout shifts).
 *
 * @param {number} hours - Heures restantes (0 à 23).
 * @param {number} minutes - Minutes restantes (0 à 59).
 * @param {number} seconds - Secondes restantes (0 à 59).
 * @returns {string} Chaîne normalisée (ex: "05 h 32 min 10 s").
 */
function formatCountdown(hours, minutes, seconds) {
    const h = String(hours).padStart(2, '0');
    const m = String(minutes).padStart(2, '0');
    const s = String(seconds).padStart(2, '0');
    return `${h} h ${m} min ${s} s`;
}

/**
 * Initialise le cycle de vie du compte à rebours dans le DOM.
 *
 * 1. Recherche les éléments nécessaires dans l'arborescence DOM.
 * 2. Si le conteneur ou le texte est absent (état vide sans tâche), s'arrête immédiatement.
 * 3. Exécute un rafraîchissement immédiat à l'affichage pour éviter toute latence visuelle.
 * 4. Cadence les rafraîchissements périodiques toutes les 1 000 ms via setInterval.
 */
function initCountdown() {
    const container = document.getElementById('countdown-container');
    const textEl = document.getElementById('countdown-text');

    // Garde défensive : si le conteneur n'est pas dans la page, arrêt sans erreur
    if (!container || !textEl) {
        return;
    }

    /**
     * Met à jour le texte du compte à rebours avec l'heure courante exacte.
     */
    function update() {
        const { hours, minutes, seconds } = calculateRemainingTime();
        textEl.textContent = formatCountdown(hours, minutes, seconds);
    }

    // Mise à jour immédiate pour éviter le délai initial d'une seconde
    update();

    // Actualisation cadencée chaque seconde
    setInterval(update, 1000);
}

// Déclenchement automatique selon l'état de chargement du document
if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCountdown);
    } else {
        initCountdown();
    }
}
