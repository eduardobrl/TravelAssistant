from typing import Optional
from pydantic import BaseModel, Field
from typing import Any

class From(BaseModel):
  id: int
  is_bot: Optional[bool]
  first_name: Optional[str] = None
  last_name: Optional[str]  = None
  username: Optional[str] = None
  language_code: Optional[str] = None

class Chat(BaseModel):
  id: int
  first_name: Optional[str] = None
  last_name: Optional[str] = None
  username: Optional[str] = None
  type: str

class Document(BaseModel):
  file_id: str
  file_unique_id: str
  file_name: str
  file_size: int
  mime_type: str
  file_size: int

class File:
  file_id: str
  file_unique_id: str
  file_path: str
  file_size: int

class Message(BaseModel):
  message_id: int
  from_: From = Field(alias='from')
  chat: Chat 
  date: int
  text: Optional[str] = None

class Update(BaseModel):
  update_id: int
  message: Message
  document: Optional[Document] = None