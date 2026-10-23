"""
Module quotes.py - Citations bienveillantes et positives sur le thème des chiens.

Ce module expose une collection statique de citations motivantes
et une fonction de sélection aléatoire utilisant la bibliothèque standard (random).
"""

import random
from typing import Dict, List

# Collection prédéfinie de citations positives et canines
QUOTES: List[Dict[str, str]] = [
    {
        "text": "Remue la queue et avance avec joie : chaque petit pas compte !",
        "author": "Max le Berger Allemand",
    },
    {
        "text": "Un os à la fois : reste concentré sur ta tâche du moment.",
        "author": "Luna le Golden Retriever",
    },
    {
        "text": "Même la plus longue promenade commence par un premier coup de patte.",
        "author": "Rocky le Jack Russell",
    },
    {
        "text": "Fais une pause grattouilles si besoin, puis repars avec le sourire !",
        "author": "Bella le Cavalier King Charles",
    },
    {
        "text": "Ton travail et ta persévérance aujourd'hui seront récompensés !",
        "author": "Sammy le Samoyède",
    },
    {
        "text": "Garde la truffe au vent et poursuis tes objectifs avec fidélité.",
        "author": "Milo le Corgi",
    },
    {
        "text": "Sois aussi déterminé et enthousiaste qu'un chiot qui attrape sa balle !",
        "author": "Daisy le Labrador",
    },
]

# Message d'accueil bienveillant affiché lorsqu'aucune tâche n'est encore enregistrée
WELCOME_QUOTE: Dict[str, str] = {
    "text": "Prêt pour une journée productive ? Ton fidèle compagnon t'attend pour ajouter ta première tâche !",
    "author": "Ton compagnon à quatre pattes",
}


def get_random_quote() -> Dict[str, str]:
    """
    Sélectionne une citation motivante aléatoire parmi la collection.

    Returns:
        Dictionnaire avec les clés 'text' et 'author'.
    """
    return random.choice(QUOTES)
