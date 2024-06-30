##################
## web Variable ##
##################

variable "web_cpu" {
  description = "The amount of CPU to reserve for the container"
  type        = number
  default     = 2
}

variable "web_memory" {
  description = "The amount of memory (in MiB) to reserve for the container"
  type        = number
  default     = 4
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

######################
## account Variable ##
######################

variable "account_cpu" {
  description = "The amount of CPU to reserve for the container"
  type        = number
  default     = 2
}

variable "account_memory" {
  description = "The amount of memory (in MiB) to reserve for the container"
  type        = number
  default     = 4
}

variable "account_containerPort" {
  description = "The port on the container to associate with the load balancer"
  type        = number
  default     = 80
}

variable "account_hostPort" {
  description = "The port on the host to associate with the load balancer"
  type        = number
  default     = 80
}

######################
## product Variable ##
######################

variable "product_cpu" {
  description = "The amount of CPU to reserve for the container"
  type        = number
  default     = 2
}

variable "product_memory" {
  description = "The amount of memory (in MiB) to reserve for the container"
  type        = number
  default     = 4
}

variable "product_containerPort" {
  description = "The port on the container to associate with the load balancer"
  type        = number
  default     = 80
}

variable "product_hostPort" {
  description = "The port on the host to associate with the load balancer"
  type        = number
  default     = 80
}

######################
## payment Variable ##
######################

variable "payment_cpu" {
  description = "The amount of CPU to reserve for the container"
  type        = number
  default     = 2
}

variable "payment_memory" {
  description = "The amount of memory (in MiB) to reserve for the container"
  type        = number
  default     = 4
}

variable "payment_containerPort" {
  description = "The port on the container to associate with the load balancer"
  type        = number
  default     = 80
}

variable "payment_hostPort" {
  description = "The port on the host to associate with the load balancer"
  type        = number
  default     = 80
}

######################
## purchase Variable ##
######################

variable "purchase_cpu" {
  description = "The amount of CPU to reserve for the container"
  type        = number
  default     = 2
}

variable "purchase_memory" {
  description = "The amount of memory (in MiB) to reserve for the container"
  type        = number
  default     = 4
}

variable "purchase_containerPort" {
  description = "The port on the container to associate with the load balancer"
  type        = number
  default     = 80
}

variable "purchase_hostPort" {
  description = "The port on the host to associate with the load balancer"
  type        = number
  default     = 80
}

######################
## cart Variable ##
######################

variable "cart_cpu" {
  description = "The amount of CPU to reserve for the container"
  type        = number
  default     = 2
}

variable "cart_memory" {
  description = "The amount of memory (in MiB) to reserve for the container"
  type        = number
  default     = 4
}

variable "cart_containerPort" {
  description = "The port on the container to associate with the load balancer"
  type        = number
  default     = 80
}

variable "cart_hostPort" {
  description = "The port on the host to associate with the load balancer"
  type        = number
  default     = 80
}