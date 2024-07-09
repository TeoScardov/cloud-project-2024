################################
## Security Group Application ##
################################

resource "aws_security_group" "app_sg" {
  name        = "app_sg"
  description = "Security group for Application"
  vpc_id      = aws_vpc.ebook_store_vpc.id

  ingress {
    description = "Allow HTTP inbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    security_groups = [aws_security_group.app_lb_sg.id]
  }

  dynamic "ingress" {
        for_each = var.enable_ssh == true ? [0] : []
        content {
            description = "SSH from a specific IP"
            from_port   = 22
            to_port     = 22
            protocol    = "tcp"
            cidr_blocks = ["${var.ssh_address}"]
        }
    }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

    tags = {
        Name = "app_sg"
        Terraform = "true"
    }
}
