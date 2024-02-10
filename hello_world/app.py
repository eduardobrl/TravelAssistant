import json
from telegram.requests.update_chat import Update
from telegram.telegram_client import TelegramClient

async def lambda_handler(event, context):
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
    
    request_context = event.get("requestContext")
    if request_context is None:
        return {
            "statusCode": 404,
            "body": "Invalid request"
        }
        
    body = request_context.get("body")
    if body is None:
        return {
            "statusCode": 404,
            "body": "Invalid request"
        }
    
    data = json.loads(body)
    update = Update.model_validate(data)
    
    client = TelegramClient()
    
    
    await client.send_message(chat_id=update.message.chat.id, text=update.message.text)
    
    print(json.dumps(event))

    return {
        "statusCode": 200,
        "body": json.dumps(event),
    }
