from ..common.util.logger import get_logger
from ..repository.driver_user_repository import driver_user_repository
from ..repository.vehicle_repository import vehicle_repository
from ..repository.route_repository import route_repository

logger = get_logger(__name__)

class DriverService:
    def __init__(self):
        self._logger = logger
        self._driver_user_repository = driver_user_repository
        self._vehicle_repository = vehicle_repository
        self._route_repository = route_repository

    async def get_vehicle(
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
        driver = await self._driver_user_repository.get_one_by_uid(driver_uid)
        if not driver:
            result.update({
                "code": 404,
                "success": False,
                "message": "Driver not found"
            })
            return result

        if not driver.vehicle:
            result.update({
                "code": 404,
                "success": False,
                "message": "Driver is not assigned to a vehicle"
            })
            return result

        vehicle = await self._vehicle_repository.get_all()
        vehicle = next((v for v in vehicle if v.uuid == driver.vehicle.uuid), None)
        if not vehicle:
            result.update({
                "code": 404,
                "success": False,
                "message": "Vehicle not found"
            })
            return result

        result.update({
            "code": 200,
            "success": True,
            "message": "Vehicle retrieved successfully",
            "data": vehicle.model_dump()
        })
        return result

    async def get_vehicle_route(
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
        driver = await self._driver_user_repository.get_one_by_uid(driver_uid)
        if not driver:
            result.update({
                "code": 404,
                "success": False,
                "message": "Driver not found"
            })
            return result

        if not driver.vehicle:
            result.update({
                "code": 404,
                "success": False,
                "message": "Driver is not assigned to a vehicle"
            })
            return result

        vehicle: list = await self._vehicle_repository.get_all()
        vehicle = next((v for v in vehicle if v.uuid == driver.vehicle.uuid), None)
        if not vehicle:
            result.update({
                "code": 404,
                "success": False,
                "message": "Vehicle not found"
            })
            return result

        routes: list = await self._route_repository.get_all()
        assigned_routes = [route.model_dump() for route in routes if route.uuid in vehicle.route_uuids]

        result.update({
            "code": 200,
            "success": True,
            "message": "Vehicle routes retrieved successfully",
            "data": {"routes": assigned_routes}
        })
        return result

driver_service = DriverService()