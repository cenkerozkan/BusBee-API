import asyncio

from ..common.db.mongodb_connector import MongoDBConnector
from ..common.base.repository_base_class import RepositoryBaseClass
from ..common.util.logger import get_logger
from ..common.db.model.admin_user_model import AdminUserModel

class AdminUserRepository(RepositoryBaseClass):
    def __init__(self):
        self._logger = get_logger(__name__)
        self._db = MongoDBConnector().client["bus_ops"]
        self._collection = self._db["admin_users"]

    async def ensure_db_setup(self) -> None:
        self._logger.info("Ensuring database setup")
        try:
            # List all databases
            db_list = await self._db.client.list_database_names()

            # Check if our database exists
            if "bus_ops" not in db_list:
                self._logger.warn("Creating new database")
                await self._db.command({"create": "admin_users"})
                self._logger.info("Created bus_ops database")

            # Check if collection exists
            collections = await self._db.list_collection_names()
            if "admin_users" not in collections:
                await self._db.create_collection(
                    "admin_users",
                    validator={
                        "$jsonSchema": {
                            "bsonType": "object",
                            "required": ["uid", "created_at", "last_active", "email"],
                            "properties": {
                                "uid": {"bsonType": "string"},
                                "created_at": {"bsonType": "string"},
                                "last_active": {"bsonType": "string"},
                                "role": {"bsonType": "string"},
                                "email": {"bsonType": "string"}
                            }
                        }
                    }
                )
                self._logger.info("Created end_users collection")

            # Create indexes
            await self._collection.create_index("uid", unique=True)
            await self._collection.create_index("email", unique=True)
            self._logger.info("Created indexes on uid and email")

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

    async def get_all(self) -> list | None:
        self._logger.info("Getting all admins")
        result: list[AdminUserModel] = []
        try:
            query = self._collection.find()
            async for document in query:
                result.append(AdminUserModel(**document))

        except Exception as e:
            self._logger.error(f"Failed to get all admins: {e}")
            return None

        return result

    async def get_one(
            self,
            email: str
    ) -> AdminUserModel | None:
        self._logger.info(f"Getting user for email: {email}")
        try:
            user = await self._collection.find_one({"email": email})
            return AdminUserModel(**user)

        except Exception as e:
            self._logger.error(f"Failed to get document: {e}")
            return None


    async def update_one(
            self,
            document
    ):
        await super().update_one(document)

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
        self._logger.info(f"Deleting user with email: {email}")
        try:
            await self._collection.delete_one({"email": email})

        except Exception as e:
            self._logger.error(f"Failed to delete document: {e}")
            return False

        return True


admin_user_repository = AdminUserRepository()