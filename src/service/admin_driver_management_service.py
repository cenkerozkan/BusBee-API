import datetime as dt
import asyncio

from ..common.meta.singleton_meta import SingletonMeta
from ..common.firebase.firebase_handler import firebase_handler
from ..common.db.model.driver_user_model import DriverUserModel
from ..common.db.model.vehicle_model import VehicleModel
from ..repository.driver_user_repository import driver_user_repository
from ..repository.vehicle_repository import vehicle_repository
from ..common.request_model.admin_driver_management_models import AddDriverUserModel
from ..common.util.logger import get_logger
from ..common.util.error_messages import get_error_message


class AdminDriverManagementService:
    __slots__ = ("_logger", "_firebase_handler", "_driver_user_repository", "_vehicle_repository")
    def __init__(self):
        self._logger = get_logger(__name__)
        self._firebase_handler = firebase_handler
        self._driver_user_repository = driver_user_repository
        self._vehicle_repository = vehicle_repository

    def add_driver(
            self,
            driver_data: AddDriverUserModel
    ) -> dict:
        self._logger.info(f"Adding driver {driver_data.first_name} {driver_data.last_name}")
        firebase_result: dict = {}
        is_saved: bool = False
        result: dict = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }

        try:
            firebase_result = self._firebase_handler.create_driver_user(driver_data.phone_number)

        except Exception as e:
            self._logger.error(f"Failed to create driver user: {e}")
            result.update(
                {
                    "code": 500,
                    "success": False,
                    "message": "Failed to create driver user",
                    "error": str(e)
                }
            )
            return result

        if firebase_result:
            new_driver_user: DriverUserModel = DriverUserModel(
                uid=firebase_result.get("uid"),
                first_name=driver_data.first_name,
                last_name=driver_data.last_name,
                phone_number=driver_data.phone_number,
            )
            is_saved = asyncio.run(self._driver_user_repository.insert_one(new_driver_user.model_dump()))
            if not is_saved:
                result.update(
                    {
                        "code": 500,
                        "success": False,
                        "message": "Failed to add driver user",
                        "error": ""
                    }
                )
            result.update(
                {
                    "code": 200,
                    "success": True,
                    "message": "Driver user added",
                    "data": new_driver_user.model_dump()
                }
            )
        return result

    def delete_driver(
            self,
            driver_uid: str
    ) -> bool:
        self._logger.info(f"Deleting driver {driver_uid}")
        is_deleted: bool = False
        firebase_response: bool = False

        try:
            firebase_response: bool = self._firebase_handler.remove_driver_user(driver_uid)

        except Exception as e:
            self._logger.error(f"Failed to delete driver user: {e}")
            return is_deleted

        if firebase_response:
            is_deleted = asyncio.run(self._driver_user_repository.delete_one_by_uid(driver_uid))

        return is_deleted

    def update_driver_phone_number(
            self,
            driver_uid: str,
            new_phone_number: str
    ) -> dict:
        self._logger.info(f"Updating driver phone number: {new_phone_number} for driver: {driver_uid}")
        result: dict = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }
        firebase_response: bool = False
        is_updated: bool = False

        try:
            firebase_response = self._firebase_handler.update_driver_phone_number(driver_uid, new_phone_number)

        except Exception as e:
            self._logger.error(f"Failed to update driver phone number: {e}")
            result.update(
                {
                    "code": 500,
                    "success": False,
                    "message": "Failed to update driver phone number",
                    "error": str(e)
                }
            )
            return result

        if firebase_response is True:
            driver_user: DriverUserModel = asyncio.run(self._driver_user_repository.get_one_by_uid(driver_uid))
            driver_user.phone_number = new_phone_number
            is_updated = asyncio.run(self._driver_user_repository.update_one(driver_user))

            if is_updated:
                result.update(
                    {
                        "code": 200,
                        "success": True,
                        "message": "Driver phone number updated",
                        "data": driver_user.model_dump()
                    }
                )
            else:
                result.update(
                    {
                        "code": 500,
                        "success": False,
                        "message": "Failed to update driver phone number",
                        "error": get_error_message("failed_to_update_driver_phone_number")
                    }
                )

        return result

    async def get_all_drivers(
            self
    ) -> dict:
        result: dict = {
            "code": 200,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }
        drivers: list

        try:
            drivers = await self._driver_user_repository.get_all()
            self._logger.info(drivers)

        except Exception as e:
            self._logger.error(f"Failed to get drivers: {e}")
            result.update(
                {
                    "code": 500,
                    "success": False,
                    "message": "Failed to get drivers",
                    "error": str(e)
                }
            )
            return result

        if len(drivers) == 0:
            result.update(
                {
                    "code": 404,
                    "success": True,
                    "message": "No drivers found",
                    "data": {}
                }
            )
        else:
            result.update(
                {
                    "code": 200,
                    "success": True,
                    "message": "Drivers retrieved",
                    "data": {"drivers": [driver.model_dump() for driver in drivers]}
                }
            )
        return result

    async def assign_vehicle_to_driver(self, driver_uid: str, vehicle_uuid: str) -> dict:
        result: dict = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }

        # Fetch the driver
        driver = await self._driver_user_repository.get_one_by_uid(driver_uid)
        if not driver:
            result.update({
                "code": 404,
                "success": False,
                "message": "Driver not found"
            })
            return result

        # Fetch the vehicle
        vehicles = await self._vehicle_repository.get_all()
        vehicle = next((v for v in vehicles if v.uuid == vehicle_uuid), None)
        if not vehicle:
            result.update({
                "code": 404,
                "success": False,
                "message": "Vehicle not found"
            })
            return result

        # Assign the vehicle to the driver
        driver.vehicle = vehicle
        update_result = await self._driver_user_repository.update_one(driver)
        if not update_result:
            result.update({
                "code": 500,
                "success": False,
                "message": "Failed to assign vehicle to driver"
            })
            return result

        result.update({
            "code": 200,
            "success": True,
            "message": "Vehicle assigned to driver successfully",
            "data": {"driver": driver.model_dump()}
        })
        return result

    async def remove_vehicle_from_driver(
            self,
            driver_uid: str
    ) -> dict:
        result: dict = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }

        self._logger.info(f"Removing vehicle from driver: {driver_uid}")

        # Get driver
        driver = await self._driver_user_repository.get_one_by_uid(driver_uid)
        if not driver:
            result.update({
                "code": 404,
                "success": False,
                "message": "Driver not found"
            })
            return result

        # Check if driver has a vehicle
        if not driver.vehicle:
            result.update({
                "code": 400,
                "success": False,
                "message": "Driver has no vehicle assigned"
            })
            return result

        # Remove vehicle from driver
        driver.vehicle = None
        update_result = await self._driver_user_repository.update_one(driver)
        if not update_result:
            result.update({
                "code": 500,
                "success": False,
                "message": "Failed to remove vehicle from driver",
                "error": "Database error"
            })
            return result

        result.update({
            "code": 200,
            "success": True,
            "message": "Vehicle removed from driver successfully",
            "data": {"driver": driver.model_dump()}
        })
        return result


admin_management_service = AdminDriverManagementService()