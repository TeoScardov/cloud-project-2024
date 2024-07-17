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
  name            = "react_app"
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
    container_port   = var.web_containerPort
  }

  lifecycle {
    ignore_changes = [desired_count]
  
  }
}

################################
## Create ECS account Service ##
################################

resource "aws_ecs_service" "ecs_account_service" {
  name            = "account_management"
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
    container_port   = var.account_containerPort
  }

  lifecycle {
    ignore_changes = [desired_count]
  }
}

################################
## Create ECS product Service ##
################################

resource "aws_ecs_service" "ecs_product_service" {
  name            = "product_catalog"
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
    container_port   = var.product_containerPort
  }
  lifecycle {
    ignore_changes = [desired_count]
  
  }
}

################################
## Create ECS payment Service ##
################################

resource "aws_ecs_service" "ecs_payment_service" {
  name            = "payment_service"
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
    container_port   = var.payment_containerPort
  }

  lifecycle {
    ignore_changes = [desired_count]
  
  }
}

################################
## Create ECS purchase Service ##
################################

resource "aws_ecs_service" "ecs_purchase_service" {
  name            = "purchase_service"
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
    container_port   = var.purchase_containerPort
  }

  lifecycle {
    ignore_changes = [desired_count]
  
  }
}

################################
## Create ECS cart Service ##
################################

resource "aws_ecs_service" "ecs_cart_service" {
  name            = "shopping_cart"
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
    container_port   = var.cart_containerPort
  }

  lifecycle {
    ignore_changes = [desired_count]
  
  }
}

####################################
## Create ECS web Task Definition ##
####################################

resource "aws_ecs_task_definition" "ecs_task_definition_web" {
  family                   = "web-task-definition"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.web_cpu
  memory                   = var.web_memory

  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn      = aws_iam_role.ecs_task_role.arn

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture = "X86_64"
  }

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
          appProtocol   = "http"

        },
      ]
      environment = [
        {
          name  = "VITE_NUMBER_OF_BOOKS_TO_DISPLAY"
          value = var.env_number_of_books_to_display
        },
      ]
      logConfiguration = {
          logDriver = "awslogs"
          options = {
            awslogs-group = aws_cloudwatch_log_group.ebook-store-cloudwatch.name
            awslogs-region = "us-east-1"
            awslogs-stream-prefix = "ecs"
          }
        }
    },
  ])
}

########################################
## Create ECS account Task Definition ##
########################################

resource "aws_ecs_task_definition" "ecs_task_definition_account" {
  family                   = "account-task-definition"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.account_cpu
  memory                   = var.account_memory

  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn      = aws_iam_role.ecs_task_role.arn

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture = "X86_64"
  }

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
      environment = [
        {
          name = "JWT_SECRET_KEY",
          value = "${var.jwt_secret_key}"
        },
        {
          name  = "DATABASE_URL",
          value = "postgresql://${aws_rds_cluster.ebook_store_db.master_username}:${aws_rds_cluster.ebook_store_db.master_password}@${aws_rds_cluster.ebook_store_db.endpoint}:5432/${aws_rds_cluster.ebook_store_db.database_name}"
        }
      ]
      # logConfiguration = {
      #     logDriver = "awslogs"
      #     options = {
      #       awslogs-group = aws_cloudwatch_log_group.ebook-store-cloudwatch.name
      #       awslogs-region = "us-east-1"
      #       awslogs-stream-prefix = "ecs"
      #     }
      #   }
    }
  ])

  depends_on = [ aws_rds_cluster.ebook_store_db, aws_rds_cluster_instance.db_instance ]
}

########################################
## Create ECS product Task Definition ##
########################################

resource "aws_ecs_task_definition" "ecs_task_definition_product" {
  family                   = "product-task-definition"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.product_cpu
  memory                   = var.product_memory

  execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn      = aws_iam_role.ecs_task_role.arn

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture = "X86_64"
  }

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
      environment = [
        {
          name = "DB_URL",
          value = "postgresql://${aws_rds_cluster.ebook_store_db.master_username}:${aws_rds_cluster.ebook_store_db.master_password}@${aws_rds_cluster.ebook_store_db.endpoint}:5432/${aws_rds_cluster.ebook_store_db.database_name}"
        }
      ]
      # logConfiguration = {
      #     logDriver = "awslogs"
      #     options = {
      #       awslogs-group =  aws_cloudwatch_log_group.ebook-store-cloudwatch.name
      #       awslogs-region = "us-east-1"
      #       awslogs-stream-prefix = "ecs"
      #     }
      #   }
    }
  ])

  depends_on = [ aws_rds_cluster.ebook_store_db, aws_rds_cluster_instance.db_instance ]

}

########################################
## Create ECS payment Task Definition ##
########################################

resource "aws_ecs_task_definition" "ecs_task_definition_payment" {
  family                   = "payment-task-definition"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.payment_cpu
  memory                   = var.payment_memory
 
  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture = "X86_64"
  }

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
      environment = [
        {
          name = "SECRET_KEY",
          value = "${var.jwt_secret_key}"
        },
        {
          name  = "URL_PREFIX",
          value = "${var.payment_prefix}"
        }
      ]
      # logConfiguration = {
      #     logDriver = "awslogs"
      #     options = {
      #       awslogs-group =  aws_cloudwatch_log_group.ebook-store-cloudwatch.name
      #       awslogs-region = "us-east-1"
      #       awslogs-stream-prefix = "ecs"
      #     }
      #   }
    }
  ])
}

#########################################
## Create ECS purchase Task Definition ##
#########################################

resource "aws_ecs_task_definition" "ecs_task_definition_purchase" {
  family                   = "purchase-task-definition"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.purchase_cpu
  memory                   = var.purchase_memory

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture = "X86_64"
  }

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
      environment = [
        {
          name = "SECRET_KEY",
          value = "${var.jwt_secret_key}"
        },
        {
          name  = "SQLALCHEMY_DATABASE_URI",
          value = "postgresql://${aws_rds_cluster.ebook_store_db.master_username}:${aws_rds_cluster.ebook_store_db.master_password}@${aws_rds_cluster.ebook_store_db.endpoint}:5432/${aws_rds_cluster.ebook_store_db.database_name}"
        },
        {
          name  = "ACCOUNT_SERVICE_URL",
          value = "http://${aws_route53_record.entrypoint_app_lb_record.fqdn}:4001/api/account"
        },
        {
          name  = "PAYMENT_SERVICE_URL",
          value = "http://${aws_route53_record.entrypoint_app_lb_record.fqdn}:4002/api/payment"
        }
      ]
      # logConfiguration = {
      #     logDriver = "awslogs"
      #     options = {
      #       awslogs-group =  aws_cloudwatch_log_group.ebook-store-cloudwatch.name
      #       awslogs-region = "us-east-1"
      #       awslogs-stream-prefix = "ecs"
      #     }
      #   }
    }
  ])

  depends_on = [ aws_rds_cluster.ebook_store_db, aws_rds_cluster_instance.db_instance ]

}

#####################################
## Create ECS cart Task Definition ##
#####################################

resource "aws_ecs_task_definition" "ecs_task_definition_cart" {
  family                   = "cart-task-definition"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.cart_cpu
  memory                   = var.cart_memory

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture = "X86_64"
  }

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
      environment = [
        {
          name  = "DB_URL",
          value = "postgresql://${aws_rds_cluster.ebook_store_db.master_username}:${aws_rds_cluster.ebook_store_db.master_password}@${aws_rds_cluster.ebook_store_db.endpoint}:5432/${aws_rds_cluster.ebook_store_db.database_name}"
        },
        {
          name  = "USER_SERVICE_URL",
          value = "http://${aws_route53_record.entrypoint_app_lb_record.fqdn}:4001/api/account"
        },
        {
          name  = "PRODUCT_SERVICE_URL",
          value = "http://${aws_route53_record.entrypoint_app_lb_record.fqdn}:4003/api/product"
        }
      ]
      # logConfiguration = {
      #     logDriver = "awslogs"
      #     options = {
      #       awslogs-group =  aws_cloudwatch_log_group.ebook-store-cloudwatch.name
      #       awslogs-region = "us-east-1"
      #       awslogs-stream-prefix = "ecs"
      #     }
      #   }
    }
  ])

  depends_on = [ aws_rds_cluster.ebook_store_db, aws_rds_cluster_instance.db_instance ]
}