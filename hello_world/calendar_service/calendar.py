import datetime
import json
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pydantic import BaseModel

from repositories.credential_repository import CredentialRepository, UserInfo
from typing import List

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

class Event(BaseModel):
    summary: str
    kind: str
    etag: str
    updated: str
    status: str
    htmlLink: str

class EventsResponse(BaseModel):
    items: List[Event]

class Calendar:
    def __init__(self):
        self.credential_repository = CredentialRepository()
        self.calendar_id = os.environ.get("CALENDAR_ID")
    
    def get_next_events(self) -> EventsResponse:   
        user_info = self.credential_repository.get_user_info()
        creds = Credentials.from_authorized_user_info(user_info.model_dump(), SCOPES)
        
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        self.credential_repository.update_credentials(UserInfo.model_validate_json(creds.to_json()))

        try:
            service = build("calendar", "v3", credentials=creds)
            now = datetime.datetime.utcnow().isoformat() + "Z"
            
            events_result = (
                service.events()
                .list(
                    calendarId=self.calendar_id,
                    timeMin=now,
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            
            return EventsResponse.model_validate(events_result)
            
            events = events_result.get("items", [])
            
            if not events:
                print("No upcoming events found.")
                return
            
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(start, event["summary"])

        except HttpError as error:
            print(f"An error occurred: {error}")
            
if __name__ == "__main__":
    calendar = Calendar()
    calendar.get_next_events()