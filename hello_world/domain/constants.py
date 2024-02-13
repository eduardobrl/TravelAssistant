class MessagesConstants:
    NOT_AUTHORIZED_MESSAGE = """
Olá ! Tudo bem ?
Este bot está em fase de testes e você ainda não está autorizado a utilizar.

A sua solicitação já foi enviada e caso aprovada você será informado. 
                """
                
    OK_RESPONSE_NOT_ALLOWED = {
                "statusCode": 200,
                "body": "Chat not allowed"
            }
    
    OK_INVALID_REQUEST = {
            "statusCode": 404,
            "body": "Invalid request"
        }
    
    OK_RESPONSE = {
                "statusCode": 200,
            }