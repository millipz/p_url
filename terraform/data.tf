data "archive_file" "backend_lambda_package" {
  type        = "zip"
  source_dir = "${path.module}/../backend/src"
  output_path = "${path.module}/../build/backend_lambda.zip"
  output_file_mode = "0666"
}

data "archive_file" "lambda_layer_package" {
  type        = "zip"
  source_dir = "${path.module}/../build/layer"
  output_path = "${path.module}/../build/backend_layer.zip"
  output_file_mode = "0666"
}