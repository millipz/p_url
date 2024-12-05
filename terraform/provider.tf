terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "p-url-tf-backend"
    region = "eu-west-2"
    key    = "backend.tfstate"
  }
}

provider "aws" {
  region = "eu-west-2"
  default_tags {
    tags = {
      ProjectName   = var.project_name
      Team          = "MJP"
      DeployedFrom  = "Terraform"
      Repository    = "https://github.com/millipz/p_url"
      CostCentre    = "slushfund"
      Environment   = "dev"
      RetentionDate = "2025-01-31"
    }
  }
}
