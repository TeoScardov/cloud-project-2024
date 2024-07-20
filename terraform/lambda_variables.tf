######################
## Layers Variables ##
######################

variable "psycopg2_layer_key" {
  description = "The key for the psycopg2 layer"
  type        = string
  default     = "psycopg2_layer.zip"
}

variable "postgres_utils_layer_key" {
  description = "The key for the postgres utils layer"
  type        = string
  default     = "pg_client_tools_layer.zip"
}

variable "lambda_code_key" {
  description = "The key for the lambda code"
  type        = string
  default     = "lambda_function.zip" 
}

variable "lambda_code_source" {
  description = "The source for the lambda code"
  type        = string
  default     = "lambda_function.zip" 
}

###############################
## Lambda Function Variables ##
###############################

variable "lambda_runtime" {
  description = "The runtime for the lambda function"
  type        = string
  default     = "python3.9"
}

variable "lambda_memory_size" {
  description = "The memory size for the lambda function"
  type        = number
  default     = 512
}

variable "lambda_timeout" {
  description = "The timeout for the lambda function"
  type        = number
  default     = 300
}

variable "dump_key" {
  description = "The key of the postgres dump"
  type        = string
  default     = "flask_db.dump"
}