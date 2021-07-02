resource "aws_ecs_task_definition" "qumitoru-task" {
  family                = "qumitoru-service-${var.env}"
  container_definitions = templatefile("./modules/ecs/container_definitions/service.json",{
    env = var.env,
    lb_dns_name = aws_lb.lb.dns_name,
    bucket_name = var.bucket_name,
    db_host = var.db_host,
    db_name = var.db_name,
    db_user = var.db_user,
    db_password = var.db_password,
    scanner_api_url = var.scanner_api_url,
    scanner_api_key = var.scanner_api_key,
    django-image-url = var.django-image-url,
    nginx-image-url = var.nginx-image-url
    })

  task_role_arn            = var.ecs_task_role_arn
  execution_role_arn       = var.ecs_task_role_arn
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 512
  memory                   = 1024
}

resource "aws_ecs_task_definition" "qumitoru-migration-task" {
  family                = "qumitoru-migration-${var.env}"
  container_definitions = templatefile("./modules/ecs/container_definitions/migration.json", {
    env = var.env
    lb_dns_name = aws_lb.lb.dns_name,
    bucket_name = var.bucket_name,
    db_host = var.db_host,
    db_name = var.db_name,
    db_user = var.db_user,
    db_password = var.db_password
    django-image-url = var.django-image-url
    })

  task_role_arn            = var.ecs_task_role_arn
  execution_role_arn       = var.ecs_task_role_arn
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 512
  memory                   = 1024
}

resource "aws_ecs_task_definition" "qumitoru-createuser-task" {
  family                = "qumitoru-createuser-${var.env}"
  container_definitions = templatefile("./modules/ecs/container_definitions/create_superuser.json", {
    env = var.env
    lb_dns_name = aws_lb.lb.dns_name,
    bucket_name = var.bucket_name,
    db_host = var.db_host,
    db_name = var.db_name,
    db_user = var.db_user,
    db_password = var.db_password
    django-image-url = var.django-image-url
    })

  task_role_arn            = var.ecs_task_role_arn
  execution_role_arn       = var.ecs_task_role_arn
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 512
  memory                   = 1024
}
