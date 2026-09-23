variable "aws_region" {
  description = "AWS region for Assessment IV"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used for AWS resource naming"
  type        = string
  default     = "assessment-4-ying"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "assessment4-ying-eks"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "key_pair_name" {
  description = "Existing EC2 key pair used for SSH access to EC2/EKS nodes"
  type        = string
}