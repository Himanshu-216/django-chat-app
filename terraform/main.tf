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
  region = "us-east-1" # Replace with your desired region
}

# Key pair for SSH access
resource "aws_key_pair" "ec2_key" {
  key_name   = "my-key-pair" # Replace with your desired key name
  public_key = file("~/.ssh/id_rsa.pub") # Path to your public key
}

# Security group to allow SSH and HTTP access
resource "aws_security_group" "ec2_sg" {
  name_prefix = "ec2-sg-"

  ingress {
    from_port   = 22
    to_port     = 22
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

# EC2 instance
resource "aws_instance" "web_server" {
  ami           = "ami-04b4f1a9cf54c11d0" # Replace with a valid AMI ID
  instance_type = "t2.micro"
  key_name      = aws_key_pair.ec2_key.key_name
  security_groups = [aws_security_group.ec2_sg.name]

  tags = {
    Name = "MyEC2Instance"
  }
}

# Output the public IP of the instance
output "instance_public_ip" {
  value = aws_instance.web_server.public_ip
}
