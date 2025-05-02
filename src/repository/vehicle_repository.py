# src/repository/vehicle_repository.py
import uuid
from ..common.base.repository_base_class import RepositoryBaseClass
from ..common.util.logger import get_logger
from ..common.db.model.vehicle_model import VehicleModel
from ..common.db.mongodb_connector import MongoDBConnector

class VehicleRepository(RepositoryBaseClass):
    def __init__(self):
        self._logger = get_logger(__name__)
        self._db = MongoDBConnector().client["bus_ops"]
        self._collection = self._db["vehicles"]

    async def ensure_db_setup(self) -> None:
        try:
            await self._collection.create_index("uuid", unique=True)
            await self._collection.create_index("plate_number", unique=True)
            self._logger.info("Vehicle indexes created successfully")
        except Exception as e:
            self._logger.error(f"Failed to create indexes: {e}")

    async def _is_exist(
            self,
            vehicle_uuid: str | None = None,
            plate_number: str | None = None
    ) -> bool:
        self._logger.info(f"Checking existence for uuid: {vehicle_uuid} or plate: {plate_number}")
        try:
            if vehicle_uuid:
                vehicle = await self._collection.find_one({"uuid": vehicle_uuid})
            elif plate_number:
                vehicle = await self._collection.find_one({"plate_number": plate_number})
            else:
                return False

            return bool(vehicle)

        except Exception as e:
            self._logger.error(f"Failed to check existence: {e}")
            return False

    async def _is_unique(
            self,
            plate_number: str
    ) -> bool:
        self._logger.info(f"Checking uniqueness for plate number: {plate_number}")
        try:
            vehicle = await self._collection.find_one({"plate_number": plate_number})
            return not bool(vehicle)

        except Exception as e:
            self._logger.error(f"Failed to check uniqueness: {e}")
            return False

    async def insert_one(
            self,
            document: dict
    ) -> dict:
        result = {"success": False, "message": "", "error": ""}
        try:
            is_unique = await self._is_unique(document["plate_number"])
            if not is_unique:
                result.update({
                    "success": False,
                    "message": "Vehicle with this plate number already exists"
                })
                return result

            await self._collection.insert_one(document)
            result.update({"success": True, "message": "Vehicle created successfully"})
        except Exception as e:
            result.update({"success": False, "message": "Failed to create vehicle", "error": str(e)})
        return result

    async def get_all(self) -> list[VehicleModel]:
        try:
            vehicles: list = []
            async for vehicle in self._collection.find():
                vehicles.append(VehicleModel(**vehicle))
            return vehicles
        except Exception as e:
            self._logger.error(f"Failed to get vehicles: {e}")
            return []

    async def get_one_by_uuid(
            self,
            vehicle_uuid: str
    ) -> VehicleModel | None:
        self._logger.info(f"Getting vehicle for uuid: {vehicle_uuid}")
        try:
            vehicle = await self._collection.find_one({"uuid": vehicle_uuid})
            if vehicle:
                return VehicleModel(**vehicle)
            return None
        except Exception as e:
            self._logger.error(f"Failed to get vehicle: {e}")
            return None

    async def update_one(
            self,
            document: VehicleModel
    ) -> dict:
        result = {"success": False, "message": "", "error": ""}
        try:
            exists = await self._is_exist(vehicle_uuid=document.uuid)
            if not exists:
                result.update({
                    "success": False,
                    "message": "Vehicle does not exist"
                })
                return result

            # Check if the updated plate number conflicts with another vehicle
            if await self._is_exist(plate_number=document.plate_number):
                current_vehicle = await self._collection.find_one({"uuid": document.uuid})
                if current_vehicle and current_vehicle["plate_number"] != document.plate_number:
                    result.update({
                        "success": False,
                        "message": "Another vehicle with this plate number already exists"
                    })
                    return result

            await self._collection.update_one(
                {"uuid": document.uuid},
                {"$set": document.model_dump()}
            )
            result.update({"success": True, "message": "Vehicle updated successfully"})
        except Exception as e:
            result.update({"success": False, "message": "Failed to update vehicle", "error": str(e)})
        return result

    async def delete_one(
            self,
            vehicle_uuid: str
    ) -> dict:
        result = {"success": False, "message": "", "error": ""}
        try:
            exists = await self._is_exist(vehicle_uuid=vehicle_uuid)
            if not exists:
                result.update({
                    "success": False,
                    "message": "Vehicle not found"
                })
                return result

            delete_result = await self._collection.delete_one({"uuid": vehicle_uuid})
            if delete_result.deleted_count > 0:
                result.update({"success": True, "message": "Vehicle deleted successfully"})
            else:
                result.update({"success": False, "message": "Vehicle not found"})
        except Exception as e:
            result.update({"success": False, "message": "Failed to delete vehicle", "error": str(e)})
        return result

    async def delete_one_by_plate(
            self,
            plate_number: str
    ) -> dict:
        result = {"success": False, "message": "", "error": ""}
        try:
            exists = await self._is_exist(plate_number=plate_number)
            if not exists:
                result.update({
                    "success": False,
                    "message": "Vehicle not found"
                })
                return result

            delete_result = await self._collection.delete_one({"plate_number": plate_number})
            if delete_result.deleted_count > 0:
                result.update({"success": True, "message": "Vehicle deleted successfully"})
            else:
                result.update({"success": False, "message": "Vehicle not found"})
        except Exception as e:
            result.update({"success": False, "message": "Failed to delete vehicle", "error": str(e)})
        return result

    async def get_by_route_uuid(
            self,
            route_uuid: str
    ) -> list[VehicleModel]:
        try:
            vehicles = []
            cursor = self._collection.find({"route_uuids": route_uuid})
            async for vehicle in cursor:
                vehicles.append(VehicleModel(**vehicle))
            return vehicles
        except Exception as e:
            self._logger.error(f"Failed to get vehicles by route UUID: {e}")
            return []

    async def insert_many(self, documents):
        raise NotImplementedError

    async def update_many(self, documents):
        raise NotImplementedError

vehicle_repository = VehicleRepository()