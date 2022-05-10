import os
from dotenv import load_dotenv

load_dotenv()

import boto3

ACCESS = os.environ['ACCESS_KEY']
SECRET = os.environ['ACCESS_SECRET_KEY']
BUCKET = os.environ['BUCKET']

s3 = boto3.client(
  "s3",
  "us-west-1",
  aws_access_key_id=ACCESS,
  aws_secret_access_key=SECRET,
)

s3.upload_file("img.jpg", BUCKET, "img.jpg",
  ExtraArgs={"ContentType" : "image/jpeg"})