###############
##### vpc #####
###############

resource "aws_vpc" "ebook_store_vpc" {
  cidr_block = var.vpc_cidr
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {
    Name = "ebook_store_vpc"
    Terraform = "true"
  }

}

# module "vpc" {
#   source = "terraform-aws-modules/vpc/aws"
#   version = "5.8.1"

#   name = "ebook_store_vpc"
#   cidr = var.vpc_cidr

#   azs             = var.azs
#   private_subnets = var.private_subnets_cidr
#   public_subnets  = var.public_subnets_cidr

#   private_subnet_names = var.private_subnets_names
#   public_subnet_names = var.public_subnets_names

#   enable_nat_gateway = false#true
#   enable_vpn_gateway = false#true

#   tags = {
#     Name = "ebook_store_vpc"
#     Terraform = "true"
#     Environment = "dev"
#   }
# }


