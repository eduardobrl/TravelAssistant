class MessagesConstants:
    NOT_AUTHORIZED_MESSAGE = """
Olá ! Tudo bem ?
Este bot está em fase de testes e você ainda não está autorizado a utilizar.

A sua solicitação já foi enviada e caso aprovada você será informado. 
                """
                
    ACCESS_ALOWED_MESSAGE = """
Parabéns ! Você está autorizado a utilizar o bot.
Este permite que você tenha acesso ao seu calendario e planeje os seus próximos eventos.

Você pode perguntar por exemplo:

*Qual meu próximo evento ?*

Ou

*Quando será minha próxima viagem internacional ?*
"""

    MESSAGE_TOO_LARGE = """Me desculpe, mas não posso ler arquivos com mais de 20MB."""
                
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