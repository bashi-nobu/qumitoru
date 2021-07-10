resource "aws_iam_role" "ecs_instance_role" {
  name               = "ecs_instance_role-qumitoru-${var.env}"
  path               = "/"
  assume_role_policy = "${file("./modules/iam/aws_iam_role_policies/ec2_assume_role_policy.json")}"
}

resource "aws_iam_role" "ecs_task_role" {
  name               = "ecs-task-role-qumitoru-${var.env}"
  path               = "/"
  assume_role_policy = file("./modules/iam/aws_iam_role_policies/ecs_task_assume_role_policy.json")
}

resource "aws_iam_role" "lambda_container_role" {
  name               = "lambda-container-role-qumitoru-${var.env}"
  path               = "/"
  assume_role_policy = file("./modules/iam/aws_iam_role_policies/lambda_assume_role_policy.json")
}

resource "aws_iam_role" "iam_for_api_gateway" {
  name = "api-gateway-role-qumitoru-${var.env}"
  description = "custom IAM Limited Role created with \"APIGateway\" as the trusted entity"
  path = "/"
  assume_role_policy = file("./modules/iam/aws_iam_role_policies/api_gateway_assume_role_policy.json")
}

resource "aws_iam_role" "rds_proxy_role" {
  name = "rds-proxy-role-qumitoru-${var.env}"
  path = "/"
  assume_role_policy = file("./modules/iam/aws_iam_role_policies/rds_proxy_assume_role.json")
}
