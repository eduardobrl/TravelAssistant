import asyncio
import json
from telegram.requests.update_chat import Update
from telegram.telegram_client import TelegramClient
import logging


def lambda_handler(event, context):
    # Use asyncio.run to synchronously "await" an async function
    result = asyncio.run(async_lambda_handler(event, context))
    
    return result


async def async_lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e
    
    body = event.get("body")
    if body is None:
        return {
            "statusCode": 404,
            "body": "Invalid request"
        }
        
        
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
    
    logging.info({"message": "Model validated"})
    
    client = TelegramClient()

    response = await client.send_message(chat_id=update.message.chat.id, text=update.message.text)
    
    logging.info({"message": "Message response", "body": json.dumps(response)})
    
    print(json.dumps(event))

    return {
        "statusCode": 200,
        "body": json.dumps(event),
    }
