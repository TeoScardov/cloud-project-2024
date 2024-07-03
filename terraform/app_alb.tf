###############################
## Application Load Balancer ##
###############################

resource "aws_lb" "app_lb" {
  name               = "applb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.app_lb_sg.id]
  subnets            = [aws_subnet.ebook_store_private_subnet_application_1.id, aws_subnet.ebook_store_private_subnet_application_2.id]

  enable_deletion_protection = false
  enable_http2               = true
  enable_cross_zone_load_balancing = true

  tags = {
    Name = "web_lb"
    Terraform = "true"
  }
}

##########################
## ALB Target Group ##
##########################
resource "aws_lb_target_group" "account_lb_target_group" {
  name        = "accountlbTargetGroup"
  port        = var.account_hostPort
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = aws_vpc.ebook_store_vpc.id

  health_check {
    path                = "/api/account/health"
    protocol            = "HTTP"
    port                = "traffic-port"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 10
  }

  tags = {
    Name = "account_lb_target_group"
    Terraform = "true"
  }
  
}

resource "aws_lb_target_group" "product_lb_target_group" {
  name        = "productlbTargetGroup"
  port        = var.product_hostPort
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = aws_vpc.ebook_store_vpc.id

  health_check {
    path                = "/api/product/test"
    protocol            = "HTTP"
    port                = "traffic-port"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 10
  }

  tags = {
    Name = "product_lb_target_group"
    Terraform = "true"
  }
  
}

resource "aws_lb_target_group" "payment_lb_target_group" {
  name        = "paymentlbTargetGroup"
  port        = var.payment_hostPort
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = aws_vpc.ebook_store_vpc.id

  health_check {
    path                = "/api/payment"
    protocol            = "HTTP"
    port                = "traffic-port"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 10
  }

  tags = {
    Name = "payment_lb_target_group"
    Terraform = "true"
  }
  
}

resource "aws_lb_target_group" "purchase_lb_target_group" {
  name        = "purchaselbTargetGroup"
  port        = var.purchase_hostPort
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = aws_vpc.ebook_store_vpc.id

  health_check {
    path                = "/api/purchase"
    protocol            = "HTTP"
    port                = "traffic-port"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 10
  }

  tags = {
    Name = "purchase_lb_target_group"
    Terraform = "true"
  }
  
}

resource "aws_lb_target_group" "cart_lb_target_group" {
  name        = "cartlbTargetGroup"
  port        = var.cart_hostPort
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = aws_vpc.ebook_store_vpc.id

  health_check {
    path                = "/api/cart/health"
    protocol            = "HTTP"
    port                = "traffic-port"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 10
  }

  tags = {
    Name = "cart_lb_target_group"
    Terraform = "true"
  }
  
}

##################
## ALB Listener ##
##################

resource "aws_lb_listener" "app_lb_listener" {
  load_balancer_arn = aws_lb.application_load_balancer.arn
  port              = "80"
  protocol          = "HTTP"
  default_action {
    type = "fixed-response"
    fixed_response {
      content_type = "text/plain"
      message_body = "404 Not Found"
      status_code  = "404"
    }
  }
}

resource "aws_lb_listener_rule" "account_lb_listener_rule" {
  listener_arn = aws_lb_listener.app_lb_listener.arn
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.account_lb_target_group.arn
  }
  condition {
    path_pattern {
      values = ["/api/account/*"]
    }
  }
  
}

resource "aws_lb_listener_rule" "product_lb_listener_rule" {
  listener_arn = aws_lb_listener.app_lb_listener.arn
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.product_lb_target_group.arn
  }
  condition {
    path_pattern {
      values = ["/api/product/*"]
    }
  }
  
}

resource "aws_lb_listener_rule" "payment_lb_listener_rule" {
  listener_arn = aws_lb_listener.app_lb_listener.arn
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.payment_lb_target_group.arn
  }
  condition {
    path_pattern {
      values = ["/api/payment/*"]
    }
  }
  
}

resource "aws_lb_listener_rule" "purchase_lb_listener_rule" {
  listener_arn = aws_lb_listener.app_lb_listener.arn
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.purchase_lb_target_group.arn
  }
  condition {
    path_pattern {
      values = ["/api/purchase/*"]
    }
  }
  
}

resource "aws_lb_listener_rule" "cart_lb_listener_rule" {
  listener_arn = aws_lb_listener.app_lb_listener.arn
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.cart_lb_target_group.arn
  }
  condition {
    path_pattern {
      values = ["/api/cart/*"]
    }
  }
  
}

