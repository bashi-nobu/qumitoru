resource "aws_iam_policy" "rds_lambda_invoke_policy" {
  name        = "rds-lambda-invoke-policy"
  path        = "/"
  description = ""
  policy      = templatefile("./modules/iam/aws_iam_policies/rds_lambda_policy.json", {
    invoke_lambda_arn = aws_lambda_function.lambda_cutout_container.arn
    })
}

resource "aws_iam_role_policy_attachment" "rds_lambda_invoke_role_attach" {
  role       = var.aws_iam_role_rds_lambda_invoke_role_id
  policy_arn = aws_iam_policy.rds_lambda_invoke_policy.arn
}
