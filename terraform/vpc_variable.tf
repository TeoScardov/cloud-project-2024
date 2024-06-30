variable "azs" {
    type    = list(string)
    default = ["us-east-1a", "us-east-1b"]
}

variable "vpc_cidr" {
    type    = string
    default = "10.0.0.0/16"
}