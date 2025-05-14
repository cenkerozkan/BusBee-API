import datetime as dt
import uuid

from ..common.db.model.driver_user_model import DriverUserModel
from ..common.db.model.vehicle_model import VehicleModel
from ..repository.route_repository import route_repository
from ..repository.vehicle_repository import vehicle_repository
from ..repository.driver_user_repository import driver_user_repository
from ..common.util.logger import get_logger
from ..common.db.model.route_model import RouteModel
from ..common.request_model.admin_route_management_models import *

class AdminRouteManagementService:
    __slots__ = ("_logger", "_route_repository", "_vehicle_repository", "_driver_user_repository")
    def __init__(self):
        self._logger = get_logger(__name__)
        self._route_repository = route_repository
        self._vehicle_repository = vehicle_repository
        self._driver_user_repository = driver_user_repository

    async def create_route(
            self,
            new_route: NewRoute,
    ) -> dict:
        self._logger.info(f"Creating new route: {new_route}")
        result: dict = {"code": 0, "success": False, "message": "", "error": "", "data": {}}
        new_route: RouteModel = RouteModel(uuid=str(uuid.uuid4()), route_name=new_route.route_name, start_time=new_route.start_time, created_at=str(dt.datetime.now().isoformat()), updated_at=str(dt.datetime.now().isoformat()), stops=new_route.stops)
        crud_result: dict = await self._route_repository.insert_one(new_route.model_dump())
        result.update({"code": 200, "success": True, "message": crud_result.get("message"), "data": {"route": new_route.model_dump()}} if crud_result.get("success") else {"code": 500, "success": False, "message": crud_result.get("message"), "error": crud_result.get("error", "Unknown error occurred")})
        return result

    async def delete_route_by_id(
            self,
            route_id: str,
    ) -> dict:
        result: dict = {"code": 0, "success": False, "message": "", "error": "", "data": {}}
        vehicle: VehicleModel = await self._vehicle_repository.get_one_by_route_uuid(route_id)
        if vehicle:
            vehicle.route_uuid = None
            _: dict = await self._vehicle_repository.update_one(vehicle)
        driver_user: DriverUserModel = await self._driver_user_repository.get_one_by_vehicle_route_uuid(route_id)
        if driver_user:
            driver_user.vehicle.route_uuid = None
            _: dict = await self._driver_user_repository.update_one(driver_user)
        crud_result: dict = await self._route_repository.delete_one_by_uuid(route_id)
        if not crud_result.get("success"):
            result.update({"code": 500, "success": False, "message": crud_result.get("message"),})
            return result
        result.update({"code": 200, "success": True, "message": crud_result.get("message")})
        return result

    async def update_route(
            self,
            updated_route: UpdateRouteModel,
    ) -> dict:
        self._logger.info(f"Updating route: {updated_route}")
        result: dict = {"code": 0, "success": False, "message": "", "error": "", "data": {}}
        existing_route: RouteModel = await self._route_repository.get_one_by_uuid(updated_route.uuid)
        if not existing_route:
            result.update({"code": 404, "success": False, "message": "Route does not exist"})
            return result
        existing_route.updated_at = str(dt.datetime.now().isoformat())
        existing_route.stops = updated_route.stops
        existing_route.start_time = updated_route.start_time
        existing_route.route_name = updated_route.route_name
        crud_result: dict = await self._route_repository.update_one(existing_route)
        if not crud_result.get("success"):
            result.update({"code": 500, "success": False, "message": crud_result.get("message"),
                           "error": crud_result.get("error", "Unknown error occurred")})
        result.update({"code": 200, "success": True, "message": crud_result.get("message"),
                       "data": {"route": updated_route.model_dump()}})
        return result

    async def get_all_routes(self) -> dict:
        self._logger.info("Getting all routes")
        result: dict = {"code": 0, "success": False, "message": "", "error": "", "data": {}}
        routes: list[RouteModel] = await self._route_repository.get_all()
        if not routes:
            result.update({"code": 404, "success": False, "message": "No routes found", "data": {"routes": []}})
            return result
        result.update({"code": 200, "success": True, "message": "Routes retrieved successfully",
                       "data": {"routes": [route.model_dump() for route in routes]}})
        return result

admin_route_management_service = AdminRouteManagementService()
