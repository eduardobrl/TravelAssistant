import json
import os
import boto3
from services.generators.embedings_generator import generate_embeddings
from services.parsers.pdf_parser import PdfParser
from services.repositories.embeddings_repository import EmbeddingRepository
from services.usecases.upload_files import S3Uploader

# import requests
pdf_parser = PdfParser()
s3_uploader = S3Uploader()
repository = EmbeddingRepository()
s3 = boto3.client('s3')

file_path = os.environ.get("FILE_PATH")

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    try:
        local_file_path = file_path + key 
        s3.download_file(bucket, key, local_file_path)
        
        results = pdf_parser.parse_file(local_file_path)
        embeddings = generate_embeddings(results)
        repository.insert_embedding(embeddings)

        print('File {} downloaded from {} bucket'.format(key, bucket))

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e


    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
        }),
    }
