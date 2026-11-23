"""
Module models.py - Gestion des données et persistance locale des tâches.

Ce module définit :
- L'entité Task (représentant une tâche quotidienne planifiée).
- L'entité ProgressStats (statistiques consolidées de complétion et célébration).
- La classe TaskManager qui assure la persistance dans un fichier JSON local (data/tasks.json).
- L'entité CheckedDate (représentant une date cochée dans le calendrier).
- Les structures CalendarDay et CalendarMonthInfo (calcul matriciel de la grille calendaire).
- La classe CalendarManager qui assure la persistance dédiée dans un fichier JSON local (data/calendar.json).

Conformément aux principes pédagogiques du projet, le code utilise
exclusivement la bibliothèque standard de Python (calendar, dataclasses, json, uuid, datetime, pathlib).
"""

import calendar
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import uuid


class TaskValidationError(ValueError):
    """Exception levée lorsqu'une validation de tâche échoue."""
    pass


class CalendarValidationError(ValueError):
    """Exception levée lorsqu'une validation liée au calendrier échoue."""
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


@dataclass
class ProgressStats:
    """
    Statistiques de progression quotidienne calculées à partir des tâches du jour.

    Attributs :
        total : Nombre total de tâches planifiées pour la journée (total >= 0).
        completed : Nombre de tâches ayant le statut completed == True (0 <= completed <= total).
        percentage : Pourcentage de complétion arrondi à l'entier le plus proche (entre 0 et 100).
        is_all_completed : Booléen strictement évalué à total > 0 and completed == total.
    """
    total: int = 0
    completed: int = 0
    percentage: int = 0
    is_all_completed: bool = False

    def __post_init__(self) -> None:
        """Valide et garantit la cohérence des indicateurs arithmétiques."""
        if not isinstance(self.total, int) or self.total < 0:
            raise TaskValidationError("Le total des tâches doit être un entier positif ou nul.")

        if not isinstance(self.completed, int) or self.completed < 0:
            raise TaskValidationError("Le nombre de tâches complétées doit être un entier positif ou nul.")

        if self.completed > self.total:
            raise TaskValidationError("Le nombre de tâches complétées ne peut pas dépasser le total.")

        # Calcul automatique ou forçage des règles métier garanties
        if self.total == 0:
            self.percentage = 0
            self.is_all_completed = False
        else:
            self.percentage = round((self.completed / self.total) * 100)
            self.is_all_completed = (self.completed == self.total)


class TaskManager:
    """
    Gestionnaire de persistance des tâches dans un fichier JSON local.
    
    Gère la création automatique du fichier, la lecture ordonnée,
    l'ajout, la complétion et la suppression des tâches.
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

    def delete_task(self, task_id: str) -> bool:
        """
        Supprime définitivement une tâche du fichier de persistance via son identifiant unique.

        Règles métier & Cycle de vie :
        - Destruction physique directe : retrait sans corbeille ni archivage intermédiaire.
        - Persistance synchrone : réécriture immédiate de data/tasks.json avec indentation.
        - Idempotence & Résilience : si task_id est introuvable, vide ou déjà supprimé,
          aucun accès en écriture n'est effectué et la méthode retourne False sans exception.

        Args:
            task_id: Identifiant unique de la tâche à supprimer.

        Returns:
            bool: True si la tâche a été trouvée et supprimée, False si elle n'existait pas.
        """
        tasks = self._read_tasks()
        initial_count = len(tasks)
        tasks = [task for task in tasks if task.id != task_id]

        # Si le nombre d'éléments a diminué, la tâche ciblée a bien été trouvée
        if len(tasks) < initial_count:
            self._write_tasks(tasks)
            return True

        # Aucun accès en écriture n'est effectué si l'identifiant n'existait pas
        return False

    def get_progress(self) -> ProgressStats:
        """
        Calcule les statistiques consolidées d'avancement des tâches du jour.

        Returns:
            Une instance de ProgressStats contenant total, completed, percentage et is_all_completed.
        """
        tasks = self.get_all_tasks()
        total = len(tasks)
        completed = sum(1 for t in tasks if t.completed)
        return ProgressStats(total=total, completed=completed)


# ==============================================================================
# Modèles et structures de données pour le Calendrier (specs/006-calendar-date-picker)
# ==============================================================================

FRENCH_MONTH_NAMES: Dict[int, str] = {
    1: "Janvier",
    2: "Février",
    3: "Mars",
    4: "Avril",
    5: "Mai",
    6: "Juin",
    7: "Juillet",
    8: "Août",
    9: "Septembre",
    10: "Octobre",
    11: "Novembre",
    12: "Décembre",
}


@dataclass
class CheckedDate:
    """
    Représente une date marquée comme cochée dans le calendrier.

    Attributs :
        date_string : Date au format ISO 8601 standard YYYY-MM-DD.
        checked : Booléen indiquant si la date est activement cochée (défaut : True).
        updated_at : Horodatage ISO 8601 UTC de la dernière mise à jour.
    """
    date_string: str
    checked: bool = True
    updated_at: str = ""

    def __post_init__(self) -> None:
        """Valide rigoureusement le format ISO 8601 et les types."""
        # 1. Validation de date_string
        if not isinstance(self.date_string, str):
            raise CalendarValidationError("La date doit être une chaîne de caractères.")

        # Format strict YYYY-MM-DD (10 caractères)
        if len(self.date_string) != 10:
            raise CalendarValidationError(f"Format de date invalide : '{self.date_string}'. Attendu YYYY-MM-DD.")

        try:
            parsed_date = date.fromisoformat(self.date_string)
            if parsed_date.isoformat() != self.date_string:
                raise CalendarValidationError(f"Format de date non conforme : '{self.date_string}'.")
        except ValueError as exc:
            raise CalendarValidationError(f"Date invalide ou impossible : '{self.date_string}'.") from exc

        # 2. Validation de checked : booléen strict
        if not isinstance(self.checked, bool):
            raise CalendarValidationError("Le statut checked doit être un booléen.")

        # 3. Horodatage updated_at
        if not self.updated_at:
            self.updated_at = datetime.now(timezone.utc).isoformat()
        elif not isinstance(self.updated_at, str):
            raise CalendarValidationError("L'horodatage updated_at doit être une chaîne de caractères.")

    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'objet CheckedDate en dictionnaire sérialisable en JSON."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CheckedDate":
        """Instancie un objet CheckedDate à partir d'un dictionnaire."""
        return cls(
            date_string=str(data.get("date_string", "")),
            checked=bool(data.get("checked", True)),
            updated_at=str(data.get("updated_at", "")),
        )


@dataclass
class CalendarDay:
    """
    Représente un jour dans la matrice calendaire mensuelle.

    Attributs :
        day_number : Numéro du jour dans le mois (1 à 31, ou 0 pour une case d'alignement).
        date_string : Date au format ISO 8601 (YYYY-MM-DD), ou chaîne vide si case vide.
        is_today : Indique si la date correspond au jour actuel.
        is_checked : Indique si la date est marquée comme cochée.
    """
    day_number: int
    date_string: str = ""
    is_today: bool = False
    is_checked: bool = False


@dataclass
class CalendarMonthInfo:
    """
    Métadonnées et structure matricielle du mois visualisé.

    Attributs :
        year : Année calendaire (ex: 2026).
        month : Numéro du mois (1 à 12).
        month_name : Intitulé du mois en français (ex: 'Novembre').
        title : Titre composé du mois et de l'année (ex: 'Novembre 2026').
        total_days : Nombre total de jours dans le mois (28 à 31).
        weeks : Matrice hebdomadaire de semaines (7 jours par semaine).
        checked_count : Nombre de dates cochées dans ce mois (défaut : 0).
    """
    year: int
    month: int
    month_name: str
    title: str
    total_days: int
    weeks: List[List[CalendarDay]]
    checked_count: int = 0


def get_month_matrix(year: int, month: int) -> List[List[CalendarDay]]:
    """
    Génère la matrice hebdomadaire d'un mois (7 colonnes, du lundi au dimanche).

    Args:
        year: Année calendaire (ex: 2026).
        month: Numéro du mois (1 à 12).

    Returns:
        Une liste de semaines de 7 jours (CalendarDay).
    """
    cal = calendar.Calendar(firstweekday=0)  # Lundi = 0, Dimanche = 6
    weeks: List[List[CalendarDay]] = []
    for week in cal.monthdayscalendar(year, month):
        week_days: List[CalendarDay] = []
        for day_num in week:
            if day_num == 0:
                week_days.append(CalendarDay(day_number=0, date_string=""))
            else:
                date_str = f"{year:04d}-{month:02d}-{day_num:02d}"
                week_days.append(CalendarDay(day_number=day_num, date_string=date_str))
        weeks.append(week_days)
    return weeks


def get_calendar_month_info(
    year: int,
    month: int,
    checked_dates: Optional[Dict[str, CheckedDate]] = None,
    today_date_str: Optional[str] = None,
) -> CalendarMonthInfo:
    """
    Construit les métadonnées et la structure matricielle pour un mois donné.

    Args:
        year: Année calendaire.
        month: Numéro du mois (1 à 12).
        checked_dates: Dictionnaire optionnel des dates cochées pour enrichir les jours.
        today_date_str: Chaîne de date ISO optionnelle pour identifier le jour courant.

    Returns:
        Instance de CalendarMonthInfo.
    """
    if not isinstance(year, int) or not isinstance(month, int) or not (1 <= month <= 12):
        raise CalendarValidationError("L'année et le mois doivent être des entiers valides (mois entre 1 et 12).")

    _, total_days = calendar.monthrange(year, month)
    month_name = FRENCH_MONTH_NAMES.get(month, "")
    title = f"{month_name} {year}"
    weeks = get_month_matrix(year, month)

    if today_date_str is None:
        today_date_str = date.today().isoformat()

    checked_map = checked_dates or {}
    checked_count = 0

    for week in weeks:
        for day in week:
            if day.day_number > 0:
                day.is_today = (day.date_string == today_date_str)
                is_checked = day.date_string in checked_map and checked_map[day.date_string].checked
                day.is_checked = is_checked
                if is_checked:
                    checked_count += 1

    return CalendarMonthInfo(
        year=year,
        month=month,
        month_name=month_name,
        title=title,
        total_days=total_days,
        weeks=weeks,
        checked_count=checked_count,
    )


class CalendarManager:
    """
    Gestionnaire de persistance des dates cochées dans un fichier JSON local.

    Assure l'isolation complète des données du calendrier par rapport aux tâches
    (data/calendar.json vs data/tasks.json).
    """

    def __init__(self, storage_path: str = "data/calendar.json") -> None:
        """
        Initialise le gestionnaire avec le chemin du fichier JSON.

        Args:
            storage_path: Chemin relatif ou absolu vers le fichier de persistance du calendrier.
        """
        self.storage_path = Path(storage_path)
        self._ensure_storage_exists()

    def _ensure_storage_exists(self) -> None:
        """
        Vérifie l'existence du fichier et du dossier parent.
        Si absent, crée le dossier et initialise le fichier avec un dictionnaire vide {}.
        """
        if not self.storage_path.parent.exists():
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.storage_path.exists():
            self._write_dates({})

    def _read_dates(self) -> Dict[str, CheckedDate]:
        """Lit et désérialise le registre des dates depuis le fichier JSON."""
        self._ensure_storage_exists()
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                if isinstance(raw_data, dict):
                    result: Dict[str, CheckedDate] = {}
                    for k, v in raw_data.items():
                        if isinstance(v, dict):
                            result[k] = CheckedDate.from_dict(v)
                    return result
                elif isinstance(raw_data, list):
                    result = {}
                    for item in raw_data:
                        if isinstance(item, dict) and "date_string" in item:
                            cd = CheckedDate.from_dict(item)
                            result[cd.date_string] = cd
                    return result
                return {}
        except (json.JSONDecodeError, OSError, ValueError):
            return {}

    def _write_dates(self, dates: Dict[str, CheckedDate]) -> None:
        """Sérialise et sauvegarde le registre des dates dans le fichier JSON avec indentation."""
        data_to_write = {date_str: cd.to_dict() for date_str, cd in dates.items()}
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data_to_write, f, indent=2, ensure_ascii=False)

    def _save_date(self, checked_date: CheckedDate) -> None:
        """Enregistre ou met à jour une date cochée dans le fichier de persistance."""
        dates = self._read_dates()
        dates[checked_date.date_string] = checked_date
        self._write_dates(dates)

    def get_all_checked_dates(self) -> Dict[str, CheckedDate]:
        """
        Récupère l'ensemble des dates actuellement cochées.

        Returns:
            Dictionnaire associant la date ISO (YYYY-MM-DD) à son objet CheckedDate.
        """
        dates = self._read_dates()
        return {date_str: cd for date_str, cd in dates.items() if cd.checked}

    def is_date_checked(self, date_string: str) -> bool:
        """
        Indique si une date spécifique est activement cochée.

        Args:
            date_string: Chaîne de date au format ISO 8601 (YYYY-MM-DD).

        Returns:
            bool: True si la date est cochée, False sinon.
        """
        checked_dates = self.get_all_checked_dates()
        return date_string in checked_dates

    def toggle_date(self, date_string: str) -> CheckedDate:
        """
        Bascule l'état coché/décoché d'une date (action réversible).

        Args:
            date_string: Chaîne de date au format ISO 8601 (YYYY-MM-DD).

        Returns:
            L'objet CheckedDate mis à jour avec son nouvel état.

        Raises:
            CalendarValidationError: Si date_string ne respecte pas le format ISO 8601 strict.
        """
        # Valide la date via l'instanciation de CheckedDate
        CheckedDate(date_string=date_string)

        dates = self._read_dates()
        current = dates.get(date_string)
        new_status = not current.checked if current else True
        now_utc = datetime.now(timezone.utc).isoformat()

        updated = CheckedDate(date_string=date_string, checked=new_status, updated_at=now_utc)
        dates[date_string] = updated
        self._write_dates(dates)
        return updated

    def get_month_checked_count(self, year: int, month: int) -> int:
        """
        Calcule le nombre de dates activement cochées pour un mois et une année donnés.

        Args:
            year: Année calendaire.
            month: Numéro du mois (1 à 12).

        Returns:
            int: Nombre de dates cochées dans ce mois.
        """
        prefix = f"{year:04d}-{month:02d}-"
        checked_dates = self.get_all_checked_dates()
        return sum(1 for date_str in checked_dates if date_str.startswith(prefix))

