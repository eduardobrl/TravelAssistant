from tkinter import Image
from typing import Any
from pydantic import BaseModel
import fitz

class Sentence(BaseModel):
    sentence: str
    page_number: int
    
class Picture(BaseModel):
    picture: Any
    page_number: int

class FileResult(BaseModel):
    file_name: str
    sentences: list[Sentence]
    images: list[Picture]