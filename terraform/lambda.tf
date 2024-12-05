resource "aws_lambda_function" "backend_lambda" {
    function_name = "${var.project_name}-backend"
    role = aws_iam_role.backend_lambda_role.arn
    handler = "main.lambda_handler"
    runtime = "python3.12"
    filename = data.archive_file.backend_lambda_package.output_path
    layers = [aws_lambda_layer_version.lambda_layer.arn]
    timeout = 180
    source_code_hash = "${filebase64sha256(data.archive_file.backend_lambda_package.output_path)}"
    environment {
        variables = {
        }
    }
}

resource "aws_lambda_layer_version" "lambda_layer" {
    layer_name = "${var.project_name}-lambda-layer"
    filename = data.archive_file.lambda_layer_package.output_path
    compatible_runtimes = ["python3.12"]
    compatible_architectures = ["x86_64"]
    source_code_hash = "${filebase64sha256(data.archive_file.lambda_layer_package.output_path)}"
}