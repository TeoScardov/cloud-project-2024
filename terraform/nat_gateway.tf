#################
## NAT Gateway ##
#################

resource "aws_eip" "eip_nat_gateway" {
    domain = "vpc"

    tags = {
      name = "eip_nat_gateway"
    }
  
}

resource "aws_nat_gateway" "nat_gateway" {
  allocation_id = aws_eip.eip_nat_gateway.id
  subnet_id     = aws_subnet.ebook_store_public_subnet_web_2.id
  tags = {
    Name = "nat_gateway"
    Terraform = "true"
  }
}