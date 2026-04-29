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
  name     = "recipe-app"
  location = var.region
  template {
    spec {
      service_account_name = google_service_account.service_account.email
      containers {
        image = var.image_path
      }
    }
  }
  traffic {
    percent         = 100
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


# Service Account
resource "google_service_account" "service_account" {
  account_id   = "recipe-app-sa"
  display_name = "Recipe App"
}

resource "google_project_iam_member" "firestore_access" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.service_account.email}"
}

resource "google_project_iam_member" "secret_access" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.service_account.email}"
}

resource "google_secret_manager_secret" "flask-secret-key" {
  secret_id = "flask-secret-key"

  replication {
    auto {}
  }
}
