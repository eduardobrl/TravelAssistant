import json
import boto3
from botocore.exceptions import ClientError
from pydantic import BaseModel


class Secrets(BaseModel):
    TELEGRAM_BOT_TOKEN: str
    OPENAI_API_KEY: str
    CALENDAR_ID: str
    
loaded_secrets: Secrets = None
   
def load_secrets() -> Secrets:
    global loaded_secrets
    
    secret_name = "travelassistant/secrets"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    
    secretString = get_secret_value_response['SecretString']
    
    secret_dict = json.loads(secretString)

    loaded_secrets = Secrets(**secret_dict)
    
    return loaded_secrets
    
def get_secrets() -> Secrets:
    global loaded_secrets
    return loaded_secrets