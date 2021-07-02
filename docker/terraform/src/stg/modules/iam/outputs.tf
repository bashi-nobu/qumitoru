output "ecs_instance_profile_name" {
  value = "${aws_iam_instance_profile.ecs_instance_profile.name}"
}

output "ecs_task_role_arn" {
  value = aws_iam_role.ecs_task_role.arn
}

output "lambda_container_role_arn" {
  value = aws_iam_role.lambda_container_role.arn
}

output "aws_iam_role_iam_for_api_gateway_arn" {
  value = aws_iam_role.iam_for_api_gateway.arn
}

output "aws_iam_role_rds_proxy_role_arn" {
  value = aws_iam_role.rds_proxy_role.arn
}

