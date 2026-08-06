output "access_key_id" {
    value = aws_iam_access_key.rekognition_user_key.id
}

output "secret_access_key" {
    value = aws_iam_access_key.rekognition_user_key.secret
    sensitive = true
}

output "bucket_name" {
    value = aws_s3_bucket.image_bucket.bucket
}

output "bucket_arn" {
    value = aws_s3_bucket.image_bucket.arn
}