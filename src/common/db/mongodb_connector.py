import os

from ..meta.singleton_meta import SingletonMeta

from pymongo import AsyncMongoClient

class MongoDBConnector:
    def __init__(self):
        self.client: AsyncMongoClient = AsyncMongoClient(os.getenv("MONGO_URI"))