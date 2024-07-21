resource "aws_cloudwatch_log_group" "ebook_store_cloudwatch" {
  name              = var.cloudwatch_group
  tags = {
    Name = "ebook-store-cloudwatch"
    Terraform = "true"
  }

}