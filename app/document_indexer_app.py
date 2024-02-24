import json
import boto3
from app.services.secrets.secrets import load_secrets
from services.generators.embedings_generator import generate_embeddings
from services.parsers.pdf_parser import PdfParser
from services.repositories.embeddings_repository import EmbeddingRepository
from services.usecases.upload_files import S3Uploader

# import requests
pdf_parser = PdfParser()
s3_uploader = S3Uploader()
repository = EmbeddingRepository()
s3 = boto3.client('s3')
load_secrets()

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    try:
        local_file_path = '/tmp/' + key 
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


if __name__ == "__main__":  
    s3_uploader.upload("Booking_Confirmation.pdf")
    results = pdf_parser.parse_file("Booking_Confirmation.pdf")
    embeddings = generate_embeddings(results)
    
    repository.insert_embedding(embeddings)
    
    