# resource "aws_s3_bucket" "books_images" {
#   bucket = "books-images"
  
# }

# resource "aws_s3_bucket" "books_files" {
#   bucket = "books-files"
  
# }

resource "aws_s3_bucket" "ebook-store-tfstate" {
  bucket = "ebook-store-tfstate"

}

# resource "aws_s3_bucket_policy" "books_files_policy" {
#   bucket = aws_s3_bucket.books_files.bucket
#   policy = data.aws_s3_bucket_policy_document.books_files_policy.json
# }

# resource "aws_s3_bucket_policy" "github_actions_policy" {
#   bucket = aws_s3_bucket.github_actions.bucket
#   policy = data.aws_s3_bucket_policy_document.github_actions_policy.json
# }

# data "aws_s3_bucket_policy_document" "books_files_policy" {
#     statement {
#         Effect = "Allow"
#         Principal = {"AWS": ecs_task_execution_role.arn}
#         Actions = ["s3:GetObject"]
#         Resources = [aws_s3_bucket.books_files.arn]
#     }
# }

# data "aws_s3_bucket_policy_document" "github_actions_policy" {
#     statement {
#         Effect = "Allow"
#         Principal = {"AWS": github_s3_access_role.arn}
#         Actions = ["s3:GetObject",
#                    "s3:PutObject"]
#         Resources = [aws_s3_bucket.books_files.arn]
#     }
# }

resource "aws_s3_bucket" "elastic-book-store-bucket" {
  bucket = "elastic-book-store-bucket"

}

resource "aws_s3_object" "postgres_dump" {
  bucket = aws_s3_bucket.elastic-book-store-bucket.bucket
  key    = var.dump_key
  source = "${path.module}/../data/flask_db.dump"
}

resource "aws_s3_object" "lambda_code" {
  bucket = aws_s3_bucket.elastic-book-store-bucket.bucket
  key    = var.lambda_code_key
  source = "${path.module}/../cloud/lambda_function.zip"
}

resource "aws_s3_object" "psycopg2_layer" {
  bucket = aws_s3_bucket.elastic-book-store-bucket.bucket
  key    = var.psycopg2_layer_key
  source = "${path.module}/../cloud/psycopg2_layer.zip"
}

resource "aws_s3_object" "postgres_utils_layer" {
  bucket = aws_s3_bucket.elastic-book-store-bucket.bucket
  key    = var.postgres_utils_layer_key
  source = "${path.module}/../cloud/pg_client_tools_layer.zip"
}