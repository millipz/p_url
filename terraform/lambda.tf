resource "aws_lambda_function" "backend_lambda" {
  function_name    = "${var.project_name}-backend"
  role             = aws_iam_role.backend_lambda_role.arn
  handler          = "main.lambda_handler"
  runtime          = "python3.11"
  filename         = data.archive_file.backend_lambda_package.output_path
  layers           = [aws_lambda_layer_version.lambda_layer.arn]
  timeout          = 180
  source_code_hash = filebase64sha256(data.archive_file.backend_lambda_package.output_path)

  # Optional environment variables
  environment {
    variables = {
      ENVIRONMENT = var.environment
      # Add other environment-specific variables here
    }
  }
}

resource "aws_lambda_layer_version" "lambda_layer" {
  layer_name               = "${var.project_name}-lambda-layer"
  filename                 = data.archive_file.lambda_layer_package.output_path
  compatible_runtimes      = ["python3.11"]
  compatible_architectures = ["x86_64"]
  source_code_hash         = filebase64sha256(data.archive_file.lambda_layer_package.output_path)
}

# Archive data sources for Lambda packaging
data "archive_file" "backend_lambda_package" {
  type             = "zip"
  source_dir       = "${path.module}/../backend/src"
  output_path      = "${path.module}/../build/backend_lambda.zip"
  output_file_mode = "0666"
}

data "archive_file" "lambda_layer_package" {
  type             = "zip"
  source_dir       = "${path.module}/../build/layer"
  output_path      = "${path.module}/../build/backend_layer.zip"
  output_file_mode = "0666"
}