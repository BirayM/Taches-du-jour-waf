"""
Module __init__.py - Fabrique applicative Flask pour Tâches du Jour.

Ce module implémente la fonction create_app() selon le patron 'Application Factory'
de Flask. Il configure les dossiers de templates et de statiques, initialise
les paramètres et enregistre les routes de l'application.
"""

from pathlib import Path
from typing import Any, Dict, Optional
from flask import Flask


def create_app(test_config: Optional[Dict[str, Any]] = None) -> Flask:
    """
    Crée et configure une instance de l'application Flask.

    Args:
        test_config: Dictionnaire optionnel pour surcharger la configuration
                     (notamment lors de l'exécution des tests avec pytest).

    Returns:
        L'instance configurée de Flask.
    """
    # Chemins absolus vers les dossiers de templates et statiques
    base_dir = Path(__file__).resolve().parent

    app = Flask(
        __name__,
        template_folder=str(base_dir / "templates"),
        static_folder=str(base_dir / "static"),
    )

    # Configuration par défaut
    # Remarque : La clé secrète est utilisée uniquement pour les messages flash
    # et sessions de développement local (aucune donnée sensible / token de prod).
    app.config.from_mapping(
        SECRET_KEY="dev-pedagogique-taches-du-jour",
        DATA_FILE="data/tasks.json",
    )

    if test_config is not None:
        app.config.update(test_config)

    # Enregistrement des routes
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
