##########################
## Create Lambda Layers ##
##########################

resource "aws_lambda_layer_version" "psycopg2_layer" {
  s3_bucket          = aws_s3_bucket.elastic-book-store-bucket.bucket
  s3_key             = var.psycopg2_layer_key 
  layer_name         = "psycopg2_layer"
  compatible_runtimes = ["python3.9"]
  description        = "Layer containing the binaries for psycopg2"
}

resource "aws_lambda_layer_version" "postgres_utils_layer" {
  s3_bucket          = aws_s3_bucket.elastic-book-store-bucket.bucket
  s3_key             = var.postgres_utils_layer_key
  layer_name         = "postgres_utils_layer" 
  compatible_runtimes = ["python3.9"]
  description        = "Layer containing postgres CLI utilities"
}

############################
## Create Lambda Function ##
############################

resource "aws_s3_object" "lambda_code" {
  bucket = aws_s3_bucket.elastic-book-store-bucket.bucket
  key    = var.lambda_code_key
  source = var.lambda_code_source
}

resource "aws_lambda_function" "restore_dump" {
  filename         = aws_s3_bucket_object.lambda_code.id
  function_name    = "restore_dump"
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = var.lambda_runtime
  memory_size      = var.lambda_memory_size
  timeout          = var.lambda_timeout
  architectures    = ["x86_64"]
  publish          = true
  layers           = [aws_lambda_layer_version.psycopg2_layer.arn, aws_lambda_layer_version.postgres_utils_layer.arn]
  environment {
    variables = {
      DB_HOST   = ${aws_rds_cluster.ebook_store_db.endpoint}
      DB_NAME   = ${aws_rds_cluster.ebook_store_db.database_name}
      DB_PASSWORD = ${aws_rds_cluster.ebook_store_db.master_password}
      DB_PORT   = "5432"
      DB_USER   = ${aws_rds_cluster.ebook_store_db.master_username}
      S3_BUCKET = aws_s3_bucket.elastic-book-store-bucket.bucket
      S3_KEY    = var.dump_key
    }
  }
  vpc_config {
    security_group_ids = [aws_security_group.app_sg.id]
    subnet_ids         = [aws_subnet.ebook_store_public_subnet_web_1.id, aws_subnet.ebook_store_public_subnet_web_2.id, aws_subnet.ebook_store_private_subnet_application_1.id, aws_subnet.ebook_store_private_subnet_application_2.id]
  }
}