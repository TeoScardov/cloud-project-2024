##########################
## Private Subnets App1 ##
##########################

resource "aws_subnet" "ebook_store_private_subnet_application_1" {
  vpc_id                  = aws_vpc.ebook_store_vpc.id
  cidr_block              = var.private_subnets_cidr[0]
  availability_zone       = var.azs[0]
  map_public_ip_on_launch = false
  tags = {
    Name = var.private_subnets_names[0]
    Terraform = "true"
  }
}

#########################
## Private Subnets db2 ##
#########################

resource "aws_subnet" "ebook_store_private_subnet_db_1" {
  vpc_id                  = aws_vpc.ebook_store_vpc.id
  cidr_block              = var.private_subnets_cidr[1]
  availability_zone       = var.azs[0]
  map_public_ip_on_launch = false
  tags = {
    Name = var.private_subnets_names[1]
    Terraform = "true"
  }
}

##########################
## Private Subnets App2 ##
##########################

resource "aws_subnet" "ebook_store_private_subnet_application_2" {
  vpc_id                  = aws_vpc.ebook_store_vpc.id
  cidr_block              = var.private_subnets_cidr[2]
  availability_zone       = var.azs[1]
  map_public_ip_on_launch = false
  tags = {
    Name = var.private_subnets_names[2]
    Terraform = "true"
  }
}

#########################
## Private Subnets db2 ##
#########################

resource "aws_subnet" "ebook_store_private_subnet_db_2" {
  vpc_id                  = aws_vpc.ebook_store_vpc.id
  cidr_block              = var.private_subnets_cidr[3]
  availability_zone       = var.azs[1]
  map_public_ip_on_launch = false
  tags = {
    Name = var.private_subnets_names[3]
    Terraform = "true"
  }
}