#########################################
## Create IAM user and attach policies ##
#########################################

resource "aws_iam_user" "github_actions" {
  name = "github_actions"
  path = "/"
}

resource "aws_iam_policy" "ecr_access_policy" {
  name = "ecr_access_policy"
  description = "Allows access to ECR"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
        {
            Effect = "Allow"
            Action = [
                "ecr:CompleteLayerUpload",
                "ecr:UploadLayerPart",
                "ecr:InitiateLayerUpload",
                "ecr:BatchCheckLayerAvailability",
                "ecr:PutImage"
            ],
            Resource = [aws_ecr_repository.react_app.arn, 
                       aws_ecr_repository.account_management.arn, 
                       aws_ecr_repository.payment_service.arn, 
                       aws_ecr_repository.purchase_service.arn, 
                       aws_ecr_repository.product_catalog.arn, 
                       aws_ecr_repository.shopping_cart.arn]
        },
        {
            Effect = "Allow",
            Action = "ecr:GetAuthorizationToken",
            Resource = "*"
        }
    ]
})
  
}

resource "aws_iam_policy" "s3_tfstate_upload_download" {
  name = "s3_tfstate_upload_download"
  description = "Allows access to S3"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
        {
            Effect = "Allow"
            Action = [
                "s3:GetObject",
                "s3:PutObject"
            ],
            Resource = [aws_s3_bucket.ebook-store-tfstate.arn]
        }
    ]
})
  
}

resource "aws_iam_user_policy_attachment" "github_actions_policy_attachment" {
  user       = aws_iam_user.github_actions.name
  policy_arn = aws_iam_policy.ecr_access_policy.arn
}

resource "aws_iam_user_policy_attachment" "s3_tfstate_upload_download_attachment" {
  user       = aws_iam_user.github_actions.name
  policy_arn = aws_iam_policy.s3_tfstate_upload_download.arn
}

#############################################


resource "aws_iam_role" "ecs_task_execution_role" {
  name = "ecs_task_execution_role"
  description = "Allows the execution of ECS tasks"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role" "ecs_task_role" {
  name = "ecs_task_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      },
    ]
  })
}

#############################################
## Attach policies ecs-task-execution-role ##
#############################################

resource "aws_iam_role_policy_attachment" "ecs-task-role-policy-attachment-ecs" {
  role       = aws_iam_role.ecs_task_execution_role.id
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy_attachment" "ecs-task-role-policy-attachment-cw" {
  role       = aws_iam_role.ecs_task_execution_role.id
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchFullAccess"
}

###################################
## Attach policies ecs-task-role ##
###################################

resource "aws_iam_role_policy_attachment" "ecs-cli-policy-attachment" {
  role       = aws_iam_role.ecs_task_role.id
  policy_arn = "arn:aws:iam::483451515855:policy/ECS-for-CLI-Exec"
}

resource "aws_iam_role_policy_attachment" "ecs-resources-full-access-policy-attachment" {
  role       = aws_iam_role.ecs_task_role.id
  policy_arn = "arn:aws:iam::aws:policy/AmazonECS_FullAccess"
}

# resource "aws_iam_user" "github_actions_user" {
#   name = "github_actions_user"
#   path = "/"
# }

# resource "aws_iam_role" "ecs_task_execution_role" {
#   name               = "ecs_task_execution_role"
#   assume_role_policy = data.aws_iam_policy.AmazonECSServiceRolePolicy.arn
# }

# resource "aws_iam_policy" "github_actions_policy" {
#   name        = "github_actions_policy"
#   description = ""

#   policy = jsondecode({
#     "Version" : "2012-10-17",
#     "Statement" : [
#       {
#         "Effect" : "Allow",
#         "Action" : [
#           "ecr:GetAuthorizationToken",
#           "ecr:BatchCheckLayerAvailability",
#           "ecr:GetDownloadUrlForLayer",
#           "ecr:BatchGetImage",

#           "ssm:GetParameters",
#           "logs:CreateLogStream",
#           "logs:PutLogEvents"
#         ],
#         "Resource" : "*"
#       }
#     ]
#   })
# }

# data "aws_iam_policy" "AmazonECSServiceRolePolicy" {
#   arn = "arn:aws:iam::aws:policy/aws-service-role/AmazonECSServiceRolePolicy"
# }

# resource "aws_iam_role" "github_s3_access_role" {
#   name = "github_s3-access-role"
#   assume_role_policy = data.aws_iam_policy.AmazonS3FullAccess.arn
# }

# data "aws_iam_policy" "AmazonS3FullAccess" {
#   arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
# }

# resource "aws_iam_role_policy_attachment" "github_s3_access_role_attachment" {
#   role       = aws_iam_role.github_s3_access_role.name
#   policy_arn = aws_iam_policy.AmazonS3FullAccess.arn
# }
# # User creation
# resource "aws_iam_user" "zambo" {
#   name          = "zambo"
#   path          = "/"
#   force_destroy = true
# }

# resource "aws_iam_user" "mahila" {
#   name          = "mahila"
#   path          = "/"
#   force_destroy = true
# }

# resource "aws_iam_user" "teo" {
#   name          = "teo"
#   path          = "/"
#   force_destroy = true
# }

# resource "aws_iam_user" "marija" {
#   name          = "marija"
#   path          = "/"
#   force_destroy = true
# }

# # Group creation
# resource "aws_iam_user_group_membership" "zambo-group-membership" {
#   user = aws_iam_user.zambo.name

#   groups = [
#     aws_iam_group.admin-group.name,
#   ]
# }

# resource "aws_iam_user_group_membership" "mahila-group-membership" {
#   user = aws_iam_user.mahila.name

#   groups = [
#     aws_iam_group.admin-group.name,
#   ]
# }

# resource "aws_iam_user_group_membership" "teo-group-membership" {
#   user = aws_iam_user.teo.name

#   groups = [
#     aws_iam_group.admin-group.name,
#   ]
# }

# resource "aws_iam_user_group_membership" "marija-group-membership" {
#   user = aws_iam_user.marija.name

#   groups = [
#     aws_iam_group.admin-group.name,
#   ]
# }

# # Create the policy document
# data "aws_iam_policy_document" "admin" {
#   statement {
#     effect    = "Allow"
#     actions   = ["*"]
#     resources = ["*"]
#   }
# }

# # Create the group
# resource "aws_iam_group" "admin-group" {
#   name = "admin-group"
# }

# # Attach the policy to the group
# resource "aws_iam_group_policy_attachment" "admin-group-attachment" {
#   group      = aws_iam_group.group.name
#   policy_arn = aws_iam_policy.admin.arn
# }

# # Login profile creation
# resource "aws_iam_user_login_profile" "zambo" {
#   user    = aws_iam_user.zambo.name
#   pgp_key = "keybase:zambo"
# }

# output "password" {
#   value = aws_iam_user_login_profile.zambo.encrypted_password
# }

# # Login profile creation
# resource "aws_iam_user_login_profile" "mahila" {
#   user    = aws_iam_user.mahila.name
#   pgp_key = "keybase:mahila"
# }

# output "password" {
#   value = aws_iam_user_login_profile.mahila.encrypted_password
# }

# # Login profile creation
# resource "aws_iam_user_login_profile" "teo" {
#   user    = aws_iam_user.teo.name
#   pgp_key = "keybase:teo"
# }

# output "password" {
#   value = aws_iam_user_login_profile.teo.encrypted_password
# }

# # Login profile creation
# resource "aws_iam_user_login_profile" "marija" {
#   user    = aws_iam_user.marija.name
#   pgp_key = "keybase:marija"
# }

# output "password" {
#   value = aws_iam_user_login_profile.marija.encrypted_password
# }

