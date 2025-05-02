import uuid

from ..common.util.logger import get_logger
from ..repository.vehicle_repository import vehicle_repository
from ..repository.route_repository import route_repository
from ..repository.driver_user_repository import driver_user_repository
from ..common.db.model.vehicle_model import VehicleModel
from ..common.db.model.driver_user_model import DriverUserModel

class AdminVehicleManagementService:
    def __init__(self):
        self._logger = get_logger(__name__)
        self._vehicle_repository = vehicle_repository
        self._route_repository = route_repository
        self._driver_user_repository = driver_user_repository

    async def create_vehicle(self, new_vehicle):
        result = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }
        vehicle = VehicleModel(
            uuid=str(uuid.uuid4()),
            vehicle_brand=new_vehicle.vehicle_brand,
            vehicle_model=new_vehicle.vehicle_model,
            vehicle_year=new_vehicle.vehicle_year,
            plate_number=new_vehicle.plate_number,
            route_uuid=new_vehicle.route_uuid
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

        routes: list = await self._route_repository.get_all()
        route_map: dict = {route.uuid: route for route in routes}

        enriched_vehicles = []
        for vehicle in vehicles:
            vehicle_data = vehicle.model_dump()
            if vehicle.route_uuid and vehicle.route_uuid in route_map:
                vehicle_data["route"] = route_map[vehicle.route_uuid].model_dump()
            else:
                vehicle_data["route"] = None
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
        vehicle = VehicleModel(**updated_vehicle.model_dump())
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
        driver_crud_result: dict = await self._driver_user_repository.get_by_vehicle(vehicle_uuid=vehicle_uuid)
        if driver_crud_result.get("success"):
            result.update({
                "code": 409, "success": False,
                "message": f"Vehicle is assigned to the driver {driver_crud_result.get("data").get("first_name")} {driver_crud_result.get("data").get("last_name")}",
                "error": driver_crud_result["error"]
            })
            return result
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
        driver_crud_result: dict = await self._driver_user_repository.get_by_vehicle(plate_number=plate_number)
        if driver_crud_result.get("success"):
            result.update({
                "code": 409, "success": False,
                "message": f"Vehicle is assigned to the driver {driver_crud_result.get("data").get("first_name")} {driver_crud_result.get("data").get("last_name")}",
                "error": driver_crud_result["error"]
            })
            return result
        vehicle_crud_result: dict = await self._vehicle_repository.delete_one_by_plate(plate_number)
        if vehicle_crud_result.get("success"):
            result.update({
                "code": 200,
                "success": True,
                "message": vehicle_crud_result["message"]
            })
        else:
            result.update({
                "code": 404 if vehicle_crud_result["message"] == "Vehicle not found" else 500,
                "success": False,
                "message": vehicle_crud_result["message"],
                "error": vehicle_crud_result["error"]
            })
        return result

    async def assign_route(self, vehicle_uuid: str, route_uuid: str):
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

        # Check if vehicle already has a route
        if vehicle.route_uuid:
            result.update({
                "code": 409,
                "success": False,
                "message": "Vehicle already has a route assigned",
                "error": f"Vehicle already has route: {vehicle.route_uuid}"
            })
            return result

        # Verify route exists
        route = await self._route_repository.get_one_by_uuid(route_uuid)
        if not route:
            result.update({
                "code": 400,
                "success": False,
                "message": "Invalid route UUID provided",
                "error": f"Route not found: {route_uuid}"
            })
            return result

        # Assign route to vehicle
        vehicle.route_uuid = route_uuid
        crud_result = await self._vehicle_repository.update_one(vehicle)

        if crud_result["success"]:
            # Update driver if vehicle is assigned to one using get_by_vehicle
            driver_result = await self._driver_user_repository.get_by_vehicle(vehicle_uuid=vehicle_uuid)
            if driver_result["success"]:
                driver = DriverUserModel(**driver_result["data"])
                driver.vehicle = vehicle  # Update with new route data
                await self._driver_user_repository.update_one(driver)

            result.update({
                "code": 200,
                "success": True,
                "message": "Route assigned successfully",
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

    async def delete_route(self, vehicle_uuid: str) -> dict:
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

        # Check if vehicle has a route assigned
        if not vehicle.route_uuid:
            result.update({
                "code": 400,
                "success": False,
                "message": "Vehicle has no route assigned"
            })
            return result

        # Remove route from vehicle
        vehicle.route_uuid = None
        crud_result = await self._vehicle_repository.update_one(vehicle)

        if crud_result["success"]:
            # Update driver if vehicle is assigned to one
            driver_result = await self._driver_user_repository.get_by_vehicle(vehicle_uuid=vehicle_uuid)
            if driver_result["success"]:
                driver = DriverUserModel(**driver_result["data"])
                driver.vehicle = vehicle  # Update with removed route
                await self._driver_user_repository.update_one(driver)

            result.update({
                "code": 200,
                "success": True,
                "message": "Route removed successfully",
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