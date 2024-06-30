########################
## Security Group Web ##
########################

resource "aws_security_group" "web_sg" {
  name        = "web_sg"
  description = "Security group for Web"
  vpc_id      = aws_vpc.ebook_store_vpc.id

  ingress {
    description = "Allow HTTP inbound traffic"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    security_groups = [aws_security_group.web_alb_sg.id]

    }

    ingress {
    description = "Allow HTTPS inbound traffic"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    security_groups = [aws_security_group.web_alb_sg.id]
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
        Name = "web_sg"
        Terraform = "true"
    }
}