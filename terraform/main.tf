# PROVIDER
provider "google" {
  project = var.project_id
  region  = var.region
}

# Artifact Registry 
resource "google_artifact_registry_repository" "gcp-recipes" {
location      = var.region
  repository_id = "recipe-app"
  description   = "recipes app docker repository"
  format        = "DOCKER"
}


# Cloud Run
resource "google_cloud_run_service" "gcp-recipes" { 
name = "recipe-app" 
location = var.region 
template {
 spec{ 
containers { 
image = var.image_path
 } 
} 
}
 traffic { 
percent = 100 
latest_revision = true 
} 
}

# for unauthenticated access
resource "google_cloud_run_service_iam_member" "public_access" {
  service  = google_cloud_run_service.gcp-recipes.name
  location = var.region
  role     = "roles/run.invoker"
  member   = "allUsers"
}