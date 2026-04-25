variable "project_id" {
  description = "Project id"
  type        = string
  default     = "gcp-recipes"
}
variable "region" {
  description = "Gcp region"
  type        = string
  default     = "europe-west3"
}
variable "image_path" {
  description = "Image path"
  type        = string
  default     = "europe-west3-docker.pkg.dev/gcp-recipes/recipe-app/recipe-app:v1"
}


