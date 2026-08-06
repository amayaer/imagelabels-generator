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

resource "aws_iam_user_policy_attachment" "rekognition_access" {
    user = aws_iam_user.rekognition_user.name
    policy_arn = "arn:aws:iam::aws:policy/AmazonRekognitionReadOnlyAccess"
}

resource "aws_s3_bucket" "image_bucket" {
    bucket_prefix = "image-labels-generator-bucket-"
}

resource "aws_s3_bucket_public_access_block" "image_bucket" {
    bucket = aws_s3_bucket.image_bucket.id

    block_public_acls   = true
    block_public_policy = true
    ignore_public_acls =  true
    restrict_public_buckets = true
}