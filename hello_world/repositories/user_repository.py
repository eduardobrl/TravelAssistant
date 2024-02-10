from flask import cli
import boto3
import os

class UserRepository:
    
    def __init__(self) -> None:
        self.client = boto3.client('dynamodb')
        self.TABLE_NAME = os.environ.get('TABLE_NAME')
        
    
    def is_chat_allowed(self, chat_id):
        response = self.client.get_item(
            TableName='chat_allowed',
            Key={
                'user_id': {
                    'S': f"CHAT#{chat_id}"
                    }
                }
            )
        return True if 'Item' in response else False
        