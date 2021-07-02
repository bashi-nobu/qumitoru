resource "aws_lb" "lb" {
  name               = "qumitoru-lb-${var.env}"
  internal           = false
  load_balancer_type = "application"

  security_groups = [
	var.aws_security_group_alb_id,
  ]

  subnets = [
    var.public_subnet_1_id,
    var.public_subnet_2_id,
  ]
}
