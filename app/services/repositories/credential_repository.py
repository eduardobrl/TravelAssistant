import json
import boto3
from pydantic import BaseModel
from dynamodb_json import json_util as dynamodb_json

from services.services import Services

class UserInfo(BaseModel):
    client_id: str
    client_secret: str
    refresh_token: str
    expiry: str
    token: str
    token_uri: str
    universe_domain: str
    
 
class CredentialRepository:
    def __init__(self) -> None:
       self.client = boto3.client('dynamodb')
       self.table_name = Services.GetTableName()
    
    def get_user_info(self) -> UserInfo:
        response = self.client.get_item(
            TableName=self.table_name,
            Key={
                'PartitionKey': {
                    'S': "USER_INF0"
                    },
                    'RangeKey': {
                        'S': 'USER_INF0'
                    },
                }
            )
        
        dynamo_json = json.dumps(response['Item'])
        items = dynamodb_json.loads(dynamo_json)
        return UserInfo(**items)

    def update_credentials(self, data: UserInfo):
   
        item = {
            "PartitionKey": {
                "S": "USER_INF0"
            },
            "RangeKey": {
                "S": "USER_INF0"
            },
            "client_id": {
                "S": data.client_id
            },
            "client_secret": {
                "S": data.client_secret
            },
            "expiry": {
                "S": data.expiry
            },
            "refresh_token": {
                "S": data.refresh_token
            },
            "token": {
                "S": data.token
            },
            "token_uri": {
                "S": data.token_uri
            },
            "universe_domain": {
                "S": data.universe_domain
            }
       }
        self.client.put_item(
            TableName=self.table_name,
            Item=item,           
        )