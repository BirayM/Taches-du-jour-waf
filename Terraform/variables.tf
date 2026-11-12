variable "project_id" {
  description = "L'ID de ton projet Google Cloud"
  type        = string
  default     = "be-ai-agent-705f"
}

variable "region" {
  description = "La région pour les ressources (utiliser une région, pas une zone)"
  type        = string
  default     = "europe-west1"
}

variable "github_repo" {
  description = "Le dépôt GitHub (format: USER/REPO)"
  type        = string
  default     = "BirayM/Taches-du-jour-waf"
}