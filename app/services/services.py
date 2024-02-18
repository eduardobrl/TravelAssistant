import boto3
import os

class Services:
    
    @staticmethod
    def DynamoDbClient():
        return boto3.client('dynamodb')
    
    @staticmethod
    def GetTableName():
        return os.environ.get('TABLE_NAME')