variable "jwt_secret_key" {
  description = "The secret key for the JWT token"
}

variable "payment_prefix" {
  description = "The prefix for the payment service"
}

##################
## web Variable ##
##################

variable "web_cpu" {
  description = "The amount of CPU to reserve for the container"
  type        = number
  default     = 1024
}

variable "web_memory" {
  description = "The amount of memory (in MiB) to reserve for the container"
  type        = number
  default     = 3072
}

variable "web_containerPort" {
  description = "The port on the container to associate with the load balancer"
  type        = number
  default     = 80
}

variable "web_hostPort" {
  description = "The port on the host to associate with the load balancer"
  type        = number
  default     = 80
}

variable "env_number_of_books_to_display" {
  description = "The number of books to display in the web application"
  type        = string
  default     = "10"
}

######################
## account Variable ##
######################

variable "account_cpu" {
  description = "The amount of CPU to reserve for the container"
  type        = number
  default     = 1024
}

variable "account_memory" {
  description = "The amount of memory (in MiB) to reserve for the container"
  type        = number
  default     = 3072
}

variable "account_containerPort" {
  description = "The port on the container to associate with the load balancer"
  type        = number
  default     = 4001
}

variable "account_hostPort" {
  description = "The port on the host to associate with the load balancer"
  type        = number
  default     = 4001
}

######################
## product Variable ##
######################

variable "product_cpu" {
  description = "The amount of CPU to reserve for the container"
  type        = number
  default     = 1024
}

variable "product_memory" {
  description = "The amount of memory (in MiB) to reserve for the container"
  type        = number
  default     = 3072
}

variable "product_containerPort" {
  description = "The port on the container to associate with the load balancer"
  type        = number
  default     = 4003
}

variable "product_hostPort" {
  description = "The port on the host to associate with the load balancer"
  type        = number
  default     = 4003
}

######################
## payment Variable ##
######################

variable "payment_cpu" {
  description = "The amount of CPU to reserve for the container"
  type        = number
  default     = 1024
}

variable "payment_memory" {
  description = "The amount of memory (in MiB) to reserve for the container"
  type        = number
  default     = 3072
}

variable "payment_containerPort" {
  description = "The port on the container to associate with the load balancer"
  type        = number
  default     = 4002
}

variable "payment_hostPort" {
  description = "The port on the host to associate with the load balancer"
  type        = number
  default     = 4002
}

######################
## purchase Variable ##
######################

variable "purchase_cpu" {
  description = "The amount of CPU to reserve for the container"
  type        = number
  default     = 1024
}

variable "purchase_memory" {
  description = "The amount of memory (in MiB) to reserve for the container"
  type        = number
  default     = 3072
}

variable "purchase_containerPort" {
  description = "The port on the container to associate with the load balancer"
  type        = number
  default     = 4004
}

variable "purchase_hostPort" {
  description = "The port on the host to associate with the load balancer"
  type        = number
  default     = 4004
}

######################
## cart Variable ##
######################

variable "cart_cpu" {
  description = "The amount of CPU to reserve for the container"
  type        = number
  default     = 1024
}

variable "cart_memory" {
  description = "The amount of memory (in MiB) to reserve for the container"
  type        = number
  default     = 3072
}

variable "cart_containerPort" {
  description = "The port on the container to associate with the load balancer"
  type        = number
  default     = 4005
}

variable "cart_hostPort" {
  description = "The port on the host to associate with the load balancer"
  type        = number
  default     = 4005
}