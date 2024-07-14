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


