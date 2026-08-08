import os, boto3
from botocore.exceptions import ClientError 
from PIL import Image, ImageDraw

file_path = "/Users/amayasmacbook/Downloads/family_picture.png"
bucket_name = "image-labels-generator-bucket-20260806004057421200000001"
key = f"uploads/{os.path.basename(file_path)}"
img = Image.open(file_path)
img_width, img_height = img.size


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
    draw = ImageDraw.Draw(img)
    box_dict = {}

    response = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': bucket, 'Name': key,}},
        MaxLabels=10,
        MinConfidence=75.0,
    )

    print(f"\nDetected labels for {key}\n")
    for label in response['Labels']:
        label_text = label['Name']
        for instance in label['Instances']:
            box = instance['BoundingBox']
            top_px = box['Top'] * img_height
            left_px = box['Left'] * img_width
            right_px = left_px + (box['Width'] * img_width)
            bottom_px = top_px + (box['Height'] * img_height)

            
            box_dict = {
                'Label': label_text,
                'Box': (left_px, top_px, right_px, bottom_px),
                'Confidence': (f"Confidence: {instance['Confidence']:.2f}%")
            }   
    
            #print(f"Bounding box info: \n {box_dict}\n")
            draw.rectangle(box_dict['Box'], fill=None, outline="black", width=3)
        if not label['Instances']: 
            print(f"No bounding box detected for label '{label_text}'.\n")

    img.show() 

if __name__ == "__main__":
    #upload_image(file_path, bucket_name, key)
    detect_labels(bucket_name, key)