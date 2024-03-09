
from services.openai.openai_client import OpenAiClient
from services.secrets.secrets import get_secrets
from domain.embedings_entities import Embedding, EmbeddingsResult
from domain.file_entities import FileResult

client = OpenAiClient()

def generate_embeddings(file: FileResult) -> EmbeddingsResult:    
    text_embeddings_list = []
    for sentence in file.sentences:
        embeddings = client.get_embeddings(sentence.model_dump_json())
        
        text_embeddings_list.append(
            Embedding(
                        embeddings = embeddings,
                        file_name=file.file_name,
                        text=sentence.sentence,
                        page_number=sentence.page_number
                        
                )
        )
    
    return EmbeddingsResult(data=text_embeddings_list)