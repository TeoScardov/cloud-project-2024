variable "public_subnets_cidr" {
    type    = list(string)
    default = ["10.0.101.0/24", "10.0.102.0/24"]
}

variable "public_subnets_names" {
    type    = list(string)
    default = ["ebook_store_public_subnet_web_1", "ebook_store_public_subnet_web_2"]
}