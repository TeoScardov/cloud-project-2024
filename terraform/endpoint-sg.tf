################################
## Security Group Endpoints ##
################################

resource "aws_security_group" "endpoints_sg" {
  name        = "endpoints_sg"
  description = "Security group for Endpoints"
  vpc_id      = aws_vpc.ebook_store_vpc.id

  ingress {
    description = "Allow TCP inbound traffic from 443"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    security_groups = [aws_security_group.app_sg.id, aws_security_group.web_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

    tags = {
        Name = "endpoints_sg"
        Terraform = "true"
    }
}