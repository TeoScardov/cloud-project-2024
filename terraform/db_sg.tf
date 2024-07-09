#############################
## Security Group Database ##
#############################

resource "aws_security_group" "db_sg" {
  name        = "db_sg"
  description = "Security group for Database"
  vpc_id      = aws_vpc.ebook_store_vpc.id

  ingress {
    description = "Allow PostgreSQL inbound traffic"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    security_groups = [aws_security_group.app_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    }

    tags = {
        Name = "db_sg"
        Terraform = "true"
    }
}