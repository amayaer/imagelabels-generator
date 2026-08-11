import os, boto3
from botocore.exceptions import ClientError 
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

FILE_PATH = "your-image-path-here"
BUCKET_NAME = "your-bucket-name-here"
IMAGE_KEY = f"sample_images/{os.path.basename(FILE_PATH)}"


def upload_image(file_path, bucket_name, key):
    s3 = boto3.client('s3')

    try: 
        s3.upload_file(file_path, bucket_name, key)
        print(f"Successfully uploaded {file_path} to {bucket_name}/{key}")
    except ClientError as e: 
        print(f"Credential or permission error: {e}")
    except FileNotFoundError:
        print("The local file was not found")


def detect_labels(bucket, key, file_path):    
    rekognition = boto3.client('rekognition', region_name='us-east-1')
    img = Image.open(file_path)

    response = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': bucket, 'Name': key,}},
        MaxLabels=10,
        MinConfidence=75.0,
    )

    if not response['Labels']:
        print(f"No labels were detected for '{key}'. Try a different image or lower the confidence threshold.")
        return

    fig, ax = plt.subplots()
    fig.patch.set_facecolor('black')   
    ax.set_facecolor('black')             
    ax.tick_params(colors='white')        
    ax.imshow(img)

    scene_only_labels = []

    for label in response['Labels']:
        label_text = label['Name']

        if not label['Instances']: 
            scene_only_labels.append(label_text)
            continue

        for instance in label['Instances']:
            box = instance['BoundingBox']
            top_px = box['Top'] * img.height
            left_px = box['Left'] * img.width
            width_px = (box['Width'] * img.width)
            height_px = (box['Height'] * img.height)

            
            box_dict = {
                'Label': label_text, 
                'Box': ((left_px, top_px), width_px, height_px),
                'Confidence': (f" {instance['Confidence']:.2f}%")
            }   
    
            print(f"Bounding box info: \n {box_dict}\n")
            rect = patches.Rectangle((left_px, top_px),height_px,height_px,linewidth=2, edgecolor='red', facecolor='none')
            ax.add_patch(rect)

            ax.text(left_px, top_px - 5, box_dict['Label'] + box_dict['Confidence'], color='black', fontsize=8,  bbox=dict(facecolor='white', alpha=1, edgecolor='yellow', pad=0.5))

    if scene_only_labels:
        print(f"Scene-level labels (no bounding box): {', '.join(scene_only_labels)}\n")

    if len(scene_only_labels) == len(response['Labels']):
        print("No object-level labels with bounding boxes were found to display.")
    else: 
        plt.show()


if __name__ == "__main__":
    upload_image(FILE_PATH, BUCKET_NAME, IMAGE_KEY)
    detect_labels(BUCKET_NAME, IMAGE_KEY, FILE_PATH)