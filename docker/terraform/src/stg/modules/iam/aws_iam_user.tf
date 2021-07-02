resource "aws_iam_user" "deploy-user" {
  name = "deploy-user-${var.env}"
}
