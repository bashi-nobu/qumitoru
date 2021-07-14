resource "aws_secretsmanager_secret" "db_auth" {
  name = "QT_DB_CONNECTION_INFO5_${var.env}"
}

resource "aws_secretsmanager_secret_version" "db_info" {
  secret_id = aws_secretsmanager_secret.db_auth.id

  secret_string = jsonencode({
    username: var.db_user
    password: var.db_password
    engine: aws_rds_cluster.qumitoru-db.engine
    host: aws_rds_cluster.qumitoru-db.endpoint
    port: aws_rds_cluster.qumitoru-db.port
    dbname: var.db_name
    dbInstanceIdentifier: aws_rds_cluster.qumitoru-db.id
  })
}
