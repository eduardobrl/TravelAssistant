from openai import BaseModel, embeddings

class Embedding(BaseModel):
    file_name: str
    embeddings: list[float]
    text: str
    page_number: int

class EmbeddingsResult(BaseModel):
    data: list[Embedding]
    
class EmbeddingQuery(BaseModel):
    file_name: str
    text: str
    page_number: int
    score: float
    
class EmbeddingQueryResult(BaseModel):
    data: list[EmbeddingQuery]