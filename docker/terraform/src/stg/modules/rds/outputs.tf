output "db_host" {
  value       = aws_rds_cluster.qumitoru-db.endpoint
  description = "DNS host name of the instance"
}

output "rds_proxy_endpoint" {
  value       = aws_db_proxy.main.endpoint
  description = "endpoint of the RDS Proxy"
}

output "aws_iam_role_rds_lambda_invoke_role_id" {
  value       = aws_iam_role.rds_lambda_invoke_role.id
  description = "role for lambda invoke"
}
