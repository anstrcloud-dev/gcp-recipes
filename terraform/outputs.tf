output "cloud_run_url" {
  description = "Recipe app URL"
  value       = google_cloud_run_service.gcp-recipes.status[0].url
}