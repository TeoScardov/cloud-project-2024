variable "private_subnets_cidr" {
    type    = list(string)
    default = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24", "10.0.4.0/24"]
}

variable "private_subnets_names" {
    type    = list(string)
    default = ["ebook_store_private_subnet_application_1", "ebook_store_private_subnet_db_1", "ebook_store_private_subnet_application_2", "ebook_store_private_subnet_db_2"]
}