
from app.services.secrets.secrets import get_secrets
from domain.embedings_entities import Embedding, EmbeddingsResult
from domain.file_entities import FileResult
import openai

client = openai.Client(api_key=get_secrets().OPENAI_API_KEY)

def generate_embeddings(file: FileResult) -> EmbeddingsResult:    
    text_embeddings_list = []
    for sentence in file.sentences:
        embeddings_result = client.embeddings.create(
                model="text-embedding-ada-002",
                input=sentence)
        
        embeddings = embeddings_result.data[0].embedding
        
        text_embeddings_list.append(
            Embedding(
                        embeddings = embeddings,
                        file_name=file.file_name,
                )
        )
    
    return EmbeddingsResult(data=text_embeddings_list)