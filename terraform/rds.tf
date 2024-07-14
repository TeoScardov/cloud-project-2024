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
  cluster_identifier        = "db"
  engine                    = "aurora-postgresql"
  database_name             = var.postgres_db_name
  master_username           = var.postgres_username
  master_password           = var.postgres_password
  db_subnet_group_name      = aws_db_subnet_group.ebook_store_db_subnet_group.name
  vpc_security_group_ids    = [aws_security_group.db_sg.id]
  skip_final_snapshot       = true
  backup_retention_period   = 7
  apply_immediately         = true


  serverlessv2_scaling_configuration {
    max_capacity = 2
    min_capacity = 1
  }

  tags = {
    Name = "ebook_store_db"
    Terraform = "true"
  }
  
}

resource "aws_rds_cluster_instance" "db_instance" {
  count              = 2
  cluster_identifier = aws_rds_cluster.ebook_store_db.id
  instance_class     = "db.serverless"
  engine             = aws_rds_cluster.ebook_store_db.engine
  engine_version     = aws_rds_cluster.ebook_store_db.engine_version
  
  publicly_accessible = false
  apply_immediately  = true
  
  tags = {
    Name = "db_instance"
    Terraform = "true"
  }
  
}

