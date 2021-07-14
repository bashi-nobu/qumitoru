# parameter group
resource "aws_rds_cluster_parameter_group" "main" {
  name        = "rds-cluster-pg"
  family      = "aurora-mysql5.7"
  description = "RDS default cluster parameter group"

  parameter {
    name  = "character_set_database"
    value = "utf8mb4"
    apply_method = "immediate"
  }

  parameter {
    name  = "character_set_server"
    value = "utf8mb4"
    apply_method = "immediate"
  }

  parameter {
    name         = "time_zone"
    value        = "Asia/Tokyo"
    apply_method = "immediate"
  }

  parameter {
    name         = "aws_default_lambda_role"
    value        = aws_iam_role.rds_lambda_invoke_role.arn
    apply_method = "immediate"
  }
}

resource "aws_db_parameter_group" "main" {
  name   = "qumitoru-tf-${var.env}-aurora-mysql57"
  family = "aurora-mysql5.7"
}
