resource "google_project_service" "required_apis" {
  for_each = toset([
    "iamcredentials.googleapis.com",
    "sts.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "iam.googleapis.com",
    "containeranalysis.googleapis.com",
    "artifactregistry.googleapis.com",
    "run.googleapis.com",
  ])
  project = var.project_id
  service = each.value

  disable_dependent_services = true
  disable_on_destroy         = false
}
