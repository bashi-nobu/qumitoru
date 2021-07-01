output "scanner_api_url" {
  value = "https://${aws_api_gateway_rest_api.lambda_scanner.id}-${var.aws_vpc_endpoint_api_gateway_id}.execute-api.ap-northeast-1.amazonaws.com/${aws_api_gateway_rest_api.lambda_scanner.name}/${aws_api_gateway_resource.lambda_scanner_container.path_part}"
}

output "scanner_api_key" {
  value = "${aws_api_gateway_usage_plan_key.lambda_scanner.value}"
}
