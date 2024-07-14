###############################
## Application Load Balancer ##
###############################

resource "aws_lb" "web_lb" {
  name               = "weblb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.web_lb_sg.id]
  subnets            = [aws_subnet.ebook_store_public_subnet_web_1.id, aws_subnet.ebook_store_public_subnet_web_2.id]

  enable_deletion_protection = false
  enable_http2               = true
  enable_cross_zone_load_balancing = true

  tags = {
    Name = "web_lb"
    Terraform = "true"
  }
}

resource "aws_lb_target_group" "web_lb_target_group" {
  name        = "weblbTargetGroup"
  port        = var.web_hostPort
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = aws_vpc.ebook_store_vpc.id

  health_check {
    path                = "/health"
    protocol            = "HTTP"
    port                = "traffic-port"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 10
  }

  tags = {
    Name = "web_lb_target_group"
    Terraform = "true"
  }
  
}

resource "aws_lb_listener" "web_lb_listener" {
  load_balancer_arn = aws_lb.web_lb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web_lb_target_group.arn
  }
}