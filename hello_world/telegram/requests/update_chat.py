from typing import Optional
from pydantic import BaseModel, Field

class From(BaseModel):
  id: int
  is_bot: bool
  first_name: str
  last_name: str 
  username: str
  language_code: str

class Chat(BaseModel):
  id: int
  first_name: Optional[str] = None
  last_name: Optional[str] = None
  username: Optional[str] = None
  type: str

class Message(BaseModel):
  message_id: int
  from_: From = Field(alias='from')
  chat: Chat 
  date: int
  text: Optional[str] = None

class Update(BaseModel):
  update_id: int
  message: Message