from openai import BaseModel, embeddings

class Embedding(BaseModel):
    file_name: str
    embeddings: list[float]

class EmbeddingsResult(BaseModel):
    data: list[Embedding]