###############################
## Application Load Balancer ##
###############################

resource "aws_lb" "app_alb" {
  name               = "appAlb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.app_alb_sg.id]
  subnets            = [aws_subnet.ebook_store_private_subnet_application_1.id, aws_subnet.ebook_store_private_subnet_application_2.id]

  enable_deletion_protection = false
  #enable_http2               = true
  #enable_cross_zone_load_balancing = true

  tags = {
    Name = "web_alb"
    Terraform = "true"
  }
}

resource "aws_alb_target_group" "app_alb_target_group" {
  name        = "appAlbTargetGroup"
  port        = 80
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = aws_vpc.ebook_store_vpc.id

  health_check {
    path                = "/"
    protocol            = "HTTP"
    port                = "traffic-port"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 10
  }

  tags = {
    Name = "web_alb_target_group"
    Terraform = "true"
  }
  
}

resource "aws_lb_listener" "app_alb_listener" {
  load_balancer_arn = aws_lb.app_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.app_alb_target_group.arn  
  }
}