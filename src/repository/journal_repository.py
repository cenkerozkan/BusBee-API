import asyncio

from ..common.db.mongodb_connector import MongoDBConnector
from ..common.base.repository_base_class import RepositoryBaseClass
from ..common.util.logger import get_logger
from ..common.db.model.journal_model import JournalModel

class JournalRepository(RepositoryBaseClass):
    def __init__(self):
        self._logger = get_logger(__name__)
        self._db = MongoDBConnector().client["bus_ops"]
        self._collection = self._db["journals"]

    async def ensure_db_setup(self) -> None:
        self._logger.info("Ensuring database setup")
        try:
            # List all databases
            db_list = await self._db.client.list_database_names()

            # Check if our database exists
            if "bus_ops" not in db_list:
                self._logger.warn("Creating new database")
                await self._db.command({"create": "journals"})
                self._logger.info("Created bus_ops database")

            # Check if collection exists
            collections = await self._db.list_collection_names()
            if "journals" not in collections:
                await self._db.create_collection("journals")
                self._logger.info("Created journals collection")

            # Create indexes
            await self._collection.create_index("journal_uuid", unique=True)
            self._logger.info("Created index on journal_uuid")

            self._logger.info("Database setup completed successfully")
        except Exception as e:
            self._logger.error(f"Database setup error: {e}")

    async def _is_exist(
            self,
            journal_uuid: str
    ) -> bool:
        self._logger.info(f"Checking existence for journal_uuid: {journal_uuid}")
        try:
            journal = await self._collection.find_one({"journal_uuid": journal_uuid})
            return bool(journal)
        except Exception as e:
            self._logger.error(f"Failed to check existence: {e}")
            return False

    async def insert_one(
            self,
            document: JournalModel
    ) -> dict:
        result = {
            "success": False,
            "message": "",
            "error": ""
        }
        try:
            await self._collection.insert_one(document.model_dump())
            result.update({
                "success": True,
                "message": "Journal created successfully"
            })
        except Exception as e:
            result.update({
                "success": False,
                "message": "Failed to create journal",
                "error": str(e)
            })
        return result

    async def get_all(self) -> list[JournalModel]:
        try:
            journals: list[JournalModel] = []
            async for journal in self._collection.find():
                journals.append(JournalModel(**journal))
            return journals
        except Exception as e:
            self._logger.error(f"Failed to get journals: {e}")
            return []

    async def get_one_by_uuid(
            self,
            journal_uuid: str
    ) -> JournalModel | None:
        self._logger.info(f"Getting journal for uuid: {journal_uuid}")
        try:
            journal = await self._collection.find_one({"journal_uuid": journal_uuid})
            if journal:
                return JournalModel(**journal)
            return None
        except Exception as e:
            self._logger.error(f"Failed to get journal: {e}")
            return None

    async def update_one(
            self,
            document: JournalModel
    ) -> dict:
        result = {
            "success": False,
            "message": "",
            "error": ""
        }
        try:
            exists = await self._is_exist(document.journal_uuid)
            if not exists:
                result.update({
                    "success": False,
                    "message": "Journal does not exist"
                })
                return result

            await self._collection.update_one(
                {"journal_uuid": document.journal_uuid},
                {"$set": document.model_dump()}
            )
            result.update({
                "success": True,
                "message": "Journal updated successfully"
            })
        except Exception as e:
            result.update({
                "success": False,
                "message": "Failed to update journal",
                "error": str(e)
            })
        return result

    async def delete_one(
            self,
            journal_uuid: str
    ) -> dict:
        result = {
            "success": False,
            "message": "",
            "error": ""
        }
        try:
            exists = await self._is_exist(journal_uuid)
            if not exists:
                result.update({
                    "success": False,
                    "message": "Journal not found"
                })
                return result

            delete_result = await self._collection.delete_one({"journal_uuid": journal_uuid})
            if delete_result.deleted_count > 0:
                result.update({
                    "success": True,
                    "message": "Journal deleted successfully"
                })
            else:
                result.update({
                    "success": False,
                    "message": "Journal not found"
                })
        except Exception as e:
            result.update({
                "success": False,
                "message": "Failed to delete journal",
                "error": str(e)
            })
        return result

    async def insert_many(self, documents):
        raise NotImplementedError

    async def update_many(self, documents):
        raise NotImplementedError

    async def append_location(
            self,
            journal_uuid: str,
            location: dict
    ) -> dict:
        result = {
            "success": False,
            "message": "",
            "error": ""
        }
        try:
            exists = await self._is_exist(journal_uuid)
            if not exists:
                result.update({"success": False, "message": "Journal not found"})
                return result

            await self._collection.update_one(
                {"journal_uuid": journal_uuid},
                {"$push": {"locations": location}}
            )
            result.update({"success": True, "message": "Location added successfully"})
        except Exception as e:
            result.update({"success": False, "message": "Failed to add location", "error": str(e)})
        return result

    async def get_one_by_driver_uuid(
            self,
            driver_uid: str
    ) -> JournalModel | None:
        self._logger.info(f"Getting journal for driver_uid: {driver_uid}")
        try:
            journal = await self._collection.find_one({"driver_uid": driver_uid})
            if journal:
                return JournalModel(**journal)
            return None
        except Exception as e:
            self._logger.error(f"Failed to get journal: {e}")
            return None


journal_repository = JournalRepository()