# resource "aws_acm_certificate" "api_cert" {
#   domain_name       = "p-url.me"
#   validation_method = "DNS"
# }

# resource "aws_api_gateway_domain_name" "api_domain" {
#   domain_name              = "p-url.me"
#   regional_certificate_arn = aws_acm_certificate.api_cert.arn

#   endpoint_configuration {
#     types = ["REGIONAL"]
#   }
# }

# resource "aws_api_gateway_base_path_mapping" "api_mapping" {
#   api_id      = aws_api_gateway_rest_api.api.id
#   stage_name  = aws_api_gateway_stage.api_test_stage.stage_name
#   domain_name = aws_api_gateway_domain_name.api_domain.domain_name
# }