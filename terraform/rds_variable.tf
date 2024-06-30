variable "postgres_account_password" {
  description = "The password for the account database"
  type        = string  
}

variable "postgres_account_username" {
  description = "The username for the account database"
  type        = string  
}

variable "postgres_product_password" {
  description = "The password for the product database"
  type        = string  
}

variable "postgres_product_username" {
  description = "The username for the product database"
  type        = string  
}

variable "postgres_purchase_password" {
  description = "The password for the purchase database"
  type        = string  
}

variable "postgres_purchase_username" {
  description = "The username for the purchase database"
  type        = string  
}

variable "postgres_cart_password" {
  description = "The password for the cart database"
  type        = string  
}

variable "postgres_cart_username" {
  description = "The username for the cart database"
  type        = string  
}

variable "db_availability_zone" {
  description = "The availability zone for the database"
  type        = string  
}

variable "enable_multi_az" {
  description = "Enable multi-az for the database"
  type        = bool
  default     = false
}

