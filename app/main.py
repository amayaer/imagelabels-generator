import os, boto3
from botocore.exceptions import ClientError 

file_path = "/Users/amayasmacbook/Downloads/family_picture.png"
bucket_name = "image-labels-generator-bucket-20260806004057421200000001"
key = f"uploads/{os.path.basename(file_path)}"


def upload_image(file_path, bucket_name, key):
    s3 = boto3.client('s3')

    try: 
        s3.upload_file(file_path, bucket_name, key)
        print(f"Successfully uploaded {file_path} to {bucket_name}/{key}")
    except ClientError as e: 
        print(f"Credential or permission error: {e}")
    except FileNotFoundError:
        print("The local file was not found")

def detect_labels(bucket, key):    
    rekognition = boto3.client('rekognition', region_name='us-east-1')

    response = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': bucket, 'Name': key,}},
        MaxLabels=10,
        MinConfidence=75.0,
    )

    print(f"Detected labels for {key}\n")
    for label in response['Labels']:
        print(f"Label: {label['Name']} | Confidence: {label['Confidence']:.2f}%")


if __name__ == "__main__":
    upload_image(file_path, bucket_name, key)
    detect_labels(bucket_name, key)