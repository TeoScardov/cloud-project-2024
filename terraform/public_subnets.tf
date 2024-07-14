######################
## Public Subnets 1 ##
######################

resource "aws_subnet" "ebook_store_public_subnet_web_1" {
  vpc_id                  = aws_vpc.ebook_store_vpc.id
  cidr_block              = var.public_subnets_cidr[0]
  availability_zone       = var.azs[0]
  map_public_ip_on_launch = true
  tags = {
    Name = var.public_subnets_names[0]
    Terraform = "true"
  }
}

######################
## Public Subnets 2 ##
######################

resource "aws_subnet" "ebook_store_public_subnet_web_2" {
  vpc_id                  = aws_vpc.ebook_store_vpc.id
  cidr_block              = var.public_subnets_cidr[1]
  availability_zone       = var.azs[1]
  map_public_ip_on_launch = true
  tags = {
    Name = var.public_subnets_names[1]
    Terraform = "true"
  }
}

