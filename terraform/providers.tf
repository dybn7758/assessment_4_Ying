provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "assess_ying"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}