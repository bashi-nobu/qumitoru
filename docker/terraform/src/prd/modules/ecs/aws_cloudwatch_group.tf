resource "aws_cloudwatch_log_group" "qumitoru-service" {
  name = "qumitoru-service-${var.env}"
}
