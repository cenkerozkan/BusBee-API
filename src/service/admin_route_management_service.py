import datetime as dt
import asyncio
import uuid

from starlette.routing import Route

from ..repository.route_repository import route_repository
from ..common.util.logger import get_logger
from ..common.util.error_messages import get_error_message
from ..common.request_model.admin_route_management_models import *
from ..common.db.model.route_model import RouteModel
from ..common.request_model.admin_route_management_models import *

class AdminRouteManagementService:
    __slots__ = ("_logger", "_route_repository")
    def __init__(self):
        self._logger = get_logger(__name__)
        self._route_repository = route_repository

    async def create_route(
            self,
            new_route: NewRoute,
    ) -> dict:
        self._logger.info(f"Creating new route: {new_route}")
        result: dict = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }
        new_route: RouteModel = RouteModel(
            uuid=str(uuid.uuid4()),
            route_name=new_route.route_name,
            start_time=new_route.start_time,
            created_at=str(dt.datetime.now().isoformat()),
            updated_at=str(dt.datetime.now().isoformat()),
            driver_name=None,
            driver_number=None,
            stops=new_route.stops,
        )
        crud_result: dict = await self._route_repository.insert_one(new_route.model_dump())
        if crud_result.get("success"):
            result.update({
                "code": 200,
                "success": True,
                "message": crud_result.get("message"),
                "data": {"route": new_route.model_dump()}
            })
        else:
            result.update({
                "code": 500,
                "success": False,
                "message": crud_result.get("message"),
                "error": crud_result.get("error", "Unknown error occurred"),
            })
        return result

    async def delete_route_by_id(
            self,
            route_id: str,
    ) -> dict:
        self._logger.info(f"Deleting route: {route_id}")
        result: dict = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }
        crud_result: dict = await self._route_repository.delete_one_by_uuid(route_id)
        if crud_result.get("success"):
            result.update({
                "code": 200,
                "success": True,
                "message": crud_result.get("message")
            })
        else:
            result.update({
                "code": 404 if crud_result.get("message") == "Route does not exist" else 500,
                "success": False,
                "message": crud_result.get("message"),
                "error": crud_result.get("error", "Unknown error occurred")
            })
        return result

    async def delete_route_by_name(
            self,
            route_name: str,
    ) -> dict:
        self._logger.info(f"Deleting route: {route_name}")
        result: dict = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }
        crud_result = await self._route_repository.delete_one_by_name(route_name)
        if crud_result.get("success"):
            result.update({
                "code": 200,
                "success": True,
                "message": crud_result.get("message")
            })
        else:
            result.update({
                "code": 404 if crud_result.get("message") == "Route does not exist" else 500,
                "success": False,
                "message": crud_result.get("message"),
                "error": crud_result.get("error", "Unknown error occurred")
            })
        return result

    async def update_route(
            self,
            updated_route: UpdateRouteModel,
    ) -> dict:
        self._logger.info(f"Updating route: {updated_route}")
        result: dict = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }
        updated_route.updated_at = str(dt.datetime.now().isoformat())
        crud_result: dict = await self._route_repository.update_one(updated_route)
        if crud_result.get("success"):
            result.update({
                "code": 200,
                "success": True,
                "message": crud_result.get("message"),
                "data": {"route": updated_route.model_dump()}
            })
        else:
            result.update({
                "code": 500,
                "success": False,
                "message": crud_result.get("message"),
                "error": crud_result.get("error", "Unknown error occurred")
            })
        return result

    async def get_all_routes(self) -> dict:
        self._logger.info("Getting all routes")
        result: dict = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }

        routes: list[RouteModel] = await self._route_repository.get_all()
        for i in routes:
            self._logger.info(f"Getting route: {i}")
        if routes:
            result.update({
                "code": 200,
                "success": True,
                "message": "Routes retrieved successfully",
                "data": {"routes": [route.model_dump() for route in routes]},
            })
        else:
            result.update({
                "code": 404,
                "success": False,
                "message": "No routes found",
                "data": {"routes": []},
            })

        return result

admin_route_management_service = AdminRouteManagementService()