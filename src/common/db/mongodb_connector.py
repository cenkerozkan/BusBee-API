import os

from ..meta.singleton_meta import SingletonMeta
from ..util.logger import get_logger

from pymongo import AsyncMongoClient
from pymongo.errors import ConnectionFailure

class MongoDBConnector:
    def __init__(self):
        self._logger = get_logger(__name__)
        self._uri = os.getenv("MONGO_URI")
        self.client: AsyncMongoClient = AsyncMongoClient(self._uri, maxPoolSize=300)

    async def ping_db(self):
        try:
            await self.client.admin.command('ping')
            return True
        except ConnectionFailure:
            self._logger.error("MongoDB connection failed.")