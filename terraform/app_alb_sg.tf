##################################################
## Security Group for Application Load Balancer ##
##################################################

resource "aws_security_group" "app_alb_sg" {
  name        = "app_alb_sg"
  description = "Security group for Application Load Balancer"
  vpc_id      = aws_vpc.ebook_store_vpc.id

  ingress {
    description = "Allow HTTP inbound traffic"
    from_port   = 4000
    to_port     = 4010
    protocol    = "tcp"
    security_groups = [aws_security_group.web_sg.id, aws_security_group.app_sg.id]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "app_alb_sg"
    Terraform = "true"
  }
}