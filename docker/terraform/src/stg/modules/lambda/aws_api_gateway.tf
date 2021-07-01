# API GATE WAY (CutOut Lmabda)
resource "aws_cloudwatch_log_group" "api_gateway_scanner_log_group" {
  name              = "/aws/lambda/${var.env}-scanner-api-gateway"
  retention_in_days = 14
}

resource "aws_api_gateway_rest_api" "lambda_scanner" {
  name        = "lambda_scanner"
  description = "lambda_scanner API Gateway"

    policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "execute-api:Invoke",
            "Resource": [
                "*"
            ]
        },
        {
            "Effect": "Deny",
            "Principal": "*",
            "Action": "execute-api:Invoke",
            "Resource": [
                "*"
            ],
            "Condition" : {
                "StringNotEquals": {
                    "aws:SourceVpce": "${var.aws_vpc_endpoint_api_gateway_id}"
                }
            }
        }
    ]
}
EOF

  endpoint_configuration {
    types = ["PRIVATE"]
    vpc_endpoint_ids = [var.aws_vpc_endpoint_api_gateway_id]
  }
}

resource "aws_api_gateway_resource" "lambda_scanner_container" {
  rest_api_id = aws_api_gateway_rest_api.lambda_scanner.id
  parent_id   = aws_api_gateway_rest_api.lambda_scanner.root_resource_id
  path_part   = "lambda_scanner_container"
}

resource "aws_api_gateway_method" "lambda_scanner_container" {
  rest_api_id      = aws_api_gateway_rest_api.lambda_scanner.id
  resource_id      = aws_api_gateway_resource.lambda_scanner_container.id
  http_method      = "POST"
  authorization    = "NONE"
  api_key_required = true
}

resource "aws_api_gateway_method_response" "lambda_scanner_container" {
  rest_api_id = aws_api_gateway_rest_api.lambda_scanner.id
  resource_id = aws_api_gateway_resource.lambda_scanner_container.id
  http_method = aws_api_gateway_method.lambda_scanner_container.http_method
  status_code = "200"
  response_models = {
    "application/json" = "Empty"
  }
  depends_on = [aws_api_gateway_method.lambda_scanner_container]
}

resource "aws_api_gateway_integration" "lambda_scanner_container" {
  rest_api_id             = aws_api_gateway_rest_api.lambda_scanner.id
  resource_id             = aws_api_gateway_resource.lambda_scanner_container.id
  http_method             = aws_api_gateway_method.lambda_scanner_container.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.lambda_scanner_container.invoke_arn}"
}

resource "aws_api_gateway_account" "main" {
  cloudwatch_role_arn = var.aws_iam_role_iam_for_api_gateway_arn
}

resource "aws_api_gateway_deployment" "lambda_scanner" {
  rest_api_id       = aws_api_gateway_rest_api.lambda_scanner.id
  stage_name        = "lambda_scanner"
  stage_description = "timestamp = ${timestamp()}"

  depends_on = [
		aws_cloudwatch_log_group.api_gateway_scanner_log_group,
    aws_api_gateway_integration.lambda_scanner_container,
		aws_api_gateway_account.main
  ]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_method_settings" "lambda_scanner" {
  rest_api_id = aws_api_gateway_rest_api.lambda_scanner.id
  stage_name  = aws_api_gateway_deployment.lambda_scanner.stage_name
  method_path = "*/*"

  settings {
    data_trace_enabled = true
	  metrics_enabled    = true
    logging_level      = "INFO"
  }
}

resource "aws_lambda_permission" "lambda_scanner_container" {
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.lambda_scanner_container.function_name}"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.lambda_scanner.execution_arn}/*/${aws_api_gateway_method.lambda_scanner_container.http_method}/${aws_api_gateway_resource.lambda_scanner_container.path_part}"
}

resource "aws_api_gateway_api_key" "lambda_scanner" {
  name    = "lambda_scanner_api_key"
  enabled = true
}

resource "aws_api_gateway_usage_plan" "lambda_scanner" {
  name       = "lambda_scanner_usage_plan"
  depends_on = [aws_api_gateway_deployment.lambda_scanner]

  api_stages {
    api_id = aws_api_gateway_rest_api.lambda_scanner.id
    stage  = aws_api_gateway_deployment.lambda_scanner.stage_name
  }
}

resource "aws_api_gateway_usage_plan_key" "lambda_scanner" {
  key_id        = aws_api_gateway_api_key.lambda_scanner.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.lambda_scanner.id
}

# API GATE WAY (Predict Lmabda)
resource "aws_cloudwatch_log_group" "api_gateway_predict_log_group" {
  name              = "/aws/lambda/${var.env}-predict-api-gateway"
  retention_in_days = 14
}

resource "aws_api_gateway_rest_api" "lambda_predict" {
  name        = "lambda_predict"
  description = "lambda_predict API Gateway"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "execute-api:Invoke",
            "Resource": [
                "*"
            ]
        },
        {
            "Effect": "Deny",
            "Principal": "*",
            "Action": "execute-api:Invoke",
            "Resource": [
                "*"
            ],
            "Condition" : {
                "StringNotEquals": {
                    "aws:SourceVpce": "${var.aws_vpc_endpoint_api_gateway_id}"
                }
            }
        }
    ]
}
EOF

  endpoint_configuration {
    types = ["PRIVATE"]
    vpc_endpoint_ids = [var.aws_vpc_endpoint_api_gateway_id]
  }
}

resource "aws_api_gateway_resource" "lambda_predict_container" {
  rest_api_id = aws_api_gateway_rest_api.lambda_predict.id
  parent_id   = aws_api_gateway_rest_api.lambda_predict.root_resource_id
  path_part   = "lambda_predict_container"
}

resource "aws_api_gateway_method" "lambda_predict_container" {
  rest_api_id      = aws_api_gateway_rest_api.lambda_predict.id
  resource_id      = aws_api_gateway_resource.lambda_predict_container.id
  http_method      = "POST"
  authorization    = "NONE"
  api_key_required = true
}

resource "aws_api_gateway_method_response" "lambda_predict_container" {
  rest_api_id = aws_api_gateway_rest_api.lambda_predict.id
  resource_id = aws_api_gateway_resource.lambda_predict_container.id
  http_method = aws_api_gateway_method.lambda_predict_container.http_method
  status_code = "200"
  response_models = {
    "application/json" = "Empty"
  }
  depends_on = [aws_api_gateway_method.lambda_predict_container]
}

resource "aws_api_gateway_integration" "lambda_predict_container" {
  rest_api_id             = aws_api_gateway_rest_api.lambda_predict.id
  resource_id             = aws_api_gateway_resource.lambda_predict_container.id
  http_method             = aws_api_gateway_method.lambda_predict_container.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "${aws_lambda_function.lambda_predict_container.invoke_arn}"
}

resource "aws_api_gateway_deployment" "lambda_predict" {
  rest_api_id       = aws_api_gateway_rest_api.lambda_predict.id
  stage_name        = "lambda_predict"
  stage_description = "timestamp = ${timestamp()}"

  depends_on = [
		aws_cloudwatch_log_group.api_gateway_scanner_log_group,
    aws_api_gateway_integration.lambda_predict_container,
		aws_api_gateway_account.main
  ]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_method_settings" "lambda_predict" {
  rest_api_id = aws_api_gateway_rest_api.lambda_predict.id
  stage_name  = aws_api_gateway_deployment.lambda_predict.stage_name
  method_path = "*/*"

  settings {
    data_trace_enabled = true
	  metrics_enabled    = true
    logging_level      = "INFO"
  }
}

resource "aws_lambda_permission" "lambda_predict_container" {
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.lambda_predict_container.function_name}"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.lambda_predict.execution_arn}/*/${aws_api_gateway_method.lambda_predict_container.http_method}/${aws_api_gateway_resource.lambda_predict_container.path_part}"
}

resource "aws_api_gateway_api_key" "lambda_predict" {
  name    = "lambda_predict_api_key"
  enabled = true
}

resource "aws_api_gateway_usage_plan" "lambda_predict" {
  name       = "lambda_predict_usage_plan"
  depends_on = [aws_api_gateway_deployment.lambda_predict]

  api_stages {
    api_id = aws_api_gateway_rest_api.lambda_predict.id
    stage  = aws_api_gateway_deployment.lambda_predict.stage_name
  }
}

resource "aws_api_gateway_usage_plan_key" "lambda_predict" {
  key_id        = aws_api_gateway_api_key.lambda_predict.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.lambda_predict.id
}
