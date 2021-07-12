resource "aws_iam_instance_profile" "ecs_instance_profile" {
  name = "ecs-instance-profile-qumitoru-${var.env}"
  role = "${aws_iam_role.ecs_instance_role.name}"
}
