data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "backend_lambda_role" {
  name               = "backend-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

data "aws_iam_policy_document" "backend_lambda_policy" {
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["arn:aws:logs:*:*:*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "ssm:PutParameter",
      "ssm:GetParameter",
      "ssm:GetParameters",
      "ssm:GetParametersByPath"
    ]
    resources = ["arn:aws:ssm:*:*:parameter/*"]
  }
}

resource "aws_iam_policy" "backend_lambda_policy" {
  name        = "backend-lambda-policy"
  description = "IAM policy for backend Lambda function"
  policy      = data.aws_iam_policy_document.backend_lambda_policy.json
}

resource "aws_iam_role_policy_attachment" "backend_lambda_policy_attachment" {
  role       = aws_iam_role.backend_lambda_role.name
  policy_arn = aws_iam_policy.backend_lambda_policy.arn
}