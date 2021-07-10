# S3バケットの作成
resource "aws_s3_bucket" "of_ecs_s3" {
  bucket = "qumitoru-${var.env}"
  acl    = "private"
}
