##################################################
## Security Group for Application Load Balancer ##
##################################################

resource "aws_security_group" "app_lb_sg" {
  name        = "app_lb_sg"
  description = "Security group for Application Load Balancer"
  vpc_id      = aws_vpc.ebook_store_vpc.id

  ingress {
    description = "HTTP from VPC"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    security_groups = [aws_security_group.web_sg.id]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "app_lb_sg"
    Terraform = "true"
  }
}