import asyncio

from ..common.db.mongodb_connector import MongoDBConnector
from ..common.base.repository_base_class import RepositoryBaseClass
from ..common.util.logger import get_logger
from ..common.db.model.route_model import RouteModel
from ..common.db.model.lat_lon_model import LatLonModel

class RouteRepository(RepositoryBaseClass):
    """
    This repository is responsible from models:
        class RouteModel(BaseModel):
            uuid: str
            route_name: str
            created_at: str
            updated_at: str
            start_time: str
            driver_name: str
            driver_number: str
            stops: list[LatLonModel]
    """
    def __init__(self):
        self._logger = get_logger(__name__)
        self._db = MongoDBConnector().client["bus_ops"]
        self._collection = self._db["routes"]

    async def ensure_db_setup(self) -> None:
        self._logger.info("Ensuring database setup")
        try:
            # List all databases
            db_list = await self._db.client.list_database_names()

            # Check if our database exists
            if "bus_ops" not in db_list:
                self._logger.warn("Creating new database")
                await self._db.command({"create": "routes"})
                self._logger.info("Created bus_ops database")

            # Check if collection exists
            collections = await self._db.list_collection_names()
            if "routes" not in collections:
                await self._db.create_collection("routes")
                self._logger.info("Created routes collection")

            # Create indexes
            await self._collection.create_index("uuid", unique=True)
            await self._collection.create_index("route_name", unique=True)

            self._logger.info("Created indexes on uid and email")

            self._logger.info("Database setup completed successfully")
        except Exception as e:
            self._logger.error(f"Database setup error: {e}")

    async def _check_uniqueness_by_name(
            self,
            name: str
    ) -> bool:
        self._logger.info(f"Checking uniqueness for name: {name}")
        try:
            route = await self._collection.find_one({"route_name": name})
            return not bool(route)
        except Exception as e:
            self._logger.error(f"Failed to check uniqueness for name: {e}")
            return False

    async def _is_exist(
            self,
            route_id: str | None = None,
            route_name: str | None = None
    ):
        self._logger.info(f"Checking existence for route_id: {route_id} and route_name: {route_name}")
        try:
            if route_id:
                route = await self._collection.find_one({"uuid": route_id})
            elif route_name:
                route = await self._collection.find_one({"route_name": route_name})
            else:
                return False

            return bool(route)

        except Exception as e:
            self._logger.error(f"Failed to check existence: {e}")
            return False

    async def insert_one(
            self,
            document
    ) -> dict:
        # I forced uniqueness on uuid and route_name
        # If the document already exists, it will raise an error
        result: dict = {
            "success": False,
            "message": "",
            "error": "",
        }
        self._logger.info("Inserting document")
        is_unique: bool = await self._check_uniqueness_by_name(document["route_name"])
        # Check if the document is unique
        if not is_unique:
            self._logger.error(f"Route name already exists: {document['route_name']}")
            result.update({"success": False, "message": "Route name already exists"})
            return result

        try:
            await self._collection.insert_one(document)
            result.update({"success": True, "message": "Document inserted successfully"})

        except Exception as e:
            self._logger.error(f"Failed to insert document: {e}")
            result.update({"success": False, "message": "Something went wrong", "error": f"{e}"})

        return result

    async def insert_many(
            self,
            documents
    ):
        pass

    async def get_all(self) -> list[RouteModel]:
        results: list[RouteModel] = []
        self._logger.info("Retrieving all routes")
        try:
            routes = self._collection.find()
            async for route in routes:
                results.append(RouteModel(**route))

        except Exception as e:
            self._logger.error(f"Failed to get all routes: {e}")
            return []

        return results

    async def get_one_by_uuid(
            self,
            uuid: str
    ) -> RouteModel | None:
        result: RouteModel
        self._logger.info(f"Getting route for uuid: {uuid}")
        try:
            route = await self._collection.find_one({"uuid": uuid})
        except Exception as e:
            self._logger.error(f"Failed to get route for uuid: {e}")
            return None
        if route:
            return RouteModel(**route)

        return None

    async def get_one_by_name(
            self,
            name: str
    ) -> RouteModel | None:
        result: RouteModel
        self._logger.info(f"Getting route for name: {name}")
        try:
            route = await self._collection.find_one({"route_name": name})

        except Exception as e:
            self._logger.error(f"Failed to get route for name: {e}")
            return None

        return RouteModel(**route)

    async def update_one(
            self,
            document
    ) -> dict:
        result: dict = {
            "success": False,
            "message": "",
            "error": "",
        }
        exists: bool = await self._is_exist(route_id=document.uuid)
        # Check if the document exists
        if not exists:
            self._logger.error(f"Route with uuid {document.uuid} does not exist")
            result.update({"success": False, "message": "Route does not exist"})
            return result
        self._logger.info(f"Updating route for uuid: {document.uuid}")

        try:
            await self._collection.update_one({"uuid": document.uuid}, {"$set": document.model_dump()})
            result.update({"success": True, "message": "Document updated successfully"})

        except Exception as e:
            self._logger.error(f"Failed to update route for uuid: {e}")
            result.update({"success": False, "message": "Something went wrong", "error": f"{e}"})

        return result

    async def delete_one_by_uuid(
            self,
            uuid: str
    ) -> dict:
        result: dict = {
            "success": False,
            "message": "",
            "error": "",
        }
        # Check if the document exists
        exists: bool = await self._is_exist(route_id=uuid)
        if not exists:
            self._logger.error(f"Route with uuid {uuid} does not exist")
            result.update({"success": False, "message": "Route does not exist"})
            return result
        self._logger.info(f"Deleting route for uuid: {uuid}")

        try:
            await self._collection.delete_one({"uuid": uuid})
            result.update({"success": True, "message": "Document deleted successfully"})

        except Exception as e:
            self._logger.error(f"Failed to delete route for uuid: {e}")
            result.update({"success": False, "message": "Something went wrong", "error": f"{e}"})

        return result

    async def delete_one_by_name(
            self,
            name: str
    ) -> dict:
        result: dict = {
            "success": False,
            "message": "",
            "error": "",
        }
        # Check if the document exists
        exists: bool = await self._is_exist(route_name=name)
        if not exists:
            self._logger.error(f"Route with name {name} does not exist")
            result.update({"success": False, "message": "Route does not exist"})
            return result

        self._logger.info(f"Deleting route for name: {name}")

        try:
            await self._collection.delete_one({"name": name})
            result.update({"success": True, "message": "Document deleted successfully"})

        except Exception as e:
            self._logger.error(f"Failed to delete route for name: {e}")
            result.update({"success": False, "message": "Something went wrong", "error": f"{e}"})

        return result

    async def delete_many_by_uuids(
            self,
            uuids: list[str]
    ) -> bool:
        self._logger.info(f"Deleting routes for uuids: {uuids}")

        try:
            await self._collection.delete_many({"uuid": uuids})
            return True

        except Exception as e:
            self._logger.error(f"Failed to delete routes for uuids: {e}")
            return False

    async def update_many(self, document):
        raise NotImplementedError

route_repository = RouteRepository()
