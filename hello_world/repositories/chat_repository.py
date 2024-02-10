from ulid import ULID
import boto3
import os

class ChatRepository:
    
    def __init__(self) -> None:
        self.client = boto3.client('dynamodb')
        self.TABLE_NAME = os.environ.get('TABLE_NAME')
        
    
    def is_chat_allowed(self, chat_id):
        response = self.client.get_item(
            TableName=self.TABLE_NAME,
            Key={
                'PartitionKey': {
                    'S': f"CHAT#{chat_id}"
                    },
                    'RangeKey': {
                        'S': 'ALLOWED'
                    },
                }
            )
        return True if 'Item' in response else False
        
    def add_message(self, chat_id, role, message):
        
        ulid = ULID()
        response = self.client.put_item(
            TableName=self.TABLE_NAME,
            Key={
                    'PartitionKey': {
                        'S': f"CHAT#{chat_id}"
                    },
                    'RangeKey': {
                        'S': f'MESSSAGE#{ulid}'
                    },
                    'role': {
                        'S': role
                    },
                    'content': {
                        'S': message
                    }
                }
            )

    def get_messages(self, chat_id):
        response = self.client.query(
            TableName=self.TABLE_NAME,
            KeyConditionExpression='PartitionKey = :pk and begins_with(RangeKey, :rk)', 
            ExpressionAttributeValues={
                ':pk': {'S': f'CHAT#{chat_id}'},
                ':rk': {'S': 'MESSAGE'}
            }
        )
        
        items = response['Items']
        
        for item in items:
            message_role = item['role']['S']
            message_content = item['content']['S']
        