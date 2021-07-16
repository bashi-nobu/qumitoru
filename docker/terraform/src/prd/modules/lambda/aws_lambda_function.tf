# lambda(scanner)_______________________________________________

resource "aws_lambda_function" "lambda_scanner_container" {
  function_name = "lambda_scanner_container_${var.env}"
  role          = var.lambda_container_role_arn
  package_type  = "Image"
  image_uri     = "${var.lambda-scanner-image-url}:latest"
  memory_size   = 3008
	timeout       = 120
  publish = true
  lifecycle {
    ignore_changes = [image_uri]
  }

  environment {
    variables = {
      BUCKET_NAME = var.bucket_name
      AWS_LAMBDA_EXEC_ENV = "production"
    }
  }
}

resource "aws_lambda_alias" "lambda_scanner" {
  name             = "scanner_alias_${var.env}"
  description      = "lambda scanner alias"
  function_name    = aws_lambda_function.lambda_scanner_container.function_name
  function_version = aws_lambda_function.lambda_scanner_container.version
}

resource "aws_lambda_provisioned_concurrency_config" "lambda_scanner_container" {
  function_name                     = aws_lambda_alias.lambda_scanner.function_name
  provisioned_concurrent_executions = 2
  qualifier                         = aws_lambda_alias.lambda_scanner.name
}

# lambda(cutout&predict)_______________________________________________

resource "aws_lambda_function" "lambda_predict_container" {
	function_name = "lambda_predict_container_${var.env}"
	role          = var.lambda_container_role_arn
	package_type  = "Image"
	image_uri     = "${var.lambda-ocr-predict-image-url}:latest"
	memory_size   = 3008
	timeout       = 120

	lifecycle {
		ignore_changes = [image_uri]
	}

	environment {
		variables = {
			BUCKET_NAME = var.bucket_name
      AWS_LAMBDA_EXEC_ENV = "production"
		}
	}
}

resource "aws_lambda_function" "lambda_cutout_container" {
	function_name = "lambda_cutout_container_${var.env}"
	role          = var.lambda_container_role_arn
	package_type  = "Image"
	image_uri     = "${var.lambda-ocr-cutout-image-url}:latest"
	memory_size   = 3008
	timeout       = 630

  vpc_config {
    subnet_ids         = [var.private_subnet_1_id, var.private_subnet_2_id]
    security_group_ids = [var.aws_security_group_lambda_id]
  }

	lifecycle {
		ignore_changes = [image_uri]
	}

	environment {
		variables = {
			DB_HOST = var.rds_proxy_endpoint
			DB_NAME = var.db_name
			DB_USER = var.db_user
			DB_PASS = var.db_password
			BUCKET_NAME = var.bucket_name
      AWS_LAMBDA_EXEC_ENV = "production"
      OCR_API_URL = "https://${aws_api_gateway_rest_api.lambda_predict.id}-${var.aws_vpc_endpoint_api_gateway_id}.execute-api.ap-northeast-1.amazonaws.com/${aws_api_gateway_rest_api.lambda_predict.name}/${aws_api_gateway_resource.lambda_predict_container.path_part}"
      OCR_API_KEY = aws_api_gateway_usage_plan_key.lambda_predict.value
    }
	}
}
