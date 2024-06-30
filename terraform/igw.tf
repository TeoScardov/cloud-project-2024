###############
##### igw #####
###############

resource "aws_internet_gateway" "ebook_store_igw" {
  vpc_id = aws_vpc.ebook_store_vpc.id
  tags = {
    Name = "ebook_store_igw"
    Terraform = "true"
  }
  
}