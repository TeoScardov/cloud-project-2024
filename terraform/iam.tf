# #########################################
# ## Create IAM user and attach policies ##
# #########################################

# resource "aws_iam_user" "github_actions" {
#   name = "github_actions"
# }

# ###################
# # Create policies #
# ###################

# resource "aws_iam_policy" "ecr_pull_policy" {
#   name = "ecr_pull_policy"
#   description = "Allows access to ECR"
#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#         {
#             Sid = "AllowPull"
#             Effect = "Allow"
#             Action = [
#                 "ecr:CompleteLayerUpload",
#                 "ecr:UploadLayerPart",
#                 "ecr:InitiateLayerUpload",
#                 "ecr:BatchCheckLayerAvailability",
#                 "ecr:DescribeRepositories",
#                 "ecr:DescribeImages",
#                 "ecr:PutImage",
#                 "ecr:ListTagsForResource",
#             ],
#             Resource = [aws_ecr_repository.react_app.arn, 
#                         aws_ecr_repository.account_management.arn, 
#                         aws_ecr_repository.payment_service.arn, 
#                         aws_ecr_repository.purchase_service.arn, 
#                         aws_ecr_repository.product_catalog.arn, 
#                         aws_ecr_repository.shopping_cart.arn]
#         }
#     ]
# })
  
# }


# resource "aws_iam_policy" "s3_tfstate_upload_download" {
#   name = "s3_tfstate_upload_download"
#   description = "Allows access to S3"
#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#         {
#             Effect = "Allow"
#             Action = [
#                 "s3:GetObject",
#                 "s3:PutObject",
#                 "s3:ListBucket"
#             ],
#             Resource = [aws_s3_bucket.ebook-store-tfstate.arn]
#         }
#     ]
# })
  
# }

# resource "aws_iam_policy" "ecr_push_policy" {
#   name = "ecr_push_policy"
#   description = "Allows push to ECR"
#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#         {
#             Sid = "AllowPush"
#             Effect = "Allow",
#             Action = "ecr:GetAuthorizationToken",
#             Resource = "*"
#         }
#     ]
# })
    
# }



# resource "aws_iam_user_policy_attachment" "github_actions_policy_attachment" {
#   user       = aws_iam_user.github_actions.name
#   policy_arn = aws_iam_policy.ecr_push_policy.arn
# }

# resource "aws_iam_user_policy_attachment" "s3_tfstate_upload_download_attachment" {
#   user       = aws_iam_user.github_actions.name
#   policy_arn = aws_iam_policy.s3_tfstate_upload_download.arn
# }

#################################
## Create ecsTaskExecutionRole ##
#################################

resource "aws_iam_role" "ecs_task_execution_role" {
  name        = "ecs_task_execution_role"
  description = "Allows the execution of ECS tasks"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = ""
        Effect = "Allow"
        Action = "sts:AssumeRole"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role-AmazonECSTaskExecutionRolePolicy" {
  role       = aws_iam_role.ecs_task_execution_role.id
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role-CloudWatchFullAccess" {
  role       = aws_iam_role.ecs_task_execution_role.id
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchFullAccess"
}

resource "aws_iam_policy" "ecr-policy" {
  name        = "ECRPolicy"
  description = "Allows ECS tasks to pull images from ECR"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
        {
            Sid = "AllowECR",
            Effect = "Allow",
            Action = [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "ecr:DescribeImages",
                "ecr:DescribeRepositories",
            ],
            Resource = "*"
        }
    ]
})
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role-ECRPolicy" {
  role       = aws_iam_role.ecs_task_execution_role.id
  policy_arn = aws_iam_policy.ecr-policy.arn
}

########################
## Create ecsTaskRole ##
########################

resource "aws_iam_role" "ecs_task_role" {
  name        = "ecs_task_role"
  description = ""

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = ""
        Effect = "Allow"
        Action = "sts:AssumeRole"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs-task-role-AmazonECS_FullAccesst" {
  role       = aws_iam_role.ecs_task_role.id
  policy_arn = "arn:aws:iam::aws:policy/AmazonECS_FullAccess"
}

resource "aws_iam_role_policy_attachment" "ecs-task-role-CloudWatchFullAccess" {
  role      = aws_iam_role.ecs_task_role.id
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchFullAccess"
}

########################
## Create lambdaRole ##
########################

resource "aws_iam_role" "lambda_role" {
  name        = "lambda_role"
  description = "Allows Lambda functions to call AWS services on your behalf."

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "s3_lambda_policy" {
  name = "s3_lambda_policy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ],
        Resource = "${aws_s3_bucket.elastic-book-store-bucket.arn}/*"
      }
    ]
  })
  
}

resource "aws_iam_role_policy_attachment" "lambda_role_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.s3_lambda_policy.arn
}

resource "aws_iam_policy" "basic_lambda_execution" {
  name = "basic_lambda_execution"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "ec2:CreateNetworkInterface",
          "ec2:DeleteNetworkInterface",
          "ec2:DescribeNetworkInterfaces"
        ],
        Resource = "*"
      }
    ]
  })
  
}

resource "aws_iam_role_policy_attachment" "basic_lambda_execution_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.basic_lambda_execution.arn
}

resource "aws_iam_policy" "db_lambda_policy" {
  name = "db_lambda_policy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement= [
      {
        Effect= "Allow",
        Action= [
          "rds-db:connect"
        ],
        Resource= "${aws_rds_cluster.ebook_store_db.arn}"
      }
    ]
  })
  
}

resource "aws_iam_role_policy_attachment" "db_lambda_role_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.db_lambda_policy.arn
}