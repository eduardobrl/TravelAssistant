import asyncio
import json

from app.services.secrets.secrets import load_secrets
from domain.constants import MessagesConstants
from services.telegram.telegram_client import TelegramClient

load_secrets()

def stream_handler(event, context):
    result = asyncio.run(async_stream_handler(event, context))
    
    return result

async def async_stream_handler(event, context):
    telegram = TelegramClient()
    
    print(json.dumps(event))
    
    for record in event['Records']:
        dynamodb_record = record["dynamodb"]

        partition_key = dynamodb_record["Keys"]["PartitionKey"]["S"]
        range_key = dynamodb_record["Keys"]["RangeKey"]["S"]

        if record["eventName"] in ["INSERT", "MODIFY"]:
            
            chat_id = partition_key.split("#")[-1]
            print(chat_id)
            if range_key == "ALLOWED":
                print(range_key)
                await telegram.send_message(chat_id=chat_id, text=MessagesConstants.ACCESS_ALOWED_MESSAGE)
                
    return MessagesConstants.OK_RESPONSE        