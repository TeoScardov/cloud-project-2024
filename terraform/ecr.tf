resource "aws_ecr_repository" "react_app" {
    name = "react_app"
    image_tag_mutability = "MUTABLE"  
}

resource "aws_ecr_repository" "account_management" {
    name = "account_management"
    image_tag_mutability = "MUTABLE"  
}

resource "aws_ecr_repository" "payment_service" {
    name = "payment_service"
    image_tag_mutability = "MUTABLE"  
}

resource "aws_ecr_repository" "purchase_service" {
    name = "purchase_service"
    image_tag_mutability = "MUTABLE"  
}

resource "aws_ecr_repository" "product_catalog" {
    name = "product_catalog"
    image_tag_mutability = "MUTABLE"  
}

resource "aws_ecr_repository" "shopping_cart" {
    name = "shopping_cart"
    image_tag_mutability = "MUTABLE"  
}