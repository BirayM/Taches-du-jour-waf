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
# Tests pour Feature 004 : Suppression de Tâche Individuelle (User Story 1)
# ==============================================================================

def test_post_delete_task_success_prg(client, task_manager):
    """
    Vérifie la suppression d'une tâche via POST /tasks/<task_id>/delete avec redirection 302
    selon le patron PRG, retrait du HTML et actualisation du ratio (T006 / US1).
    """
    t1 = task_manager.add_task("Tâche conservée terminée")
    t2 = task_manager.add_task("Tâche à supprimer")
    t3 = task_manager.add_task("Tâche conservée en cours")

    task_manager.mark_completed(t1.id)

    # Avant suppression : 1 sur 3 (33%)
    r_before = client.get("/")
    assert "1 sur 3" in r_before.get_data(as_text=True)
    assert "Tâche à supprimer" in r_before.get_data(as_text=True)

    # Exécution de la suppression par POST (PRG sans suivi immédiat)
    response = client.post(f"/tasks/{t2.id}/delete", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] in ["/", "http://localhost/"]

    # Vérification dans la couche modèle
    assert task_manager.get_task_by_id(t2.id) is None
    assert len(task_manager.get_all_tasks()) == 2

    # Vérification après redirection sur GET /
    r_after = client.get("/")
    assert r_after.status_code == 200
    html_after = r_after.get_data(as_text=True)
    assert "Tâche à supprimer" not in html_after
    assert "Tâche conservée terminée" in html_after
    assert "Tâche conservée en cours" in html_after
    assert "1 sur 2" in html_after
    assert "50%" in html_after
    assert 'aria-valuenow="50"' in html_after


def test_post_delete_task_unknown_id_redirects_gracefully(client):
    """
    Vérifie qu'une tentative de suppression avec un identifiant inexistant
    redirige en 302 sans erreur 500 ni crash (T006 / US1 / FR-007).
    """
    response = client.post("/tasks/unknown-task-id-404/delete", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] in ["/", "http://localhost/"]


def test_get_delete_task_method_not_allowed(client, task_manager):
    """
    Vérifie que la méthode GET sur /tasks/<task_id>/delete est strictement
    rejetée avec une erreur 405 Method Not Allowed (T006 / US1 / web-routes.md).
    """
    task = task_manager.add_task("Tâche protégée")
    response = client.get(f"/tasks/{task.id}/delete")
    assert response.status_code == 405
    # La tâche ne doit pas avoir été supprimée
    assert task_manager.get_task_by_id(task.id) is not None


def test_post_delete_task_triggers_celebration_at_100_percent(client, task_manager):
    """
    Vérifie que supprimer une tâche non terminée, laissant uniquement des tâches
    terminées (ex: 1/2 -> 1/1 à 100%), active la célébration festive et dog-cheer.svg (T007 / US1).
    """
    t1 = task_manager.add_task("Mission Réussie")
    t2 = task_manager.add_task("Mission Abandonnée")

    task_manager.mark_completed(t1.id)

    # 1/2 terminée (50%) -> pas de célébration
    r1 = client.get("/")
    assert "celebration-card" not in r1.get_data(as_text=True)

    # Suppression de la tâche non terminée
    response = client.post(f"/tasks/{t2.id}/delete", follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)

    # Recalcul à 1 sur 1 (100%) et apparition de la célébration
    assert "1 sur 1" in html
    assert "100%" in html
    assert "celebration-card" in html
    assert "dog-cheer.svg" in html
    assert "Bravo ! Toutes les missions du jour sont terminées" in html


# ==============================================================================
# Tests pour Feature 004 : Suppression de Tâche Individuelle (User Story 2)
# ==============================================================================

def test_post_delete_last_task_returns_to_empty_state(client, task_manager):
    """
    Vérifie qu'après suppression de l'unique tâche restante, l'application réaffiche
    l'état d'accueil initial sans barre de progression ni célébration (T012 / US2).
    """
    import html as html_lib
    from app.quotes import WELCOME_QUOTE

    task = task_manager.add_task("Dernière tâche active")

    # Vérification que la liste et la progression sont actives avant suppression
    r_before = client.get("/")
    assert "progress-section" in r_before.get_data(as_text=True)

    # Suppression de la dernière tâche
    response = client.post(f"/tasks/{task.id}/delete", follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)

    # Vérifications de l'état vide d'accueil
    assert "dog-resting.svg" in html
    assert "Aucune tâche pour l'instant !" in html
    assert WELCOME_QUOTE["text"] in html_lib.unescape(html)
    assert WELCOME_QUOTE["author"] in html
    assert "progress-section" not in html
    assert "celebration-card" not in html
    assert 'role="progressbar"' not in html
    assert "Mes activités (0)" in html


# ==============================================================================
# Tests pour Feature 004 : Suppression de Tâche Individuelle (User Story 3)
# ==============================================================================

def test_delete_button_accessibility_attributes(client, task_manager):
    """
    Vérifie la conformité WAI-ARIA du bouton de suppression :
    aria-label descriptif, title explicite et masquage de l'émoji aux lecteurs d'écran (T014 / US3).
    """
    task = task_manager.add_task("Brosser le pelage de Rocky")

    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)

    # Vérification des attributs d'accessibilité requis
    assert f'aria-label="Supprimer la tâche : {task.title}"' in html
    assert f'title="Supprimer la tâche : {task.title}"' in html
    assert '<span class="delete-icon" aria-hidden="true">🗑️</span>' in html


def test_delete_button_active_on_completed_task(client, task_manager):
    """
    Vérifie que le bouton de suppression reste actif sans attribut disabled
    sur une tâche complétée, et permet sa suppression avec recalcul exact (T015 / US3).
    """
    t1 = task_manager.add_task("Tâche complétée à supprimer")
    t2 = task_manager.add_task("Tâche en cours")

    task_manager.mark_completed(t1.id)

    # Récupération de la page d'accueil
    response = client.get("/")
    html = response.get_data(as_text=True)

    # La case à cocher est désactivée car complétée, mais le bouton de suppression DOIT rester actif
    assert "is-completed" in html
    assert f"/tasks/{t1.id}/delete" in html

    # Vérification qu'aucun attribut disabled n'est présent sur le bouton de suppression
    # On isole la balise ouvrante <button ...> du formulaire de suppression de t1
    delete_form_start = html.find(f'action="/tasks/{t1.id}/delete"')
    assert delete_form_start != -1
    delete_form_end = html.find('</form>', delete_form_start)
    delete_form_html = html[delete_form_start:delete_form_end]
    button_start = delete_form_html.find("<button")
    button_end = delete_form_html.find(">", button_start)
    button_tag = delete_form_html[button_start:button_end]
    assert "disabled" not in button_tag
    assert 'class="btn-delete"' in button_tag

    # Suppression de la tâche complétée
    del_response = client.post(f"/tasks/{t1.id}/delete", follow_redirects=True)
    assert del_response.status_code == 200
    del_html = del_response.get_data(as_text=True)

    # Ratio mis à jour : 0 sur 1 (0%)
    assert "0 sur 1" in del_html
    assert "0%" in del_html
    assert "Tâche complétée à supprimer" not in del_html
    assert "Tâche en cours" in del_html


def test_quickstart_004_delete_task_all_scenarios(client, task_manager):
    """
    Validation de bout en bout des 6 scénarios du guide quickstart.md (T020) :
    1. Suppression d'une tâche parmi plusieurs et recalcul de progression.
    2. Suppression de la dernière tâche et retour à l'état vide.
    3. Suppression menant à 100% d'achèvement (Célébration festive).
    4. Suppression d'une tâche déjà complétée.
    5. Résilience, patron PRG et rafraîchissement navigateur.
    6. Accessibilité au clavier et lecteur d'écran (aria-label).
    """
    import html as html_lib
    from app.quotes import WELCOME_QUOTE

    # --- Scénario 1 : Suppression d'une tâche parmi plusieurs et recalcul ---
    t1 = task_manager.add_task("Tâche 1")
    t2 = task_manager.add_task("Tâche 2")
    t3 = task_manager.add_task("Tâche 3")
    task_manager.mark_completed(t1.id)

    r_sc1_init = client.get("/")
    assert "1 sur 3" in r_sc1_init.get_data(as_text=True)

    # Suppression de Tâche 2
    r_sc1_del = client.post(f"/tasks/{t2.id}/delete", follow_redirects=True)
    html_sc1 = r_sc1_del.get_data(as_text=True)
    assert "Tâche 2" not in html_sc1
    assert "Tâche 1" in html_sc1
    assert "Tâche 3" in html_sc1
    assert "1 sur 2" in html_sc1
    assert "50%" in html_sc1

    # --- Scénario 2 : Suppression de la dernière tâche et retour à l'état vide ---
    # On supprime Tâche 1 puis Tâche 3
    client.post(f"/tasks/{t1.id}/delete", follow_redirects=True)
    r_sc2 = client.post(f"/tasks/{t3.id}/delete", follow_redirects=True)
    html_sc2 = r_sc2.get_data(as_text=True)
    assert "dog-resting.svg" in html_sc2
    assert "Aucune tâche pour l'instant !" in html_sc2
    assert WELCOME_QUOTE["text"] in html_lib.unescape(html_sc2)
    assert "progress-section" not in html_sc2

    # --- Scénario 3 : Suppression menant à 100% d'achèvement (Célébration festive) ---
    t_rap = task_manager.add_task("Rédiger le rapport")
    t_cour = task_manager.add_task("Envoyer le courriel")
    task_manager.mark_completed(t_rap.id)

    r_sc3_init = client.get("/")
    assert "celebration-card" not in r_sc3_init.get_data(as_text=True)

    # Suppression de la tâche non complétée -> 1/1 = 100%
    r_sc3_del = client.post(f"/tasks/{t_cour.id}/delete", follow_redirects=True)
    html_sc3 = r_sc3_del.get_data(as_text=True)
    assert "1 sur 1" in html_sc3
    assert "100%" in html_sc3
    assert "celebration-card" in html_sc3
    assert "dog-cheer.svg" in html_sc3

    # --- Scénario 4 : Suppression d'une tâche déjà complétée ---
    # t_rap est complétée, on vérifie que le bouton de suppression est présent et fonctionnel
    btn_rap_idx = html_sc3.find(f'action="/tasks/{t_rap.id}/delete"')
    assert btn_rap_idx != -1
    r_sc4 = client.post(f"/tasks/{t_rap.id}/delete", follow_redirects=True)
    html_sc4 = r_sc4.get_data(as_text=True)
    assert "Rédiger le rapport" not in html_sc4
    assert "progress-section" not in html_sc4

    # --- Scénario 5 : Résilience, patron PRG et rafraîchissement navigateur ---
    t_prg = task_manager.add_task("Tâche PRG")
    # POST sans redirection automatique -> doit renvoyer 302 vers /
    r_post = client.post(f"/tasks/{t_prg.id}/delete", follow_redirects=False)
    assert r_post.status_code == 302
    assert r_post.headers["Location"] in ["/", "http://localhost/"]
    # Rechargement ultérieur (F5) -> simple GET /
    r_f5 = client.get("/")
    assert r_f5.status_code == 200
    assert "Tâche PRG" not in r_f5.get_data(as_text=True)

    # --- Scénario 6 : Accessibilité au clavier et lecteur d'écran ---
    t_aria = task_manager.add_task("Vérifier accessibilité")
    r_sc6 = client.get("/")
    html_sc6 = r_sc6.get_data(as_text=True)
    assert f'aria-label="Supprimer la tâche : {t_aria.title}"' in html_sc6
    assert f'title="Supprimer la tâche : {t_aria.title}"' in html_sc6
    assert '<span class="delete-icon" aria-hidden="true">🗑️</span>' in html_sc6


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




