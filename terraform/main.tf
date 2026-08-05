terraform {
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

resource "aws_iam_user" "rekognition_user" {
    name = "image-labels-generator-user"
    tags = {
        Project = "ImageLabelsGenerator"
    }
}

resource "aws_iam_access_key" "rekognition_user_key" {
    user = aws_iam_user.rekognition_user.name
}

resource "aws_iam_user_policy_attachment" "s3_access" {
    user = aws_iam_user.rekognition_user.name
    policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}