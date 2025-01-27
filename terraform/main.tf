terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

# Provider configuration
provider "aws" {
  region  = "ap-south-1"
  profile = "personal-iam" # Or your profile name
}

# Key pair for SSH access
resource "aws_key_pair" "ec2_key" {
  key_name   = "my-key-pair" # Replace with your desired key name
  public_key = file("~/.ssh/id_rsa.pub") # Path to your public key
}

# Data block to fetch the default VPC
data "aws_vpc" "default" {
  default = true
}

# Security group to allow SSH and HTTP access
resource "aws_security_group" "ec2_sg" {
  name        = "my-ec2-sg"
  description = "Allow SSH and HTTP access"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "Allow SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Replace with specific CIDR if needed
  }

  ingress {
    description = "Allow HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Replace with specific CIDR if needed
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "MyEC2SecurityGroup"
  }
}

# EC2 instance
resource "aws_instance" "web_server" {
  ami           = "ami-00bb6a80f01f03502" # Replace with a valid AMI ID
  instance_type = "t2.micro"
  key_name      = aws_key_pair.ec2_key.key_name
  subnet_id     = "subnet-09d003c65b4701d03"
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  tags = {
    Name = "MyEC2Instance"
  }
}

# Output the public IP of the instance
output "instance_public_ip" {
  value = aws_instance.web_server.public_ip
}
