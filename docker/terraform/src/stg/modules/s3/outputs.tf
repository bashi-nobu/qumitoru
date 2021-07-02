output "bucket_name" {
  value = "${aws_s3_bucket.of_ecs_s3.id}"
}
