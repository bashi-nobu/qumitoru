# RDSの作成
resource "aws_rds_cluster" "qumitoru-db" {
  cluster_identifier_prefix = "qumitoru-${var.env}"
  engine                    = "aurora-mysql"
  engine_version            = "5.7.mysql_aurora.2.08.2"
  master_username           = var.db_user
  master_password           = var.db_password
  database_name             = var.db_name
  backup_retention_period   = 30
  storage_encrypted         = true
  port                      = "3306"
  vpc_security_group_ids    = [var.db_sg_id]
  db_subnet_group_name      = var.db_subnet_group_name
  db_cluster_parameter_group_name = aws_rds_cluster_parameter_group.main.name
  iam_roles                 = [aws_iam_role.rds_lambda_invoke_role.arn]
  skip_final_snapshot       = "true"
}

resource "aws_rds_cluster_instance" "qumitoru-db-instance" {
  count                   = 1
  identifier              = "qumitoru-tf-${var.env}-${count.index}"
  cluster_identifier      = aws_rds_cluster.qumitoru-db.cluster_identifier
  db_subnet_group_name    = var.db_subnet_group_name
  db_parameter_group_name = aws_db_parameter_group.main.name
  engine                  = "aurora-mysql"
  engine_version          = "5.7.mysql_aurora.2.08.2"
  instance_class          = "db.t3.small"
  apply_immediately       = true
  publicly_accessible     = true
}
