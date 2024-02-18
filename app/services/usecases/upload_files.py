import os
import string
from domain.file_entities import FileResult
import boto3
import secrets


class S3Uploader:
    def __init__(self) -> None:
        self.s3 = boto3.client('s3')
        self.bucket_name = os.environ.get('BUCKET_NAME')
    
    def upload(self, filename: str) -> None:
        output_file = filename.join(secrets.choice(string.ascii_uppercase + string.digits)
              for i in range(5))
        self.s3.upload_file("docs/" + filename, self.bucket_name, output_file)

        