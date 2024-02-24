import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pydantic import BaseModel
from dateutil import parser
from services.secrets.secrets import get_secrets
from services.repositories.credential_repository import CredentialRepository, UserInfo
from typing import List, Optional

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly", "https://www.googleapis.com/auth/calendar"]

class Event(BaseModel):
    nome_evento: str
    descricao: Optional[str] = None
    endereco: Optional[str] = None
    inicio: str
    fim: str
    link: str

class EventsResponse(BaseModel):
    items: List[Event]
    
class AddEvent(BaseModel):
    nome_evento: str
    descricao: Optional[str] = None
    inicio: datetime.datetime
    fim: datetime.datetime
    link: Optional[str] = None
    
class AddEventResponse(BaseModel):
    mensagem: str
    
def localize(self, dt, is_dst=False):
    '''Convert naive time to local time'''
    if dt.tzinfo is not None:
        raise ValueError('Not naive datetime (tzinfo is already set)')
    return dt.replace(tzinfo=self)

class Calendar:
    def __init__(self):
        self.credential_repository = CredentialRepository()
        self.calendar_id = get_secrets().CALENDAR_ID
        
        user_info = self.credential_repository.get_user_info()
        creds = Credentials.from_authorized_user_info(user_info.model_dump(), SCOPES)
        
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        self.credential_repository.update_credentials(UserInfo.model_validate_json(creds.to_json()))
        
        self.client = build("calendar", "v3", credentials=creds)      
        
    
    def get_next_events(self) -> EventsResponse:   
        try:
            now = datetime.datetime.utcnow().isoformat() + "Z"
            
            events_result = (
                self.client.events()
                .list(
                    calendarId=self.calendar_id,
                    timeMin=now,
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )

            response = []
            

            
            for event in events_result["items"]:
                start = event.get("start")
                inicio = parser.parse(start['dateTime'])
                
                end = event.get("start")
                fim = parser.parse(end['dateTime'])
                
                response.append(Event(
                    nome_evento=event.get("summary"),
                    descricao=event.get("description"),
                    endereco=event.get("location"),
                    inicio=inicio.astimezone().isoformat(),
                    fim=fim.astimezone().isoformat(),
                    link=event.get("htmlLink")
                ))
            
            return EventsResponse(items=response)

        except HttpError as error:
            print(f"An error occurred: {error}")
            
    def add_event_to_calendar(self, add_event: AddEvent) -> AddEventResponse:
        try:           
            event = {
                'summary': add_event.nome_evento,
                'description': add_event.descricao,
                'start': {
                    'dateTime':add_event.inicio.isoformat(),
                    'timeZone': 'America/Sao_Paulo',
                },
                'end': {
                    'dateTime': add_event.inicio.isoformat(),
                    'timeZone': 'America/Sao_Paulo',
                },
                'reminders': {
                    'useDefault': True,
                },
            }
            event = self.client.events().insert(calendarId=self.calendar_id, body=event).execute()
            
            return AddEventResponse(mensagem="Evento adicionado com sucesso!")
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            
            


if __name__ == "__main__":
    calendar = Calendar()
    calendar.get_next_events()