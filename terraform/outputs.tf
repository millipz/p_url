output "lambda_function_name" {
  description = "The name of the Lambda function"
  value       = aws_lambda_function.backend_lambda.function_name
}

output "api_gateway_invoke_url" {
  description = "The invoke URL for the API Gateway"
  value       = aws_api_gateway_stage.dev.invoke_url
}

output "lambda_function_arn" {
  description = "The ARN of the Lambda function"
  value       = aws_lambda_function.backend_lambda.arn
}