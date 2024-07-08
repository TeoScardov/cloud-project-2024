######################
## RDB subnet group ##
######################

resource "aws_db_subnet_group" "ebook_store_db_subnet_group" {
  name       = "ebook_store_db_subnet_group"
  subnet_ids = [aws_subnet.ebook_store_private_subnet_db_1.id, aws_subnet.ebook_store_private_subnet_db_2.id]
  tags = {
    Name = "ebook_store_db_subnet_group"
    Terraform = "true"
  }
}

##################
## RDS instance ##
##################

resource "aws_rds_cluster" "ebook_store_db" {
  cluster_identifier      = "db"
  engine                  = "aurora-postgresql"
  engine_version          = "15.1"
  database_name           = var.postgres_db_name
  master_username         = var.postgres_username
  master_password         = var.postgres_password
  db_subnet_group_name    = aws_db_subnet_group.ebook_store_db_subnet_group.name
  vpc_security_group_ids  = [aws_security_group.db_sg.id]
  availability_zones      = var.db_availability_zone
  skip_final_snapshot     = true
  backup_retention_period = 7
  apply_immediately       = true
  tags = {
    Name = "ebook_store_db"
    Terraform = "true"
  }
  
}

# resource "aws_db_instance" "account_db" {
#   identifier           = "accountdb"
#   allocated_storage    = 20
#   storage_type         = "gp2"
#   engine               = "postgres"
#   engine_version       = "11.5"
#   instance_class       = "db.t2.micro"
#   username             = var.postgres_account_username
#   password             = var.postgres_account_password
#   db_subnet_group_name = aws_db_subnet_group.ebook_store_db_subnet_group.name
#   vpc_security_group_ids = [aws_security_group.db_sg.id]
#   skip_final_snapshot  = true
#   availability_zone = var.db_availability_zone
#   multi_az = var.enable_multi_az
#   tags = {
#     Name = "account_db"
#     Terraform = "true"
#   }
# }

# resource "aws_db_instance" "product_db" {
#   identifier           = "productdb"
#   allocated_storage    = 20
#   storage_type         = "gp2"
#   engine               = "postgres"
#   engine_version       = "11.5"
#   instance_class       = "db.t2.micro"
#   username             = var.postgres_product_username
#   password             = var.postgres_product_password
#   db_subnet_group_name = aws_db_subnet_group.ebook_store_db_subnet_group.name
#   vpc_security_group_ids = [aws_security_group.db_sg.id]
#   skip_final_snapshot  = true
#   availability_zone = var.db_availability_zone
#   multi_az = var.enable_multi_az
#   tags = {
#     Name = "product_db"
#     Terraform = "true"
#   }
# }

# resource "aws_db_instance" "purchase_db" {
#   identifier           = "purchasedb"
#   allocated_storage    = 20
#   storage_type         = "gp2"
#   engine               = "postgres"
#   engine_version       = "11.5"
#   instance_class       = "db.t2.micro"
#   username             = var.postgres_purchase_username
#   password             = var.postgres_purchase_password
#   db_subnet_group_name = aws_db_subnet_group.ebook_store_db_subnet_group.name
#   vpc_security_group_ids = [aws_security_group.db_sg.id]
#   skip_final_snapshot  = true
#   availability_zone = var.db_availability_zone
#   multi_az = var.enable_multi_az
#   tags = {
#     Name = "purchase_db"
#     Terraform = "true"
#   }
# }


# resource "aws_db_instance" "cart_db" {
#   identifier           = "cartdb"
#   allocated_storage    = 20
#   storage_type         = "gp2"
#   engine               = "postgres"
#   engine_version       = "11.5"
#   instance_class       = "db.t2.micro"
#   username             = var.postgres_cart_username
#   password             = var.postgres_cart_password
#   db_subnet_group_name = aws_db_subnet_group.ebook_store_db_subnet_group.name
#   vpc_security_group_ids = [aws_security_group.db_sg.id]
#   skip_final_snapshot  = true
#   availability_zone = var.db_availability_zone
#   multi_az = var.enable_multi_az
#   tags = {
#     Name = "cart_db"
#     Terraform = "true"
#   }
# }