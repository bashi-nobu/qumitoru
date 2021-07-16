terraform {
  backend "s3" {
    bucket = "qumitoru-tf"
    key    = "src/stg/terraform.tfstate"
    region = "ap-northeast-1"
  }
}

provider "aws" {
  region = "ap-northeast-1"
}

module "vpc" {
  source   = "./modules/vpc"
  env      = "stg"
}

module "s3" {
  source   = "./modules/s3"
  env      = "stg"
}

module "iam" {
  source   = "./modules/iam"
  env      = "stg"
}

module "rds" {
  source   = "./modules/rds"
  env      = "stg"
  db_name  = var.db_name
  db_user  = var.db_user
  db_password  = var.db_password
  db_sg_id = module.vpc.aws_security_group_db_id
  db_subnet_group_name = module.vpc.aws_db_subnet_group_main_name
  private_subnet_1_id = module.vpc.private_subnet_1_id
  private_subnet_2_id = module.vpc.private_subnet_2_id
  lambda_container_role_arn = module.iam.lambda_container_role_arn
  aws_iam_role_rds_proxy_role_arn = module.iam.aws_iam_role_rds_proxy_role_arn
  aws_security_group_rds_proxy_id = module.vpc.aws_security_group_rds_proxy_id
}

module "lambda" {
  source   = "./modules/lambda"
  env      = "stg"
  lambda_container_role_arn = module.iam.lambda_container_role_arn
  aws_iam_role_iam_for_api_gateway_arn = module.iam.aws_iam_role_iam_for_api_gateway_arn
  db_host  = module.rds.db_host
  db_name  = var.db_name
  db_user  = var.db_user
  db_password  = var.db_password
  rds_proxy_endpoint = module.rds.rds_proxy_endpoint
  bucket_name = module.s3.bucket_name
  lambda-scanner-image-url = module.ecr.lambda-scanner-image-url
  lambda-ocr-cutout-image-url = module.ecr.lambda-ocr-cutout-image-url
  lambda-ocr-predict-image-url = module.ecr.lambda-ocr-predict-image-url
  aws_security_group_lambda_id = module.vpc.aws_security_group_lambda_id
  private_subnet_1_id = module.vpc.private_subnet_1_id
  private_subnet_2_id = module.vpc.private_subnet_2_id
  aws_vpc_endpoint_lambda_dns = module.vpc.aws_vpc_endpoint_lambda_dns
  aws_vpc_endpoint_api_gateway_id = module.vpc.aws_vpc_endpoint_api_gateway_id
  aws_iam_role_rds_lambda_invoke_role_id = module.rds.aws_iam_role_rds_lambda_invoke_role_id
}

module "ecr" {
  source   = "./modules/ecr"
}

module "ecs" {
  source   = "./modules/ecs"
  env      = "stg"
  ecs_task_role_arn = module.iam.ecs_task_role_arn
  ecs_instance_profile_name = module.iam.ecs_instance_profile_name
  vpc_id = module.vpc.vpc_id
  public_subnet_1_id = module.vpc.public_subnet_1_id
  public_subnet_2_id = module.vpc.public_subnet_2_id
  aws_security_group_alb_id = module.vpc.aws_security_group_alb_id
  aws_security_group_instance_id = module.vpc.aws_security_group_instance_id
  bucket_name = module.s3.bucket_name
  db_host  = module.rds.db_host
  db_name  = var.db_name
  db_user  = var.db_user
  db_password  = var.db_password
  django-image-url = module.ecr.django-image-url
  nginx-image-url = module.ecr.nginx-image-url
  scanner_api_url = module.lambda.scanner_api_url
  scanner_api_key = module.lambda.scanner_api_key
}



# terraform init -target=module.<module name>
# terraform plan -target=module.<module name>
# terraform apply -target=module.<module name>
# terraform destroy -target=module.<module name>
