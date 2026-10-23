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


# ==============================================================================
# Tests pour Feature 002 : Suivi de la Progression Quotidienne
# ==============================================================================

def test_get_index_progress_bar_and_counter(client, task_manager):
    """Vérifie la présence et la conformité du compteur et de la barre de progression (T006)."""
    t1 = task_manager.add_task("Mission Une")
    task_manager.add_task("Mission Deux")
    task_manager.add_task("Mission Trois")
    task_manager.add_task("Mission Quatre")

    # Marquer 1 tâche sur 4 comme terminée
    task_manager.mark_completed(t1.id)

    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)

    # Vérification du compteur textuel (1 sur 4 terminée(s), 25%)
    assert "1 sur 4" in html
    assert "25%" in html

    # Vérification des attributs d'accessibilité ARIA de la barre de progression
    assert 'role="progressbar"' in html
    assert 'aria-valuenow="25"' in html
    assert 'aria-valuemin="0"' in html
    assert 'aria-valuemax="100"' in html

    # Vérification de la largeur stylisée en ligne
    assert "width: 25%" in html


def test_get_index_celebration_banner_when_all_completed(client, task_manager):
    """Vérifie l'apparition de la bannière festive à 100% et sa disparition lors d'un ajout (T011)."""
    t1 = task_manager.add_task("Première étape")
    t2 = task_manager.add_task("Deuxième étape")

    task_manager.mark_completed(t1.id)
    task_manager.mark_completed(t2.id)

    # Requête GET à 100% de complétion
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)

    # Présence de la bannière de célébration et de l'illustration festive
    assert "celebration-card" in html
    assert "dog-cheer.svg" in html
    assert "Bravo ! Toutes les missions du jour sont terminées" in html
    assert "width: 100%" in html
    assert "2 sur 2" in html

    # Ajout d'une 3ème tâche non terminée via POST /tasks
    client.post("/tasks", data={"title": "Nouvelle tâche imprévue"})

    # La célébration doit disparaître
    response_after = client.get("/")
    html_after = response_after.get_data(as_text=True)
    assert "celebration-card" not in html_after
    assert "dog-cheer.svg" not in html_after
    assert "2 sur 3" in html_after
    assert "width: 67%" in html_after


def test_get_index_empty_state_no_progress_or_celebration(client):
    """Vérifie l'absence de section de progression et de félicitations sur liste vide (T015)."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)

    # La barre de progression et la célébration ne doivent PAS s'afficher
    assert "progress-section" not in html
    assert "celebration-card" not in html
    assert 'role="progressbar"' not in html

    # L'état vide d'accueil bienveillant doit être présent
    assert "dog-resting.svg" in html
    assert "Aucune tâche pour l'instant" in html


def test_quickstart_e2e_complete_flow(client, task_manager):
    """
    Déroule l'intégralité des 6 scénarios du guide quickstart.md :
    1. État initial (0 tâche) : pas de barre, pas de célébration.
    2. Ajout de 3 tâches : barre à 0%, compteur 0 sur 3.
    3. Complétion de 1 tâche (33%), puis 2ème (67%).
    4. Complétion 3ème tâche (100%) : bannière festive active.
    5. Ajout d'une 4ème tâche : 75%, disparition de la bannière.
    """
    # 1. État initial
    r1 = client.get("/")
    assert "progress-section" not in r1.get_data(as_text=True)
    assert "celebration-card" not in r1.get_data(as_text=True)

    # 2. Ajout de 3 tâches
    client.post("/tasks", data={"title": "Tâche Alpha"}, follow_redirects=True)
    client.post("/tasks", data={"title": "Tâche Bêta"}, follow_redirects=True)
    client.post("/tasks", data={"title": "Tâche Gamma"}, follow_redirects=True)

    r2 = client.get("/")
    html2 = r2.get_data(as_text=True)
    assert "0 sur 3" in html2
    assert "0%" in html2
    assert "celebration-card" not in html2

    # Récupération des tâches via la fixture task_manager
    tasks = task_manager.get_all_tasks()
    assert len(tasks) == 3

    # 3. Complétion 1ère tâche (33%)
    client.post(f"/tasks/{tasks[0].id}/complete", follow_redirects=True)
    r3 = client.get("/")
    html3 = r3.get_data(as_text=True)
    assert "1 sur 3" in html3
    assert "33%" in html3
    assert "celebration-card" not in html3

    # Complétion 2ème tâche (67%)
    client.post(f"/tasks/{tasks[1].id}/complete", follow_redirects=True)
    r4 = client.get("/")
    html4 = r4.get_data(as_text=True)
    assert "2 sur 3" in html4
    assert "67%" in html4
    assert "celebration-card" not in html4

    # 4. Complétion 3ème tâche (100%)
    client.post(f"/tasks/{tasks[2].id}/complete", follow_redirects=True)
    r5 = client.get("/")
    html5 = r5.get_data(as_text=True)
    assert "3 sur 3" in html5
    assert "100%" in html5
    assert "celebration-card" in html5
    assert "dog-cheer.svg" in html5

    # 5. Ajout d'une 4ème tâche (75%)
    client.post("/tasks", data={"title": "Tâche Delta"}, follow_redirects=True)
    r6 = client.get("/")
    html6 = r6.get_data(as_text=True)
    assert "3 sur 4" in html6
    assert "75%" in html6
    assert "celebration-card" not in html6
    assert "dog-cheer.svg" not in html6




