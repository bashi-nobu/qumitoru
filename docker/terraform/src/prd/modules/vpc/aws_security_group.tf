resource "aws_security_group" "instance" {
  name        = "instance"
  description = "instance sg"
  vpc_id      = aws_vpc.vpc.id

  ingress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"

    security_groups = [
      "${aws_security_group.alb.id}",
    ]
  }

  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port = 22
    to_port = 22
    protocol = "TCP"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "alb" {
  name        = "qumitoru-webapp-alb-${var.env}"
  description = "http and https"
  vpc_id      = aws_vpc.vpc.id

  ingress {
    from_port = 80
    to_port   = 80
    protocol  = "TCP"

    cidr_blocks = [
      "0.0.0.0/0",
    ]
  }

  ingress {
    from_port = 443
    to_port   = 443
    protocol  = "TCP"

    cidr_blocks = [
      "0.0.0.0/0",
    ]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}


resource "aws_security_group" "lambda" {
  name        = "lambda-security-group"
  description = "lambda security group"
  vpc_id      = aws_vpc.vpc.id

  ingress {
    from_port = 0
    to_port = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 443
    to_port   = 443
    protocol  = "TCP"

    cidr_blocks = [
      "0.0.0.0/0",
    ]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "rds_proxy" {
  name        = "rds-proxy-security-grout"
  description = "rds proxy security group"
  vpc_id      = aws_vpc.vpc.id

  ingress {
    from_port = 3306
    to_port = 3306
    protocol = "tcp"
    security_groups = [aws_security_group.lambda.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "db" {
  name        = "qumitoru-db-${var.env}"
  description = "DB"
  vpc_id      = aws_vpc.vpc.id

  ingress {
    from_port = 3306
    to_port   = 3306
    protocol  = "tcp"

    security_groups = [
      aws_security_group.instance.id,
      aws_security_group.rds_proxy.id
    ]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
