resource "aws_iam_policy" "deploy" {
  name        = "deploy-${var.env}"
  path        = "/"
  description = "deploy policy"
  policy      = "${file("./modules/iam/aws_iam_policies/ecr_policy.json")}"
}

resource "aws_iam_policy" "ecs_instance_policy" {
  name        = "ecs-instance-policy-${var.env}"
  path        = "/"
  description = ""
  policy      = "${file("./modules/iam/aws_iam_policies/ecs_instance_policy.json")}"
}

resource "aws_iam_policy" "ecs_task_policy" {
  name        = "ecs-task-policy-${var.env}"
  path        = "/"
  description = ""
  policy      = file("./modules/iam/aws_iam_policies/ecs_task_policy.json")
}

resource "aws_iam_policy" "lambda_policy" {
  name        = "lambda-policy-${var.env}"
  path        = "/"
  description = ""
  policy      = file("./modules/iam/aws_iam_policies/lambda_policy.json")
}

resource "aws_iam_policy" "api_gateway_logging" {
  name        = "api-gateway-logging-policy-${var.env}"
  path        = "/"
  description = "IAM policy for logging from the api gateway"
  policy      = file("./modules/iam/aws_iam_policies/api_gateway_policy.json")
}

resource "aws_iam_policy" "rds_proxy_policy" {
  name        = "rds-proxy-policy"
  path        = "/"
  description = ""
  policy      = file("./modules/iam/aws_iam_policies/rds_proxy_policy.json")
}

