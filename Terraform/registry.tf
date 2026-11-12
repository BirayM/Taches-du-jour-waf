# 1. Registre Docker
resource "google_artifact_registry_repository" "repo" {
  repository_id = "taches-du-jour-repo"
  format        = "DOCKER"
  location      = var.region
}