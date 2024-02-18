import asyncio
import json
import logging
import requests
import boto3
from domain.constants import MessagesConstants
from services.openai.openai_client import OpenAiClient
from services.repositories.chat_repository import ChatRepository, ChatRole
from services.telegram.requests.update_chat import Update
from services.telegram.telegram_client import TelegramClient


def lambda_handler(event, context):
    # Use asyncio.run to synchronously "await" an async function
    result = asyncio.run(async_lambda_handler(event, context))
    
    return result     

async def async_lambda_handler(event, context):
    telegram = TelegramClient()
    openai = OpenAiClient()
    repository = ChatRepository()
    s3 = boto3.client('s3')
    
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
        "body": data
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
    
    if update.message.document is not None:
        
        if update.message.document.file_size > 2e7:
            logging.error(MessagesConstants.MESSAGE_TOO_LARGE)
            
            return MessagesConstants.MESSAGE_TOO_LARGE

        file = await telegram.get_file(update.message.document.file_id)
        
        logging.info({
            "statusCode": 200,
            "message": "resposta get file",
            "body": file,
            }
        )
        
        if not file["ok"]:
            logging.error({
                "message": "Erro ao obter arquivo"
                }
            )
            return MessagesConstants.OK_RESPONSE
            
        
        response = requests.get(file["result"]["file_path"])
        
        logging.info({
            "message": "arquivo lido"
            }
        )
        
        s3.put_object(
            Body=response.content, 
            Bucket='travel-assistant-documents', 
            Key=update.message.document.file_name + update.message.document.file_id
        )
        
        logging.info({
            "message": "realizado o put do arquivo"
            }
        )
        return MessagesConstants.OK_RESPONSE
    
    chat_history = repository.get_messages(update.message.chat.id)
       
    response = openai.ask(update.message.text, chat_history)
    
    repository.add_message(update.message.chat.id, ChatRole.USER, update.message.text)
    repository.add_message(update.message.chat.id, ChatRole.ASSISTANT, response)

    response = await telegram.send_message(chat_id=update.message.chat.id, text=response)
    
    logging.info({"message": "Message response", "body": json.dumps(response)})
    
    print(json.dumps(event))

    return MessagesConstants.OK_RESPONSE
