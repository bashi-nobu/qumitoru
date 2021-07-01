resource "aws_ecr_repository" "django-image" {
  name = "qumitoru-django-api"
}

resource "aws_ecr_repository" "nginx-image" {
  name = "qumitoru-nginx"
}

resource "aws_ecr_repository" "lambda-scanner-image" {
  name = "qumitoru-scanner"
}

resource "aws_ecr_repository" "lambda-ocr-cutout-image" {
  name = "qumitoru-ocr-cutout"
}

resource "aws_ecr_repository" "lambda-ocr-predict-image" {
  name = "qumitoru-ocr-predict"
}
