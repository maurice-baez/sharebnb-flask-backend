import os
import boto3

print(os.environ)
access = os.environ['ACCESS_KEY']
secret = os.environ['SECRET_ACCESS_KEY']

s3 = boto3.client(
  "s3",
  "us-west-1",
  aws_access_key_id=access,
  aws_secret_access_key=secret,
)

s3.upload_file("bg.jpg", "sharebnb", "bg.jpg", 
  ExtraArgs={"ContentType" : "image/jpeg"})