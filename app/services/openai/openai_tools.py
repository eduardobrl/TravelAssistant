from typing import Annotated, get_type_hints
from click import argument
from pydantic import BaseModel
from services.calendar.calendar import AddEvent, Calendar
import inspect


Tools = []
def OpenAiTool(func):         
    Tools.append({
        "name": func.__name__,
        "description": func.__doc__,
        "function": func
    })
    
    
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

class OpenAiTools():
    def __init__(self, calendar : Calendar) -> None:
        self.calendar = calendar
    
    @OpenAiTool
    def get_next_calendar_events(self):
        """
            Esta função obtém os próximos eventos que estão agendados no calendário do usuário.
        """
        return self.calendar.get_next_events().model_dump_json()
    
    @OpenAiTool
    def add_calendar_event(self, addToCalendarEvent: AddEvent):
        """
            Esta função adiciona um novo evento ao calendário do usuário.
        """
        return self.calendar.add_event_to_calendar(AddEvent.model_validate(addToCalendarEvent)).model_dump_json()
    

    
    schemas = [
        {
            "type": "function",
            "function": {
                "name": "get_next_calendar_events",
                "description": "Obtém os próximos eventos que estão agendados no calendário do usuário.",
            }
        },
        {
            "type": "function",
            "function": {
                "name": "add_calendar_event",
                "description": "Adiciona eventos para o calendario do usuário.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "nome_evento": {
                            "type": "string",
                            "description": "Título do evento."
                        },
                        "descricao": {
                            "type": "string",
                            "description": "Descrição do evento."
                        },
                        "inicio": {
                            "type": "string",
                            "description": "Hora de início do evento."
                        },
                        "fim": {
                            "type": "string",
                            "description": "Hora de término do evento."
                        }
                    }
                }
            }
        }  
    ]
    
    
    def call_tools_by_name(self, name: str, params):
        for tool in Tools:
            if tool["name"] == name:
                if len(params) == 0:
                    return tool["function"](self)               
                return tool["function"](self, params) 
        return None
    
