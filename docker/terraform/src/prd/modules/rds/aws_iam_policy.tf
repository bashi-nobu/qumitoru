resource "aws_iam_role" "rds_lambda_invoke_role" {
  name = "rds-lambda-invoke-role"
  path = "/"
  assume_role_policy = file("./modules/iam/aws_iam_role_policies/rds_assume_role.json")
}
