########################
## Public Route Table ##
########################

resource "aws_route_table" "ebook_store_public_route_table" {
  vpc_id = aws_vpc.ebook_store_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.ebook_store_igw.id
  }
  
  tags = {
    Name = var.public_route_table_name
    Terraform = "true"
  }
}

####################################
## Public Route Table Association ##
####################################

resource "aws_route_table_association" "ebook_store_public_route_table_association_1" {
  subnet_id      = aws_subnet.ebook_store_public_subnet_web_1.id
  route_table_id = aws_route_table.ebook_store_public_route_table.id
}

# resource "aws_route_table_association" "ebook_store_public_route_table_association_2" {
#   subnet_id      = aws_subnet.ebook_store_public_subnet_web_2.id
#   route_table_id = aws_route_table.ebook_store_public_route_table.id
# }