# src/service/admin_vehicle_management_service.py
import uuid

from ..common.util.logger import get_logger
from ..repository.vehicle_repository import vehicle_repository
from ..repository.route_repository import route_repository
from ..common.db.model.vehicle import Vehicle

class AdminVehicleManagementService:
    def __init__(self):
        self._logger = get_logger(__name__)
        self._vehicle_repository = vehicle_repository
        self._route_repository = route_repository

    async def create_vehicle(self, new_vehicle):
        result = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }
        vehicle = Vehicle(
            uuid=str(uuid.uuid4()),
            vehicle_brand=new_vehicle.vehicle_brand,
            vehicle_model=new_vehicle.vehicle_model,
            vehicle_year=new_vehicle.vehicle_year,
            plate_number=new_vehicle.plate_number,
            route_uuids=new_vehicle.route_uuids
        )
        crud_result = await self._vehicle_repository.insert_one(vehicle.model_dump())
        if crud_result["success"]:
            result.update({
                "code": 200,
                "success": True,
                "message": crud_result["message"],
                "data": {"vehicle": vehicle.model_dump()}
            })
        else:
            result.update({
                "code": 500,
                "success": False,
                "message": crud_result["message"],
                "error": crud_result["error"]
            })
        return result

    async def get_all_vehicles(self):
        result = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }
        vehicles = await self._vehicle_repository.get_all()
        if not vehicles:
            result.update({
                "code": 404,
                "success": False,
                "message": "No vehicles found",
                "data": {"vehicles": []}
            })
            return result

        routes = await self._route_repository.get_all()
        route_map = {route.uuid: route for route in routes}

        enriched_vehicles = []
        for vehicle in vehicles:
            vehicle_data = vehicle.model_dump()
            assigned_routes = []
            for route_uuid in vehicle.route_uuids:
                if route := route_map.get(route_uuid):
                    assigned_routes.append(route.model_dump())
            vehicle_data["routes"] = assigned_routes
            enriched_vehicles.append(vehicle_data)

        result.update({
            "code": 200,
            "success": True,
            "message": "Vehicles retrieved successfully",
            "data": {"vehicles": enriched_vehicles}
        })
        return result

    async def update_vehicle(self, updated_vehicle):
        result = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }
        vehicle = Vehicle(**updated_vehicle.model_dump())
        crud_result = await self._vehicle_repository.update_one(vehicle)
        if crud_result["success"]:
            result.update({
                "code": 200,
                "success": True,
                "message": crud_result["message"],
                "data": {"vehicle": vehicle.model_dump()}
            })
        else:
            result.update({
                "code": 404 if crud_result["message"] == "Vehicle does not exist" else 500,
                "success": False,
                "message": crud_result["message"],
                "error": crud_result["error"]
            })
        return result

    async def delete_vehicle(self, vehicle_uuid):
        result = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }
        crud_result: dict = await self._vehicle_repository.delete_one(vehicle_uuid)
        if crud_result.get("success"):
            result.update({
                "code": 200,
                "success": True,
                "message": crud_result["message"]
            })
        else:
            result.update({
                "code": 404 if crud_result["message"] == "Vehicle not found" else 500,
                "success": False,
                "message": crud_result["message"],
                "error": crud_result["error"]
            })
        return result

    async def delete_vehicle_by_plate(self, plate_number):
        result = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }
        crud_result: dict = await self._vehicle_repository.delete_one_by_plate(plate_number)
        if crud_result.get("success"):
            result.update({
                "code": 200,
                "success": True,
                "message": crud_result["message"]
            })
        else:
            result.update({
                "code": 404 if crud_result["message"] == "Vehicle not found" else 500,
                "success": False,
                "message": crud_result["message"],
                "error": crud_result["error"]
            })
        return result

    async def assign_routes(self, vehicle_uuid, route_uuids):
        result = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }
        # Get vehicle
        vehicles = await self._vehicle_repository.get_all()
        vehicle = next((v for v in vehicles if v.uuid == vehicle_uuid), None)
        if not vehicle:
            result.update({
                "code": 404,
                "success": False,
                "message": "Vehicle not found"
            })
            return result

        # Check for duplicate routes
        # This is a nice way of handling duplicates.
        duplicate_routes = set(vehicle.route_uuids) & set(route_uuids)
        if duplicate_routes:
            result.update({
                "code": 409,
                "success": False,
                "message": "Routes already assigned",
                "error": f"Routes already assigned to vehicle: {list(duplicate_routes)}"
            })
            return result

        # Verify routes exist
        routes = await self._route_repository.get_all()
        route_map = {route.uuid: route for route in routes}
        invalid_routes = [uuid for uuid in route_uuids if uuid not in route_map]
        if invalid_routes:
            result.update({
                "code": 400,
                "success": False,
                "message": "Invalid route UUIDs provided",
                "error": f"Routes not found: {invalid_routes}"
            })
            return result

        # Update vehicle routes
        vehicle.route_uuids = route_uuids
        crud_result = await self._vehicle_repository.update_one(vehicle)

        if crud_result["success"]:
            result.update({
                "code": 200,
                "success": True,
                "message": "Routes assigned successfully",
                "data": {"vehicle": vehicle.model_dump()}
            })
        else:
            result.update({
                "code": 500,
                "success": False,
                "message": crud_result["message"],
                "error": crud_result["error"]
            })
        return result

admin_vehicle_management_service = AdminVehicleManagementService()