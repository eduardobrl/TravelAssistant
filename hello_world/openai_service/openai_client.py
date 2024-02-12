from openai import OpenAI

from repositories.chat_repository import ChatMessages

class OpenAiClient:

    def __init__(self) -> None:
        self.client = OpenAI()
        self.SYSTEM_PROMPT = """
            Você é um bot assistente de viagens. 
            Que ajuda usuários através do telegram a planejarem suas viagens.
        
        """
        
    def ask(self, question, history:ChatMessages = None) -> str:
        messages=[
            {"role": "system", "content": self.SYSTEM_PROMPT} ]
        
        if history is not None:
            messages.extend(history.messages)
        
        messages.append({"role": "user", "content": question})
        
        completions =  self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            # tools= [
            #     {
            #         "type":"function",
            #         "function":{}
            #     }
            # ]
        )
        
        return completions.choices[0].message.content