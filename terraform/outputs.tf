output "vpc_id" {
  description = "ID of the Assessment IV VPC"
  value       = aws_vpc.main.id
}

output "eks_cluster_name" {
  description = "Name of the EKS cluster"
  value       = aws_eks_cluster.main.name
}

output "eks_cluster_endpoint" {
  description = "Endpoint for the EKS control plane"
  value       = aws_eks_cluster.main.endpoint
}

output "private_subnet_ids" {
  description = "Private subnet IDs used by EKS worker nodes"

  value = [
    aws_subnet.private_1.id,
    aws_subnet.private_2.id
  ]
}

output "public_subnet_ids" {
  description = "Public subnet IDs"

  value = [
    aws_subnet.public_1.id,
    aws_subnet.public_2.id
  ]
}

output "ecr_repository_urls" {
  description = "ECR repository URLs"

  value = {
    for name, repository in aws_ecr_repository.services :
    name => repository.repository_url
  }
}