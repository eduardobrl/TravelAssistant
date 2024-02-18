import asyncio
import json
import logging
from domain.constants import MessagesConstants
from services.openai.openai_client import OpenAiClient
from services.repositories.chat_repository import ChatRepository, ChatRole
from services.telegram.requests.update_chat import Update
from services.telegram.telegram_client import TelegramClient


def lambda_handler(event, context):
    # Use asyncio.run to synchronously "await" an async function
    result = asyncio.run(async_lambda_handler(event, context))
    
    return result

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
        

async def async_lambda_handler(event, context):
    telegram = TelegramClient()
    openai = OpenAiClient()
    repository = ChatRepository()
    
    body = event.get("body")
    if body is None:
        return MessagesConstants.OK_INVALID_REQUEST
        
    logging.info({
        "message": "Body Data",
        "body": json.dumps(body)
    })
    
    data = json.loads(body)
    
    logging.info({
        "message": "data Loads",
        "body": json.dumps(data)
    })
    
    update = Update.model_validate(data)
    
    
    if not repository.is_chat_allowed(update.message.chat.id):
        if repository.is_chat_requested(update.message.chat.id):
            return MessagesConstants.OK_RESPONSE_NOT_ALLOWED
        
        repository.add_chat_access_requested(update.message.chat.id)
        await telegram.send_message(
            chat_id=update.message.chat.id, 
            text=MessagesConstants.NOT_AUTHORIZED_MESSAGE
        )
        
        return MessagesConstants.OK_RESPONSE_NOT_ALLOWED
    
    logging.info({"message": "Model validated"})
    
    chat_history = repository.get_messages(update.message.chat.id)
       
    response = openai.ask(update.message.text, chat_history)
    
    repository.add_message(update.message.chat.id, ChatRole.USER, update.message.text)
    repository.add_message(update.message.chat.id, ChatRole.ASSISTANT, response)

    response = await telegram.send_message(chat_id=update.message.chat.id, text=response)
    
    logging.info({"message": "Message response", "body": json.dumps(response)})
    
    print(json.dumps(event))

    return MessagesConstants.OK_RESPONSE
