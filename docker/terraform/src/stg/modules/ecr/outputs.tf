output "django-image-url" {
  value = "${aws_ecr_repository.django-image.repository_url}"
}

output "nginx-image-url" {
  value = "${aws_ecr_repository.nginx-image.repository_url}"
}

output "lambda-scanner-image-url" {
  value = "${aws_ecr_repository.lambda-scanner-image.repository_url}"
}

output "lambda-ocr-cutout-image-url" {
  value = "${aws_ecr_repository.lambda-ocr-cutout-image.repository_url}"
}

output "lambda-ocr-predict-image-url" {
  value = "${aws_ecr_repository.lambda-ocr-predict-image.repository_url}"
}
