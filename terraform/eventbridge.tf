resource "aws_cloudwatch_log_group" "backend_lambda_log_group" {
  name = "/aws/lambda/${aws_lambda_function.backend_lambda.function_name}"
}