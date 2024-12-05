resource "aws_cloudwatch_log_group" "backend_lambda_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.backend_lambda.function_name}"
  retention_in_days = 14
}

resource "aws_cloudwatch_log_group" "api_gateway_logs" {
  name              = "/aws/apigateway/${var.project_name}-access-logs"
  retention_in_days = 14
}