# 3. Accorder les permissions au compte de service
resource "google_project_iam_member" "artifact_writer" {
  project = data.google_project.project.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${google_service_account.github_actions.email}"
}

resource "google_project_iam_member" "run_admin" {
  project = data.google_project.project.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${google_service_account.github_actions.email}"
}

resource "google_project_iam_member" "sa_user" {
  project = data.google_project.project.project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${google_service_account.github_actions.email}"
}

resource "google_service_account_iam_member" "github_impersonation" {
  service_account_id = google_service_account.github_actions.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github_pool.name}/attribute.repository/${var.github_repo}"
}

# 5. Accès public pour Cloud Run (C'est ici que l'erreur est corrigée)
resource "google_cloud_run_v2_service_iam_member" "public_access" {
  project  = data.google_project.project.project_id
  location = google_cloud_run_v2_service.app.location
  name     = google_cloud_run_v2_service.app.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}