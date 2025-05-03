import asyncio

from ..common.db.mongodb_connector import MongoDBConnector
from ..common.base.repository_base_class import RepositoryBaseClass
from ..common.util.logger import get_logger
from ..common.db.model.driver_user_model import DriverUserModel


class DriverUserRepository(RepositoryBaseClass):
    def __init__(self):
        self._logger = get_logger(__name__)
        self._db = MongoDBConnector().client["bus_ops"]
        self._collection = self._db["driver_users"]

    async def ensure_db_setup(self) -> None:
        self._logger.info("Ensuring database setup")
        try:
            # List all databases
            db_list = await self._db.client.list_database_names()

            # Check if our database exists
            if "bus_ops" not in db_list:
                self._logger.warn("Creating new database")
                await self._db.command({"create": "driver_users"})
                self._logger.info("Created bus_ops database")

            # Check if collection exists
            collections = await self._db.list_collection_names()
            if "driver_users" not in collections:
                await self._db.create_collection("driver_users")
                self._logger.info("Created driver_users collection")

            # Create indexes
            await self._collection.create_index("uid", unique=True)
            self._logger.info("Created index on uid")

            self._logger.info("Database setup completed successfully")
        except Exception as e:
            self._logger.error(f"Database setup error: {e}")

    async def insert_one(
            self,
            document
    ) -> bool:
        try:
            self._logger.info("Inserting document")
            await self._collection.insert_one(document)

        except Exception as e:
            self._logger.error(f"Failed to insert document: {e}")
            return False

        return True

    async def insert_many(
            self,
            documents
    ):
        pass

    async def get_all(self) -> list[DriverUserModel]:
        result: list = []
        try:
            self._logger.info("Getting all users")
            drivers = self._collection.find()
            async for driver in drivers:
                result.append(DriverUserModel(**driver))

        except Exception as e:
            self._logger.error(f"Failed to get documents: {e}")
            return []

        return result

    async def get_one_by_uid(
            self,
            uid: str
    ) -> DriverUserModel | None:
        self._logger.info(f"Getting user for uid: {uid}")
        try:
            user = await self._collection.find_one({"uid": uid})
            return DriverUserModel(**user)

        except Exception as e:
            self._logger.error(f"Failed to get document: {e}")
            return None

    async def update_one(
            self,
            document
    ) -> bool:
        self._logger.info(f"Updating user with uid: {document.uid}")
        try:
            await self._collection.update_one({"uid": document.uid}, {"$set": document.dict()})

        except Exception as e:
            self._logger.error(f"Failed to update document: {e}")
            return False

        return True

    async def update_many(
            self,
            document
    ):
        await super().update_many(document)

    async def delete_one_by_uid(
            self,
            uid: str
    ) -> bool:
        self._logger.info(f"Deleting user with uid: {uid}")
        try:
            await self._collection.delete_one({"uid": uid})

        except Exception as e:
            self._logger.error(f"Failed to delete document: {e}")
            return False

        return True

    async def delete_one_by_email(
            self,
            email: str
    ) -> bool:
        raise NotImplementedError()

    async def get_by_vehicle(
            self,
            plate_number: str | None = None,
            vehicle_uuid: str | None = None
    ) -> dict:
        self._logger.info(f"Getting user by plate: {plate_number} or vehicle_uuid: {vehicle_uuid}")
        result: dict = {"success": False, "message": "", "error": "", "data": {}}
        query = {}

        # NOTE: This is a new one for me, it seems like mongodb allows
        #       you to use dot notation to access nested fields in a document.
        if plate_number:
            query["vehicle.plate_number"] = plate_number
        elif vehicle_uuid:
            query["vehicle.uuid"] = vehicle_uuid
        else:
            self._logger.warn("Neither plate number nor vehicle UUID provided")
            result.update({"success": False, "message": "Herhangi bir araç bilgisi sağlanmadı", "error": ""})
            return result

        try:
            user = await self._collection.find_one(query)
            result.update({"success": True, "message": "User found", "data": user} if user else {"success": False,
                                                                                                 "message": "User not found",
                                                                                                 "error": ""})
        except Exception as e:
            self._logger.error(f"Failed to get document: {e}")
            result.update({"success": False, "message": "Failed to extract document.", "error": str(e)})

        return result


driver_user_repository = DriverUserRepository()