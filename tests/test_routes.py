"""
Tests d'intégration HTTP pour les routes de l'application (app/routes.py).

Couvre les exigences :
- Affichage de la page d'accueil (GET /) avec ou sans tâches.
- Patron Post/Redirect/Get (PRG) sur l'ajout de tâche (POST /tasks).
- Rejet des soumissions invalides (champs vides).
- Complétion d'une tâche (POST /tasks/<id>/complete) et redirection.
- Présence d'un message de motivation bienveillant et des illustrations.
- Échappement et sécurité du texte saisi.
"""

def test_get_index_empty_state(client):
    """Vérifie que la page d'accueil s'affiche correctement avec 0 tâche."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["Content-Type"]
    html = response.get_data(as_text=True)
    assert "<form" in html
    assert 'name="title"' in html
    assert "Aucune tâche pour l'instant" in html
    assert "Mes activités (0)" in html


def test_post_task_success_prg(client, task_manager):
    """
    Vérifie qu'une soumission valide enregistre la tâche et redirige (302)
    vers / pour réinitialiser le formulaire (patron PRG).
    """
    response = client.post("/tasks", data={"title": "Rédiger la leçon 1"}, follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] in ["/", "http://localhost/"]

    tasks = task_manager.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Rédiger la leçon 1"
    assert tasks[0].completed is False

    redirected = client.get("/")
    assert redirected.status_code == 200
    assert "Rédiger la leçon 1" in redirected.get_data(as_text=True)


def test_post_task_empty_fails(client, task_manager):
    """Vérifie qu'une soumission avec intitulé vide est rejetée et ne crée pas de tâche."""
    response = client.post("/tasks", data={"title": "   "}, follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "ne doit pas être vide" in html or "vide" in html

    assert len(task_manager.get_all_tasks()) == 0


def test_post_task_too_long_fails(client, task_manager):
    """Vérifie qu'une soumission dépassant 200 caractères est rejetée."""
    long_title = "Z" * 201
    response = client.post("/tasks", data={"title": long_title}, follow_redirects=True)
    assert response.status_code == 200

    assert len(task_manager.get_all_tasks()) == 0


def test_post_task_special_characters_escaped(client, task_manager):
    """Vérifie que les balises HTML et caractères spéciaux sont gérés sans injection."""
    script_title = "<b>Test</b> & <script>alert('woof')</script>"
    response = client.post("/tasks", data={"title": script_title}, follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)

    assert "<script>alert('woof')</script>" not in html or "&lt;script&gt;" in html
    tasks = task_manager.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == script_title


def test_get_index_with_tasks_and_random_quote(client, task_manager):
    """Vérifie l'affichage ordonné des tâches et de la citation motivante."""
    task_manager.add_task("Tâche Alpha")
    task_manager.add_task("Tâche Bêta")

    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)

    assert "Mes activités (2)" in html
    assert "Tâche Alpha" in html
    assert "Tâche Bêta" in html
    # Vérification de la présence de la carte de citation
    assert "quote-card" in html
    assert "«" in html and "»" in html


def test_post_complete_task_success(client, task_manager):
    """Vérifie le marquage d'une tâche comme terminée avec redirection 302."""
    task = task_manager.add_task("Préparer la gamelle")
    assert task.completed is False

    response = client.post(f"/tasks/{task.id}/complete", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] in ["/", "http://localhost/"]

    # Vérification que la tâche est maintenant terminée
    updated = task_manager.get_task_by_id(task.id)
    assert updated is not None
    assert updated.completed is True

    # Vérification dans le HTML rendu
    redirected = client.get("/")
    html = redirected.get_data(as_text=True)
    assert "is-completed" in html
    assert "Terminée" in html


def test_post_complete_task_unknown_id_redirects_gracefully(client):
    """Vérifie que tenter de compléter un ID inexistant ne provoque pas de crash 500."""
    response = client.post("/tasks/non-existent-id/complete", follow_redirects=False)
    assert response.status_code == 302
