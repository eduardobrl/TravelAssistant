from typing import Any, Optional
from pydantic import BaseModel

class Sentence(BaseModel):
    sentence: str
    summary: Optional[str] = None
    page_number: int
    
class Picture(BaseModel):
    picture: Any
    page_number: int

class FileResult(BaseModel):
    file_name: str
    sentences: list[Sentence]
    images: list[Picture]