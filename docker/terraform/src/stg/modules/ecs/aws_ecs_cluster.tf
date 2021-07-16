resource "aws_ecs_cluster" "qumitoru-ecs-cluster" {
  name = "qumitoru-ecs-cluster-${var.env}"
}
