"""
Module models.py - Gestion des données et persistance locale des tâches.

Ce module définit l'entité Task (représentant une tâche quotidienne)
et la classe TaskManager qui assure la persistance dans un fichier JSON local.
Conformément aux principes pédagogiques du projet, le code utilise
exclusivement la bibliothèque standard de Python (json, uuid, datetime, pathlib).
"""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import uuid


class TaskValidationError(ValueError):
    """Exception levée lorsqu'une validation de tâche échoue."""
    pass


@dataclass
class Task:
    """
    Représente une tâche du jour planifiée par l'utilisateur.

    Attributs :
        id : Identifiant unique immuable sous forme de chaîne de caractères.
        title : Intitulé descriptif de l'activité (1 à 200 caractères non vides).
        completed : Booléen indiquant si la tâche est terminée (défaut : False).
        created_at : Date et heure de création au format ISO 8601 (UTC).
    """
    id: str
    title: str
    completed: bool = False
    created_at: str = ""

    def __post_init__(self) -> None:
        """Valide et initialise les attributs après instanciation."""
        # 1. Validation de l'intitulé : "DOIT PAS être vide après suppression des espaces"
        if not isinstance(self.title, str):
            raise TaskValidationError("L'intitulé de la tâche doit être une chaîne de caractères.")
        
        cleaned_title = self.title.strip()
        if not cleaned_title:
            raise TaskValidationError("L'intitulé de la tâche ne doit pas être vide.")

        # 2. Validation de la longueur : "longueur DOIT être comprise entre 1 et 200 caractères"
        if len(cleaned_title) > 200:
            raise TaskValidationError("L'intitulé de la tâche ne doit pas dépasser 200 caractères.")
        
        self.title = cleaned_title

        # 3. Validation de l'identifiant
        if not self.id:
            self.id = uuid.uuid4().hex[:8]

        # 4. Validation du statut : booléen strict
        if not isinstance(self.completed, bool):
            raise TaskValidationError("Le statut d'achèvement doit être un booléen.")

        # 5. Horodatage ISO 8601
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'objet Task en dictionnaire sérialisable en JSON."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """Instancie un objet Task à partir d'un dictionnaire."""
        return cls(
            id=str(data.get("id", "")),
            title=str(data.get("title", "")),
            completed=bool(data.get("completed", False)),
            created_at=str(data.get("created_at", "")),
        )


class TaskManager:
    """
    Gestionnaire de persistance des tâches dans un fichier JSON local.
    
    Gère la création automatique du fichier, la lecture ordonnée,
    l'ajout et la complétion des tâches.
    """

    def __init__(self, storage_path: str = "data/tasks.json") -> None:
        """
        Initialise le gestionnaire avec le chemin du fichier JSON.

        Args:
            storage_path: Chemin relatif ou absolu vers le fichier de persistance.
        """
        self.storage_path = Path(storage_path)
        self._ensure_storage_exists()

    def _ensure_storage_exists(self) -> None:
        """
        Vérifie l'existence du fichier et du dossier parent.
        Si absent, crée le dossier et initialise le fichier avec un tableau vide [].
        """
        if not self.storage_path.parent.exists():
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.storage_path.exists():
            self._write_tasks([])

    def _read_tasks(self) -> List[Task]:
        """Lit et désérialise la liste des tâches depuis le fichier JSON."""
        self._ensure_storage_exists()
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                if not isinstance(raw_data, list):
                    return []
                return [Task.from_dict(item) for item in raw_data if isinstance(item, dict)]
        except (json.JSONDecodeError, OSError):
            return []

    def _write_tasks(self, tasks: List[Task]) -> None:
        """Sérialise et sauvegarde la liste des tâches dans le fichier JSON avec indentation."""
        data_to_write = [task.to_dict() for task in tasks]
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data_to_write, f, indent=2, ensure_ascii=False)

    def get_all_tasks(self) -> List[Task]:
        """
        Récupère l'ensemble des tâches ordonnées chronologiquement par date de création.
        
        Returns:
            Liste des tâches triées par created_at.
        """
        tasks = self._read_tasks()
        return sorted(tasks, key=lambda t: t.created_at)

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Recherche une tâche par son identifiant unique."""
        tasks = self._read_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None

    def add_task(self, title: str) -> Task:
        """
        Valide et enregistre une nouvelle tâche dans le fichier de persistance.

        Args:
            title: Intitulé de la tâche à ajouter.

        Returns:
            L'objet Task créé.

        Raises:
            TaskValidationError: Si le titre est vide ou dépasse 200 caractères.
        """
        new_task = Task(id=uuid.uuid4().hex[:8], title=title)
        tasks = self._read_tasks()
        tasks.append(new_task)
        self._write_tasks(tasks)
        return new_task

    def mark_completed(self, task_id: str) -> Optional[Task]:
        """
        Marque une tâche comme terminée (completed = True) et enregistre la modification.

        Args:
            task_id: Identifiant de la tâche à marquer comme complétée.

        Returns:
            L'objet Task mis à jour, ou None si la tâche n'a pas été trouvée.
        """
        tasks = self._read_tasks()
        updated_task: Optional[Task] = None
        for task in tasks:
            if task.id == task_id:
                task.completed = True
                updated_task = task
                break

        if updated_task is not None:
            self._write_tasks(tasks)

        return updated_task
