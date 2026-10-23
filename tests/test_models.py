"""
Tests unitaires pour les modèles et la persistance des tâches (app/models.py).

Couvre les exigences :
- Validation de l'intitulé (non vide, suppression des espaces, 1 à 200 caractères).
- Persistance et relecture dans le fichier JSON.
- Marquage d'une tâche comme terminée et préservation après redémarrage simulé.
- Tri chronologique des tâches.
"""

import pytest
from app.modey import Task, TaskManager, TaskValidationError


def test_task_creation_valid():
    """Vérifie la création valide d'une tâche avec valeurs par défaut."""
    task = Task(id="t1", title="Préparer le cours")
    assert task.id == "t1"
    assert task.title == "Préparer le cours"
    assert task.completed is False
    assert task.created_at != ""


def test_task_title_stripped():
    """Vérifie que les espaces superflus en début et fin d'intitulé sont nettoyés."""
    task = Task(id="t2", title="   Faire une promenade canine   ")
    assert task.title == "Faire une promenade canine"


@pytest.mark.parametrize("invalid_title", [
    "",
    "   ",
    "\t\n",
])
def test_task_title_empty_raises_error(invalid_title):
    """Vérifie le rejet d'un intitulé vide ou composé uniquement d'espaces."""
    with pytest.raises(TaskValidationError, match="ne doit pas être vide"):
        Task(id="t3", title=invalid_title)


def test_task_title_too_long_raises_error():
    """Vérifie le rejet d'un intitulé dépassant 200 caractères."""
    long_title = "A" * 201
    with pytest.raises(TaskValidationError, match="ne doit pas dépasser 200 caractères"):
        Task(id="t4", title=long_title)


def test_task_title_boundary_200_chars():
    """Vérifie qu'un intitulé de pile 200 caractères est accepté."""
    title_200 = "B" * 200
    task = Task(id="t5", title=title_200)
    assert len(task.title) == 200


def test_task_manager_add_task(task_manager):
    """Vérifie l'ajout d'une tâche via le gestionnaire et la persistance JSON."""
    task = task_manager.add_task("Apprendre Flask")
    assert task.id != ""
    assert task.title == "Apprendre Flask"
    assert task.completed is False

    # Vérification de la relecture
    all_tasks = task_manager.get_all_tasks()
    assert len(all_tasks) == 1
    assert all_tasks[0].id == task.id
    assert all_tasks[0].title == "Apprendre Flask"


def test_task_manager_add_invalid_task(task_manager):
    """Vérifie que le gestionnaire refuse d'ajouter une tâche au titre invalide."""
    with pytest.raises(TaskValidationError):
        task_manager.add_task("   ")

    all_tasks = task_manager.get_all_tasks()
    assert len(all_tasks) == 0


def test_task_manager_mark_completed_and_reload(temp_storage_path):
    """
    Vérifie le passage d'une tâche à l'état terminée et sa relecture fidèle
    depuis une nouvelle instance de TaskManager (simulation de redémarrage).
    """
    manager1 = TaskManager(storage_path=temp_storage_path)
    task = manager1.add_task("Sortir le chien")
    assert task.completed is False

    # Marquer comme complétée
    updated = manager1.mark_completed(task.id)
    assert updated is not None
    assert updated.completed is True

    # Simulation d'un redémarrage complet de l'application
    manager2 = TaskManager(storage_path=temp_storage_path)
    reloaded_tasks = manager2.get_all_tasks()
    assert len(reloaded_tasks) == 1
    assert reloaded_tasks[0].id == task.id
    assert reloaded_tasks[0].title == "Sortir le chien"
    assert reloaded_tasks[0].completed is True


def test_task_manager_mark_completed_nonexistent(task_manager):
    """Vérifie que marquer un ID inconnu retourne None sans lever d'erreur."""
    result = task_manager.mark_completed("inconnu-123")
    assert result is None


def test_task_manager_get_all_ordered(temp_storage_path):
    """Vérifie que les tâches sont restituées dans l'ordre chronologique de création."""
    manager = TaskManager(storage_path=temp_storage_path)
    # Création directe de tâches avec horodatages explicites
    t1 = Task(id="1", title="Première tâche", created_at="2026-10-22T08:00:00")
    t2 = Task(id="2", title="Deuxième tâche", created_at="2026-10-22T08:15:00")
    t3 = Task(id="3", title="Troisième tâche", created_at="2026-10-22T08:30:00")
    
    # Enregistrement dans un ordre mélangé
    manager._write_tasks([t2, t3, t1])

    ordered = manager.get_all_tasks()
    assert [t.id for t in ordered] == ["1", "2", "3"]
