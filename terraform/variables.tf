variable "aws_region" {
  description = "AWS region on which we will setup our network cluster"
}

variable "user" {
  type    = "string"
  default = "ec2-user"
}

variable "aws_access_key" {
	description = "AWS IAM public key"
}

variable "aws_secret_key" {
	description = "AWS IAM private key"
}

variable "aws_ami" {
  description = "Amazon Linux AMI"
}

variable "instance_type" {
  description = "Instance type"
}

variable "instance_type_a1" {
  description = "Instance type"
}

variable "public_key_path" {
  description = "SSH public key path"
}

variable "private_key_path" {
  description = "SSH private key path"
}

variable "bootstrap_path" {
  description = "Script to install bootstrap environment"
  default = "bootstrap.sh"
}



