########################
## Autoscaling Target ##
########################

resource "aws_appautoscaling_target" "web-scaling-tg" {
  max_capacity = 5
  min_capacity = 1
  resource_id = "service/${aws_ecs_cluster.ecs_cluster.name}/${aws_ecs_service.ecs_web_service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace = "ecs"
}

resource "aws_appautoscaling_target" "account-scaling-tg" {
  max_capacity = 5
  min_capacity = 1
  resource_id = "service/${aws_ecs_cluster.ecs_cluster.name}/${aws_ecs_service.ecs_account_service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace = "ecs"
}

resource "aws_appautoscaling_target" "payment-scaling-tg" {
  max_capacity = 5
  min_capacity = 1
  resource_id = "service/${aws_ecs_cluster.ecs_cluster.name}/${aws_ecs_service.ecs_payment_service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace = "ecs"
}

resource "aws_appautoscaling_target" "purchase-scaling-tg" {
  max_capacity = 5
  min_capacity = 1
  resource_id = "service/${aws_ecs_cluster.ecs_cluster.name}/${aws_ecs_service.ecs_purchase_service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace = "ecs"
}   

resource "aws_appautoscaling_target" "product-scaling-tg" {
  max_capacity = 5
  min_capacity = 1
  resource_id = "service/${aws_ecs_cluster.ecs_cluster.name}/${aws_ecs_service.ecs_product_service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace = "ecs"
}

resource "aws_appautoscaling_target" "cart-scaling-tg" {
  max_capacity = 5
  min_capacity = 1
  resource_id = "service/${aws_ecs_cluster.ecs_cluster.name}/${aws_ecs_service.ecs_cart_service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace = "ecs"
}

########################
## Autoscaling Policy ##
########################

resource "aws_appautoscaling_policy" "web-scaling-policy" {
  name               = "web-scaling-policy"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.web-scaling-tg.resource_id
  scalable_dimension = aws_appautoscaling_target.web-scaling-tg.scalable_dimension
  service_namespace  = aws_appautoscaling_target.web-scaling-tg.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }

    target_value = 60.0
  }
}

resource "aws_appautoscaling_policy" "account-scaling-policy" {
  name               = "account-scaling-policy"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.account-scaling-tg.resource_id
  scalable_dimension = aws_appautoscaling_target.account-scaling-tg.scalable_dimension
  service_namespace  = aws_appautoscaling_target.account-scaling-tg.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }

    target_value = 60.0
  }
}

resource "aws_appautoscaling_policy" "payment-scaling-policy" {
  name               = "payment-scaling-policy"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.payment-scaling-tg.resource_id
  scalable_dimension = aws_appautoscaling_target.payment-scaling-tg.scalable_dimension
  service_namespace  = aws_appautoscaling_target.payment-scaling-tg.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }

    target_value = 60.0
  }
}

resource "aws_appautoscaling_policy" "purchase-scaling-policy" {
  name               = "purchase-scaling-policy"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.purchase-scaling-tg.resource_id
  scalable_dimension = aws_appautoscaling_target.purchase-scaling-tg.scalable_dimension
  service_namespace  = aws_appautoscaling_target.purchase-scaling-tg.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }

    target_value = 60.0
  }
}

resource "aws_appautoscaling_policy" "product-scaling-policy" {
  name               = "product-scaling-policy"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.product-scaling-tg.resource_id
  scalable_dimension = aws_appautoscaling_target.product-scaling-tg.scalable_dimension
  service_namespace  = aws_appautoscaling_target.product-scaling-tg.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }

    target_value = 60.0
  }
}

resource "aws_appautoscaling_policy" "cart-scaling-policy" {
  name               = "cart-scaling-policy"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.cart-scaling-tg.resource_id
  scalable_dimension = aws_appautoscaling_target.cart-scaling-tg.scalable_dimension
  service_namespace  = aws_appautoscaling_target.cart-scaling-tg.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }

    target_value = 60.0
  }
}