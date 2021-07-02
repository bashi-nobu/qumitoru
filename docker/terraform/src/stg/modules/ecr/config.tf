terraform {
  backend "s3" {
    bucket = "qumitoru-tf"
    key    = "src/ecr/terraform.tfstate"
    region = "ap-northeast-1"
  }
}

provider "aws" {
  region = "ap-northeast-1"
}
