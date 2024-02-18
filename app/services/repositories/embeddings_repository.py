import os
import pymongo

from domain.embedings_entities import EmbeddingsResult

class EmbeddingRepository:
    def __init__(self) -> None:
        self.client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
        self.db = self.client.get_database(os.environ.get('MONGO_DB'))
        self.collection = self.db.get_collection(os.environ.get('MONGO_COLLECTION'))
        
    def insert_embedding(self, embedding_result: EmbeddingsResult):
        for embedding in embedding_result.data:
            self.collection.insert_one(embedding.model_dump())     