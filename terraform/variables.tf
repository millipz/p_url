variable "project_name" {
  description = "Name of project"
  type = string
  default = "p_url"
}

variable "admin_email" {
  description = "Administrator email address for alerts"
  type = string
  sensitive = true
  default = ""
}