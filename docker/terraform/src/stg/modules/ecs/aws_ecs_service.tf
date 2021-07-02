resource "aws_ecs_service" "webapp-service" {
  name            = "qumitoru-service-${var.env}"
  cluster         = "${aws_ecs_cluster.qumitoru-ecs-cluster.id}"
  task_definition = "${aws_ecs_task_definition.qumitoru-task.arn}"
  desired_count   = 1 # スケーリングに合わせて調整
  launch_type     = "FARGATE"

  load_balancer {
    target_group_arn = aws_lb_target_group.http.arn
    container_name   = "nginx"
    container_port   = "80"
  }

  network_configuration {
    subnets = [
      var.public_subnet_1_id,
      var.public_subnet_2_id,
    ]
    security_groups = [
      var.aws_security_group_instance_id
    ]
    assign_public_ip = true
  }

  lifecycle {
    ignore_changes = [
      "desired_count",
      "task_definition",
      "load_balancer",
    ]
  }
}

resource "aws_ecs_service" "webapp-migration" {
  name            = "qumitoru-migration-${var.env}"
  cluster         = "${aws_ecs_cluster.qumitoru-ecs-cluster.id}"
  task_definition = "${aws_ecs_task_definition.qumitoru-migration-task.arn}"
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets = [
      var.public_subnet_1_id,
      var.public_subnet_2_id,
    ]
    security_groups = [
      var.aws_security_group_instance_id
    ]
    assign_public_ip = true
  }
}

resource "aws_ecs_service" "webapp-createuser" {
  name            = "qumitoru-createuser-${var.env}"
  cluster         = "${aws_ecs_cluster.qumitoru-ecs-cluster.id}"
  task_definition = "${aws_ecs_task_definition.qumitoru-createuser-task.arn}"
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets = [
      var.public_subnet_1_id,
      var.public_subnet_2_id,
    ]
    security_groups = [
      var.aws_security_group_instance_id
    ]
    assign_public_ip = true
  }
}
