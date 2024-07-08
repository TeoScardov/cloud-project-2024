variable "postgres_password" {
  description = "The password for the account database"
  type        = string  
}

variable "postgres_username" {
  description = "The username for the account database"
  type        = string  
}

variable "postgres_db_name" {
  description = "The name of the database"
  type        = string  
}
variable "db_availability_zone" {
  description = "The availability zone for the database"
  type        = list(string)
}

variable "enable_multi_az" {
  description = "Enable multi-az for the database"
  type        = bool
  default     = false
}

