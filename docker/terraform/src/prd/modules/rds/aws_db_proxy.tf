resource "aws_db_proxy" "main" {
  name = "qumitoru"
  engine_family = "MYSQL"
  role_arn = var.aws_iam_role_rds_proxy_role_arn
  vpc_security_group_ids = [var.aws_security_group_rds_proxy_id]
  vpc_subnet_ids = [var.private_subnet_1_id, var.private_subnet_2_id]

  auth {
    secret_arn = aws_secretsmanager_secret.db_auth.arn
  }
}

resource "aws_db_proxy_default_target_group" "main" {
  db_proxy_name = aws_db_proxy.main.name
}

resource "aws_db_proxy_target" "main" {
  db_cluster_identifier = aws_rds_cluster.qumitoru-db.id
  db_proxy_name = aws_db_proxy.main.name
  target_group_name = "default"
}

resource "aws_ssm_parameter" "db_hostname" {
  name = "DB_HOSTNAME"
  type = "SecureString"
  value = aws_db_proxy.main.endpoint
}
