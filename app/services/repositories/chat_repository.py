from pydantic import BaseModel
from ulid import ULID
import boto3
import os

class ChatRole:
    USER="user"
    SYSTEM="system"
    ASSISTANT="assistant"
    
class ChatMessage(BaseModel):
    role: str
    content: str
    
class ChatMessages(BaseModel):
    messages: list[ChatMessage]


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
    
    def is_chat_requested(self, chat_id):
        response = self.client.get_item(
            TableName=self.TABLE_NAME,
            Key={
                'PartitionKey': {
                    'S': f"CHAT#{chat_id}"
                    },
                    'RangeKey': {
                        'S': 'REQUESTED'
                    },
                }
            )
        return True if 'Item' in response else False
    
    def add_chat_access_requested(self, chat_id):
        response = self.client.put_item(
            TableName=self.TABLE_NAME,
            Item={
                'PartitionKey': {
                    'S': f"CHAT#{chat_id}"
                    },
                    'RangeKey': {
                        'S': 'REQUESTED'
                    },
                }
            )
        return response
        
    def add_message(self, chat_id, role, message):
        
        ulid = ULID()
        self.client.put_item(
            TableName=self.TABLE_NAME,
            Item={
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
                },
            )

    def get_messages(self, chat_id) -> ChatMessages:
        response = self.client.query(
            TableName=self.TABLE_NAME,
            KeyConditionExpression='PartitionKey = :pk and begins_with(RangeKey, :rk)', 
            ExpressionAttributeValues={
                ':pk': {'S': f'CHAT#{chat_id}'},
                ':rk': {'S': 'MESSSAGE'}
            },
            ScanIndexForward= False,
            Limit=2
        )
        
        if 'Items' not in response:
            return None
        
        items = response['Items']
        
        if items is None or response['Count'] == 0:
            return None
        
        chat_messages = []
        items.reverse()
        
        for item in items:
            message_role = item['role']['S']
            message_content = item['content']['S']
            
            chat_messages.append(ChatMessage(role=message_role, content=message_content))
        
        return ChatMessages(messages=chat_messages)