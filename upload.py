import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import uuid

load_dotenv()

import boto3

ACCESS = os.environ['ACCESS_KEY']
SECRET = os.environ['ACCESS_SECRET_KEY']
BUCKET = os.environ['BUCKET']

def upload_to_aws(file):

  s3 = boto3.client(
    "s3",
    "us-west-1",
    aws_access_key_id=ACCESS,
    aws_secret_access_key=SECRET,
  )

  img_id = str(uuid.uuid4())
  object_name = img_id + "/" + secure_filename(file.filename)
  img_type = file.mimetype

  ## upload_file_obj
  s3.upload_fileobj(file, BUCKET, object_name,
    ExtraArgs={"ContentType" : img_type})

  objURL = "https://" + BUCKET + ".s3.us-west-1.amazonaws.com/" + object_name
  
  return (objURL)

