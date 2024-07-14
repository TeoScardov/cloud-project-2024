#!/bin/bash

EXCLUDE_RESOURCES=(
  "aws_route53_zone.ebook_store_zone"
  "aws_ecr_repository.react_app"
  "aws_ecr_repository.account_management"
  "aws_ecr_repository.product_catalog"
  "aws_ecr_repository.payment_service"
  "aws_ecr_repository.purchase_service"
  "aws_ecr_repository.shopping_cart"
  "aws_s3_bucket.ebook-store-tfstate"
)

cp terraform.tfstate terraform.tfstate.main.backup

for resource in "${EXCLUDE_RESOURCES[@]}"; do
  terraform state rm "$resource"
done

terraform destroy -auto-approve

for resource in "${EXCLUDE_RESOURCES[@]}"; do
  terraform state mv -state=terraform.tfstate.main.backup -state-out=terraform.tfstate $resource $resource
done