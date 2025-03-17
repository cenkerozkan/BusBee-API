from abc import ABC, abstractmethod

class RepositoryBaseClass(ABC):
    @abstractmethod
    async def _ensure_db_setup(self):
        raise NotImplementedError

    @abstractmethod
    async def insert_one(self, document):
        raise NotImplementedError

    @abstractmethod
    async def insert_many(self, documents):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, document):
        raise NotImplementedError

    @abstractmethod
    async def update_many(self, document):
        raise NotImplementedError