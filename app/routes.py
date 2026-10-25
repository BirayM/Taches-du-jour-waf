"""
Module routes.py - Définition des routes web HTTP pour Tâches du Jour.

Ce module gère les requêtes HTTP selon les principes du rendu côté serveur (SSR)
et du patron Post/Redirect/Get (PRG).

Routes disponibles :
- GET / : Affiche la page principale (formulaire, liste des tâches, citation).
- POST /tasks : Ajoute une nouvelle tâche et redirige vers / (PRG).
- POST /tasks/<task_id>/complete : Marque une tâche comme terminée et redirige vers /.
- POST /tasks/<task_id>/delete : Supprime définitivement une tâche et redirige vers / (PRG).
"""

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from app.models import TaskManager, TaskValidationError
from app.quotes import WELCOME_QUOTE, get_random_quote

bp = Blueprint("main", __name__)


def get_task_manager() -> TaskManager:
    """
    Instancie le gestionnaire de tâches configuré avec le fichier de persistance.
    Permet de basculer facilement sur un fichier de test temporaire lors des tests pytest.
    """
    storage_path = current_app.config.get("DATA_FILE", "data/tasks.json")
    return TaskManager(storage_path=storage_path)


@bp.route("/", methods=["GET"])
def index():
    """
    Affiche la page d'accueil de l'application.
    Injecte la liste ordonnée des tâches, la progression du jour et une citation canine adaptée.
    """
    manager = get_task_manager()
    tasks = manager.get_all_tasks()
    progress = manager.get_progress()

    # Si aucune tâche n'est encore enregistrée, afficher le message d'accueil initial
    if not tasks:
        quote = WELCOME_QUOTE
    else:
        quote = get_random_quote()

    return render_template("index.html", tasks=tasks, quote=quote, progress=progress)


@bp.route("/tasks", methods=["POST"])
def add_task():
    """
    Traite l'ajout d'une tâche via formulaire HTML standard.
    
    Patron Post/Redirect/Get :
    Après validation et persistance, effectue une redirection 302 vers '/'
    afin de réinitialiser le champ de saisie et de permettre un enchaînement
    fluide sans risquer un renvoi accidentel de données.
    """
    title = request.form.get("title", "")
    manager = get_task_manager()

    try:
        manager.add_task(title)
    except TaskValidationError as error:
        # Émission d'un message flash d'erreur affiché sur la page d'accueil
        flash(str(error), "error")

    return redirect(url_for("main.index"))


@bp.route("/tasks/<task_id>/complete", methods=["POST"])
def complete_task(task_id: str):
    """
    Marque la tâche spécifiée par son identifiant comme terminée.
    Effectue une redirection vers la page d'accueil.
    """
    manager = get_task_manager()
    manager.mark_completed(task_id)
    return redirect(url_for("main.index"))


@bp.route("/tasks/<task_id>/delete", methods=["POST"])
def delete_task(task_id: str):
    """
    Supprime définitivement la tâche spécifiée par son identifiant unique.

    Patron Post/Redirect/Get (PRG) & Idempotence :
    - Restreint strictement à la méthode POST (methods=["POST"]). Les requêtes GET
      sont automatiquement rejetées avec une erreur HTTP 405 Method Not Allowed.
    - Supprime la tâche de manière synchrone via TaskManager.delete_task().
    - Redirige en HTTP 302 vers 'main.index', que la tâche ait été trouvée ou non
      (résilience face aux identifiants inexistants et absence de crash 500).
    - Aucune notification flash superflue n'est émise.
    """
    manager = get_task_manager()
    manager.delete_task(task_id)
    return redirect(url_for("main.index"))

