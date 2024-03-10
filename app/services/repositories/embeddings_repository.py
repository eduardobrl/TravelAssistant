import os
import pymongo

from domain.embedings_entities import Embedding, EmbeddingQuery, EmbeddingQueryResult, EmbeddingsResult
from services.secrets.secrets import get_secrets

class EmbeddingRepository:
    def __init__(self) -> None:
        
        secrets = get_secrets()
        self.client = pymongo.MongoClient(secrets.MONGODB_URL)
        self.db = self.client.get_database(secrets.MONGODB_DB)
        self.collection = self.db.get_collection(secrets.MONGODB_COLLECTION)
        
    def insert_embedding(self, embedding_result: EmbeddingsResult):
        models = [embedding.model_dump() for embedding in embedding_result.data]
        self.collection.insert_many(models)     
        
    def search_embeddings(self, embedding_result: list[float], text: str) -> EmbeddingQueryResult:
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embeddings",
                    "queryVector": embedding_result,
                    "numCandidates": 100,
                    "limit": 10
                }
            },
            {
                "$project": {
                    "embeddings": 0,
                    "score": { "$meta": "vectorSearchScore" }
                }
            }
        ]  
        
        results = self.collection.aggregate(pipeline)
        
        results_list = [
            EmbeddingQuery(
                file_name=result["file_name"], 
                page_number=result["page_number"],
                text = result["text"],
                score=result["score"],
                summary= result["summary"]
            ) 
            for result in results
        ]
        
        return EmbeddingQueryResult(data=results_list)