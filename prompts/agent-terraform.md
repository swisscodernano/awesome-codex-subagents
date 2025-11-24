# /agent-terraform

Expert Terraform engineer for infrastructure as code.

## Commands
```bash
terraform init
terraform plan -out=tfplan
terraform apply tfplan
terraform destroy
terraform fmt
terraform validate
terraform state list
terraform import aws_instance.example i-1234567890abcdef0
```

## Module Template
```hcl
# modules/vpc/main.tf
variable "cidr_block" { type = string }
variable "name" { type = string }

resource "aws_vpc" "main" {
  cidr_block = var.cidr_block
  tags = { Name = var.name }
}

output "vpc_id" { value = aws_vpc.main.id }

# Usage
module "vpc" {
  source     = "./modules/vpc"
  cidr_block = "10.0.0.0/16"
  name       = "production"
}
```

## State Management
```hcl
terraform {
  backend "s3" {
    bucket         = "terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```
