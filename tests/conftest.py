"""
Fixtures pytest pour les tests automatisés de l'application Tâches du Jour.

Ce module configure un environnement de test hermétique :
il fournit une instance de l'application Flask et un client de test
associés à un fichier de stockage temporaire (tmp_path) pour ne jamais
impacter les données réelles du projet.
"""

import pytest
from app import create_app
from app.models import TaskManager


@pytest.fixture
def temp_storage_path(tmp_path):
    """Fournit un chemin de fichier temporaire pour la persistance JSON."""
    return str(tmp_path / "test_tasks.json")


@pytest.fixture
def app_instance(temp_storage_path):
    """Crée une instance de Flask configurée pour les tests avec stockage temporaire."""
    app = create_app({
        "TESTING": True,
        "DATA_FILE": temp_storage_path,
        "SECRET_KEY": "test-secret-key",
    })
    return app


@pytest.fixture
def client(app_instance):
    """Fournit un client de test HTTP pour simuler des requêtes vers l'application."""
    return app_instance.test_client()


@pytest.fixture
def task_manager(temp_storage_path):
    """Fournit une instance de TaskManager pointant sur le stockage temporaire."""
    return TaskManager(storage_path=temp_storage_path)
