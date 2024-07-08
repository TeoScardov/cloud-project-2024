########################
## Create ECS Cluster ##
########################

resource "aws_ecs_cluster" "ecs_cluster" {
  name = "ecs-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Name        = "ECS Cluster"
    Terraform   = "true"
  }
}

############################
## Create ECS Web Service ##
############################

resource "aws_ecs_service" "ecs_web_service" {
  name            = "ecs-service"
  cluster         = aws_ecs_cluster.ecs_cluster.id
  task_definition = aws_ecs_task_definition.ecs_task_definition_web.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [aws_subnet.ebook_store_public_subnet_web_1.id, aws_subnet.ebook_store_public_subnet_web_2.id]
    security_groups  = [aws_security_group.web_sg.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.web_lb_target_group.arn
    container_name   = "web"
    container_port   = 80
  }
}

################################
## Create ECS account Service ##
################################

resource "aws_ecs_service" "ecs_account_service" {
  name            = "ecs-service"
  cluster         = aws_ecs_cluster.ecs_cluster.id
  task_definition = aws_ecs_task_definition.ecs_task_definition_account.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [aws_subnet.ebook_store_private_subnet_application_1.id, aws_subnet.ebook_store_private_subnet_application_2.id]
    security_groups  = [aws_security_group.app_sg.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.account_lb_target_group.arn
    container_name   = "account"
    container_port   = 4001
  }
}

################################
## Create ECS product Service ##
################################

resource "aws_ecs_service" "ecs_product_service" {
  name            = "ecs-service"
  cluster         = aws_ecs_cluster.ecs_cluster.id
  task_definition = aws_ecs_task_definition.ecs_task_definition_product.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [aws_subnet.ebook_store_private_subnet_application_1.id, aws_subnet.ebook_store_private_subnet_application_2.id]
    security_groups  = [aws_security_group.app_sg.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.product_lb_target_group.arn
    container_name   = "product"
    container_port   = 4003
  }
}

################################
## Create ECS payment Service ##
################################

resource "aws_ecs_service" "ecs_payment_service" {
  name            = "ecs-service"
  cluster         = aws_ecs_cluster.ecs_cluster.id
  task_definition = aws_ecs_task_definition.ecs_task_definition_payment.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [aws_subnet.ebook_store_private_subnet_application_1.id, aws_subnet.ebook_store_private_subnet_application_2.id]
    security_groups  = [aws_security_group.app_sg.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.payment_lb_target_group.arn
    container_name   = "payment"
    container_port   = 4002
  }
}

################################
## Create ECS purchase Service ##
################################

resource "aws_ecs_service" "ecs_purchase_service" {
  name            = "ecs-service"
  cluster         = aws_ecs_cluster.ecs_cluster.id
  task_definition = aws_ecs_task_definition.ecs_task_definition_purchase.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [aws_subnet.ebook_store_private_subnet_application_1.id, aws_subnet.ebook_store_private_subnet_application_2.id]
    security_groups  = [aws_security_group.app_sg.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.purchase_lb_target_group.arn
    container_name   = "purchase"
    container_port   = 4004
  }
}

################################
## Create ECS cart Service ##
################################

resource "aws_ecs_service" "ecs_cart_service" {
  name            = "ecs-service"
  cluster         = aws_ecs_cluster.ecs_cluster.id
  task_definition = aws_ecs_task_definition.ecs_task_definition_cart.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [aws_subnet.ebook_store_private_subnet_application_1.id, aws_subnet.ebook_store_private_subnet_application_2.id]
    security_groups  = [aws_security_group.app_sg.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.cart_lb_target_group.arn
    container_name   = "cart"
    container_port   = 4005
  }
}

####################################
## Create ECS web Task Definition ##
####################################

resource "aws_ecs_task_definition" "ecs_task_definition_web" {
  family                   = "ecs-task-definition"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.web_cpu
  memory                   = var.web_memory

  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn      = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "web"
      image     = "${aws_ecr_repository.react_app.repository_url}:latest"
      cpu       = var.web_cpu
      memory    = var.web_memory
      essential = true
      portMappings = [
        {
          containerPort = var.web_containerPort
          hostPort      = var.web_hostPort
          protocol      = "tcp"
        }
      ]
      enviroment = [
        {
          name  = "NUMBER_OF_BOOKS_TO_DISPLAY"
          value = var.env_number_of_books_to_display
        },
        {
          name = "API_BASE_URL"
          value = "http://${aws_lb.app_lb.dns_name}"
        }
      ]
    }
  ])
}

########################################
## Create ECS account Task Definition ##
########################################

resource "aws_ecs_task_definition" "ecs_task_definition_account" {
  family                   = "ecs-task-definition"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.account_cpu
  memory                   = var.account_memory

  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn      = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "account"
      image     = "${aws_ecr_repository.account_management.repository_url}:latest"
      cpu       = var.account_cpu
      memory    = var.account_memory
      essential = true
      portMappings = [
        {
          containerPort = var.account_containerPort
          hostPort      = var.account_hostPort
          protocol      = "tcp"
          appProtocol   = "http"
        }
      ]
      enviroment = [
        {
          name  = "DATABASE_URL"
          value = "postgresql://${aws_rds_cluster.ebook_store_db.master_username}:${aws_rds_cluster.ebook_store_db.master_password}@${aws_rds_cluster.ebook_store_db.endpoint}:5432/${aws_rds_cluster.ebook_store_db.database_name}"
        }
      ]
    }
  ])
}

########################################
## Create ECS product Task Definition ##
########################################

resource "aws_ecs_task_definition" "ecs_task_definition_product" {
  family                   = "ecs-task-definition"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.product_cpu
  memory                   = var.product_memory

  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn      = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "product"
      image     = "${aws_ecr_repository.product_catalog.repository_url}:latest"
      cpu       = var.product_cpu
      memory    = var.product_memory
      essential = true
      portMappings = [
        {
          containerPort = var.product_containerPort
          hostPort      = var.product_hostPort
          protocol      = "tcp"
        }
      ]
    }
  ])
}

########################################
## Create ECS payment Task Definition ##
########################################

resource "aws_ecs_task_definition" "ecs_task_definition_payment" {
  family                   = "ecs-task-definition"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.payment_cpu
  memory                   = var.payment_memory

  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn      = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "payment"
      image     = "${aws_ecr_repository.payment_service.repository_url}:latest"
      cpu       = var.payment_cpu
      memory    = var.payment_memory
      essential = true
      portMappings = [
        {
          containerPort = var.payment_containerPort
          hostPort      = var.payment_hostPort
          protocol      = "tcp"
        }
      ]
    }
  ])
}

#########################################
## Create ECS purchase Task Definition ##
#########################################

resource "aws_ecs_task_definition" "ecs_task_definition_purchase" {
  family                   = "ecs-task-definition"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.purchase_cpu
  memory                   = var.purchase_memory

  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn      = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "purchase"
      image     = "${aws_ecr_repository.purchase_service.repository_url}:latest"
      cpu       = var.purchase_cpu
      memory    = var.purchase_memory
      essential = true
      portMappings = [
        {
          containerPort = var.purchase_containerPort
          hostPort      = var.purchase_hostPort
          protocol      = "tcp"
        }
      ]
    }
  ])
}

#####################################
## Create ECS cart Task Definition ##
#####################################

resource "aws_ecs_task_definition" "ecs_task_definition_cart" {
  family                   = "ecs-task-definition"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.cart_cpu
  memory                   = var.cart_memory

  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn      = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name      = "cart"
      image     = "${aws_ecr_repository.shopping_cart.repository_url}:latest"
      cpu       = var.cart_cpu
      memory    = var.cart_memory
      essential = true
      portMappings = [
        {
          containerPort = var.cart_containerPort
          hostPort      = var.cart_hostPort
          protocol      = "tcp"
        }
      ]
    }
  ])
}