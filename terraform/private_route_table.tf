#########################
## Private Route Table ##
#########################

resource "aws_route_table" "ebook_store_private_route_table" {
  vpc_id = aws_vpc.ebook_store_vpc.id

  # route {
  #   cidr_block = "0.0.0.0/0"
  #   nat_gateway_id = aws_nat_gateway.nat_gateway.id
  # }

  route {
    cidr_block = "10.0.0.0/16"
    gateway_id = "local"
  }

  tags = {
    Name = var.private_route_table_name
    Terraform = "true"
  }
}

#########################################
## Private Route Table Association App ##
#########################################

resource "aws_route_table_association" "ebook_store_private_route_table_association_application_1" {
  subnet_id      = aws_subnet.ebook_store_private_subnet_application_1.id
  route_table_id = aws_route_table.ebook_store_private_route_table.id
}

resource "aws_route_table_association" "ebook_store_private_route_table_association_application_2" {
  subnet_id      = aws_subnet.ebook_store_private_subnet_application_2.id
  route_table_id = aws_route_table.ebook_store_private_route_table.id
}

########################################
## Private Route Table Association db ##
########################################

resource "aws_route_table_association" "ebook_store_private_route_table_association_db_1" {
  subnet_id      = aws_subnet.ebook_store_private_subnet_db_1.id
  route_table_id = aws_route_table.ebook_store_private_route_table.id
}

resource "aws_route_table_association" "ebook_store_private_route_table_association_db_2" {
  subnet_id      = aws_subnet.ebook_store_private_subnet_db_2.id
  route_table_id = aws_route_table.ebook_store_private_route_table.id
}