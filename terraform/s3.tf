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
