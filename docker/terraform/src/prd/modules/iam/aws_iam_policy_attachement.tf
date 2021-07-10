resource "aws_iam_role_policy_attachment" "ecs_instance_role_attach" {
  role = "${aws_iam_role.ecs_instance_role.name}"
  policy_arn = "${aws_iam_policy.ecs_instance_policy.arn}"
}

resource "aws_iam_role_policy_attachment" "ecs_task_role_attach" {
  role = aws_iam_role.ecs_task_role.name
  policy_arn = aws_iam_policy.ecs_task_policy.arn
}

resource "aws_iam_role_policy_attachment" "lambda_role_attach" {
  role       = aws_iam_role.lambda_container_role.id
  policy_arn = aws_iam_policy.lambda_policy.arn
}

resource "aws_iam_role_policy_attachment" "gateway_logs" {
  role       = aws_iam_role.iam_for_api_gateway.id
  policy_arn = aws_iam_policy.api_gateway_logging.arn
}

resource "aws_iam_role_policy_attachment" "rds_proxy_role_attach" {
  role       = aws_iam_role.rds_proxy_role.id
  policy_arn = aws_iam_policy.rds_proxy_policy.arn
}
