# Terraform Infrastructure as Code (IaC)
# 3-Tier Highly Available Cloud Architecture for Educational Platform
# Educational Cloud Networking and Management Lab (ICTE 4342)

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# 1. Main Virtual Private Cloud (VPC)
resource "aws_vpc" "edu_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "EduCloud-Production-VPC"
    Environment = "Academic-Lab"
    Project     = "Cloud-Classroom"
  }
}

# 2. Internet Gateway for Public Tier
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.edu_vpc.id

  tags = {
    Name = "EduCloud-IGW"
  }
}

# 3. Public Web Subnets (Multi-AZ)
resource "aws_subnet" "public_subnet_1" {
  vpc_id                  = aws_vpc.edu_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "Public-Web-Subnet-1a"
    Tier = "Public"
  }
}

resource "aws_subnet" "public_subnet_2" {
  vpc_id                  = aws_vpc.edu_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true

  tags = {
    Name = "Public-Web-Subnet-1b"
    Tier = "Public"
  }
}

# 4. Private Application Subnets (Multi-AZ)
resource "aws_subnet" "private_app_subnet_1" {
  vpc_id            = aws_vpc.edu_vpc.id
  cidr_block        = "10.0.10.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "Private-App-Subnet-1a"
    Tier = "Private-App"
  }
}

# 5. Isolated Database Subnets (Multi-AZ)
resource "aws_subnet" "private_db_subnet_1" {
  vpc_id            = aws_vpc.edu_vpc.id
  cidr_block        = "10.0.20.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "Isolated-DB-Subnet-1a"
    Tier = "Private-Database"
  }
}

# 6. Security Group for Web Load Balancer
resource "aws_security_group" "alb_sg" {
  name        = "edu-alb-sg"
  description = "Allow inbound HTTPS and HTTP traffic from Internet"
  vpc_id      = aws_vpc.edu_vpc.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
