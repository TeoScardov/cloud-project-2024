resource "aws_cloudwatch_log_group" "ebook-store-cloudwatch" {
  name              = "/aws/ecs/ebook-store"
  retention_in_days = 90

  tags = {
    Name = "ebook-store-cloudwatch"
    Terraform = "true"
  }

}