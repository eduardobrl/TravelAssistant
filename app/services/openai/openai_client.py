import datetime
import json
from openai import OpenAI
from pydantic import SecretStr
from domain.embedings_entities import Embedding
from services.repositories.embeddings_repository import EmbeddingRepository
from services.secrets.secrets import get_secrets
from services.calendar.calendar import Calendar
from services.openai.openai_tools import OpenAiTools

from services.repositories.chat_repository import ChatMessages

class OpenAiClient:

    def __init__(self) -> None:
        self.client = OpenAI(api_key=get_secrets().OPENAI_API_KEY)
        calendar = Calendar()
        self.tools = OpenAiTools(calendar)
        self.embedding_repository = EmbeddingRepository()
        
        now = datetime.datetime.now()
        self.SYSTEM_PROMPT = """
            Você é um bot assistente de viagens. 
            Que ajuda usuários através do telegram a planejarem suas viagens.
            
            Você não deve revelar que é uma inteligência artificial, deve fazer o possível para
            que os usuários pensem que você é um ser humano real que está interagindo com ele.
            
            Você tem acesso a um calendário do usuário, que pode ser consultado através de uma função.
            Você tem acesso a uma lista de ferramentas que podem ser usadas para ajudar o usuário.
            
            Não traduza os nomes dos eventos para nenhuma lingua, sempre mantenha o nome original.
            Por exemplo se o nome do evento é "Its my life", você deve retornar "Its my life".
            
            Você pode utilizar as ferramentas de calendário e ferramentas de agendamento, para responder
            perguntas mesmo que não foi pedido diretamento pelo usuário.
            Exemplo:
            Usuario: Quando será minha próxima viagem internacional ?
            Assistente: Busca no calendário a próxima viagem internacional.
            Assistente: A próxima viagem internacional será em ...
            
            Você tem acesso a uma série de documentos do usuário e pode utilizar esses documentos como fontes para
            responder as perguntas. Os documentos que mais se aproximaram das perguntas do usuário foram os seguintes
            
            ------------------------------------------------------------------------------------------------------
            Ao utilizar esses documentos como fonte, responda SEMPRE no seguinte formato:
            
            SUA RESPOSTA
            
            Fonte: <file_name>
            Página: <page_number>
            
            ------------------------------------------------------------------------------------------------------
            Exemplo:
            
            Seu hotel no Atacama é El Deserto.
            
            Fonte: Booking_Atacama.pdf
            Pagina: 10
            ------------------------------------------------------------------------------------------------------
            
            DOCUMENTOS:
            
            {documentos}
        """
        
        self.SYSTEM_PROMPT += f"Para que possa auxiliar o usuário com agendamentos saiba que hoje é {now}"
        
        
    def get_embeddings(self, text: str) -> list[float]:
        embeddings_result = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text)
        
        embeddings = embeddings_result.data[0].embedding
        
        return embeddings
    
    def ask(self, question, history:ChatMessages = None) -> str:
        
        embeddings = self.get_embeddings(question)
        
        results = self.embedding_repository.search_embeddings(embeddings)       
        
        system_prompt =  self.SYSTEM_PROMPT.replace("{documentos}", results.model_dump_json())
        
        messages=[
            {"role": "system", "content": system_prompt} ]
        
        if history is not None:
            messages.extend(history.messages)
        
        messages.append({"role": "user", "content": question})
        
        completions =  self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
            tools= self.tools.schemas,
        )
        
        response_message = completions.choices[0].message
        tool_calls = response_message.tool_calls
        
        if tool_calls:
            messages.append(response_message)
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                function_response = self.tools.call_tools_by_name(function_name, function_args)
                         
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )
            second_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
            ) 
            return second_response.choices[0].message.content
        
        
        return response_message.content