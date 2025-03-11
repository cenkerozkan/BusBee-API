from ..common.meta.singleton_meta import SingletonMeta
from ..common.db.mongodb_connector import MongoDBConnector
from ..common.logger import get_logger
from ..common.base.repository_base_class import RepositoryBaseClass

class UserRepository(RepositoryBaseClass):
    def __init__(self):
        self._logger = get_logger(__name__)
        self._db = MongoDBConnector().client["bus_ops"]

    async def insert_one(
            self,
            document
    ):
        pass

    async def insert_many(
            self,
            documents
    ):
        pass

    async def get_all(self):
        pass

    async def update_one(
            self,
            document
    ):
        pass

    async def update_many(
            self,
            document
    ):
        pass