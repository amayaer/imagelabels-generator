# AWS Image Label Generator
 
A Python pipeline that uploads images to Amazon S3, uses Amazon
Rekognition to detect objects/labels, and renders the results as
bounding boxes on the original image. Infrastructure (S3 bucket,
IAM role/policies) is provisioned with Terraform.
 
## Architecture
1. Image is uploaded to an S3 bucket
2. Amazon Rekognition's detect_labels API analyzes the stored image
3. IAM handles authentication between the CLI/SDK and AWS services
4. Python (boto3) parses the label + bounding box response
5. Matplotlib renders bounding boxes over the original image
   
<img width="650" height="390" alt="imagelabelsgenerator_diagram" src="https://github.com/user-attachments/assets/34a948d1-fd34-4c95-a850-8c227ef85251" />

 
## Tech Stack
- Python 3.12
- boto3 (AWS SDK)
- Amazon S3, Amazon Rekognition, IAM
- Terraform (infrastructure provisioning)
- Pillow (PIL), matplotlib

## Project Structure
```
imagelabels-generator/
├── app/
│   └── main.py          
│   └── requirements.txt         
├── terraform/
│   ├── main.tf           
│   └── outputs.tf        
└── .gitignore
```
 
## Setup
1. Clone the repo
2. Provision infrastructure with Terraform:
   `cd terraform;
   terraform init;
   terraform apply`
3. Create a virtual environment: `python -m venv venv`
4. Install dependencies: `pip install -r requirements.txt`
5. Configure AWS CLI: `aws configure`
6. Set your bucket name in main.py (using the value from step 2) — or via env variable
 
## Example Output
<img width="470" height="360" alt="Figure_1" src="https://github.com/user-attachments/assets/0de5e802-8af0-4d0d-ae3b-4db4ffbed961" />



 
