import datetime as dt
import uuid

from ..common.db.model.bus_location_model import BusLocationModel
from ..common.db.model.journal_model import JournalModel
from ..common.db.model.vehicle_model import VehicleModel
from ..common.request_model.driver_models import LocationDataModel
from ..common.util.logger import get_logger
from ..repository.driver_user_repository import driver_user_repository
from ..repository.vehicle_repository import vehicle_repository
from ..repository.route_repository import route_repository
from ..repository.journal_repository import journal_repository
from ..common.db.model.driver_user_model import DriverUserModel
from ..common.db.model.route_model import RouteModel

logger = get_logger(__name__)

# To make it faster.
_JOURNAL_CACHE: dict = {}

class DriverUserService:
    def __init__(self):
        self._logger = logger
        self._driver_user_repository = driver_user_repository
        self._vehicle_repository = vehicle_repository
        self._route_repository = route_repository
        self._journal_repository = journal_repository

    async def get_vehicle(
            self,
            driver_uid: str
    ) -> dict:
        self._logger.info(f"Get driver vehicle {driver_uid}")
        result: dict = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }
        driver = await self._driver_user_repository.get_one_by_uid(driver_uid)
        if not driver:
            self._logger.info(f"Driver {driver_uid} not found")
            result.update({"code": 404, "success": False, "message": "Driver not found"})
            return result

        if not driver.vehicle:
            self._logger.info(f"Driver {driver_uid} does not have a vehicle assigned")
            result.update({"code": 404, "success": False, "message": "Driver is not assigned to a vehicle"})
            return result

        vehicle = await self._vehicle_repository.get_all()
        vehicle = next((v for v in vehicle if v.uuid == driver.vehicle.uuid), None)
        if not vehicle:
            self._logger.info(f"Vehicle {driver.vehicle.uuid} not found")
            result.update({"code": 404, "success": False, "message": "Vehicle not found"})
            return result

        result.update({"code": 200, "success": True, "message": "Vehicle retrieved successfully", "data": vehicle.model_dump()})
        return result

    async def get_driver_information(
            self,
            driver_uid: str
    ) -> dict:
        self._logger.info(f"Get driver information {driver_uid}")
        result: dict = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }
        driver: DriverUserModel = await self._driver_user_repository.get_one_by_uid(driver_uid)
        if not driver:
            result.update({"code": 404, "success": False, "message": "Driver not found"})
            return result

        result.update({
            "code": 200, "success": True, "message": "Driver information retrieved successfully", "data": driver.model_dump()
        })
        return result

    async def get_active_journal_by_uid(
            self,
            driver_uid: str
    ) -> dict:
        self._logger.info(f"Get active journal for driver {driver_uid}")
        result: dict = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }
        journal: JournalModel = await self._journal_repository.get_active_one_by_driver_uid(driver_uid)
        if not journal:
            result.update({"code": 404, "success": False, "message": "No active journal found"})
            return result

        result.update({
            "code": 200, "success": True, "message": "Active journal retrieved successfully", "data": journal.model_dump()
        })
        return result

    async def get_vehicle_route(
            self,
            driver_uid: str
    ) -> dict:
        self._logger.info(f"Get driver vehicle route {driver_uid}")
        result: dict = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }
        # Check if there is a journal for

        driver: DriverUserModel = await self._driver_user_repository.get_one_by_uid(driver_uid)
        if not driver:
            result.update({"code": 404, "success": False, "message": "Driver not found"})
            return result

        if not driver.vehicle:
            result.update({"code": 404, "success": False, "message": "Driver is not assigned to a vehicle"})
            return result

        if not driver.vehicle.route_uuid:
            result.update({"code": 404, "success": False, "message": "Vehicle is not assigned to a route"})
            return result

        vehicles: list = await self._vehicle_repository.get_all()
        vehicle = next((v for v in vehicles if v.uuid == driver.vehicle.uuid), None)
        if not vehicle:
            result.update({"code": 404, "success": False, "message": "Vehicle not found"})
            return result

        route: RouteModel = await self._route_repository.get_one_by_uuid(driver.vehicle.route_uuid)

        result.update({
            "code": 200, "success": True, "message": "Vehicle routes retrieved successfully", "data": {"route": route.model_dump()}
        })
        return result

    async def start_journey(
            self,
            driver_uid: str,
    ) -> dict:
        result: dict = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }
        driver: DriverUserModel
        driver_vehicle: VehicleModel
        vehicle_route: RouteModel
        new_journal: JournalModel

        # Check if driver has an assigned vehicle.
        driver = await self._driver_user_repository.get_one_by_uid(driver_uid)
        if driver.vehicle == None:
            self._logger.info(f"Driver {driver_uid} does not have a vehicle assigned")
            result.update({"code": 404, "success": False, "message": "Bu şoföre atanmış bir araç bulunamadı"})
            return result

        # Check if vehicle has an assigned route.
        driver_vehicle = await self._vehicle_repository.get_one_by_uuid(driver.vehicle.uuid)
        vehicle_route = await self._route_repository.get_one_by_uuid(driver_vehicle.route_uuid)
        if not vehicle_route:
            self._logger.info(f"Vehicle {driver_vehicle.uuid} does not have a route assigned")
            result.update({"code": 404, "success": False, "message": "Bu araca atanmış herhangi bir rota bulunamadı"})
            return result

        # Check if that vehicle is already on road.
        if driver_vehicle.is_started:
            self._logger.info(f"Vehicle {driver_vehicle.uuid} is already on road")
            result.update({"code": 400, "success": False, "message": "Bu araç zaten yolda"})
            return result


        # Create a new journal object and insert it.
        new_journal = JournalModel(
            journal_date=dt.datetime.today().strftime("%d-%m-%Y"),
            driver_name=driver.first_name,
            driver_last_name=driver.last_name,
            created_at=str(dt.datetime.now().isoformat()),
            updated_at=str(dt.datetime.now().isoformat()),
            journal_uuid=str(uuid.uuid4()),
            journal_route=vehicle_route.model_dump(),
            journal_vehicle=driver_vehicle.model_dump(),
            is_open=True,
            driver_uid=driver.uid,
            locations=[]
        )
        self._logger.info(f"New journal {new_journal}")

        # Insert the new journal into the DB.
        journal_crud_result: dict = await self._journal_repository.insert_one(new_journal)
        if not journal_crud_result.get("success"):
            self._logger.error(f"SOMETHING FUCKED UP !!, Error: {journal_crud_result.get('error')}")
            result.update({"code": 500, "success": False, "message": "Failed to create journal", "error": journal_crud_result.get("error")})
            return result

        # Update is_started flag to true.
        driver_vehicle.is_started = True # This is the
        driver.vehicle.is_started = True
        is_vehicle_updated: dict = await self._vehicle_repository.update_one(driver_vehicle)
        is_driver_updated: dict = await self._driver_user_repository.update_one(driver)
        if not is_vehicle_updated.get("success") and not is_driver_updated.get("success"):
            self._logger.error(f"SOMETHING FUCKED UP!!, Errors Are: {is_vehicle_updated.get('error')}, {is_driver_updated.get('error')}")
            await self._route_repository.delete_one(driver_vehicle.route_uuid)
            result.update({"code": 500, "success": False, "message": "Failed to update vehicle", "error": is_vehicle_updated.get("error")})

        # Success
        result.update({"code": 200, "success": True, "message": "Journey started successfully", "data": {"journal": new_journal.model_dump()}})
        return result

    async def stop_journey(
            self,
            driver_uid: str,
            journal_uuid: str
    ) -> dict:
        self._logger.info(f"Stop journal for driver {driver_uid} and journal id {journal_uuid}")
        result: dict = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }
        driver: DriverUserModel
        drivers_vehicle: VehicleModel
        journal: JournalModel

        # Check if journal exists.
        journal = await self._journal_repository.get_one_by_uuid(journal_uuid)
        if not journal:
            self._logger.info(f"Journal {journal_uuid} not found")
            result.update({"code": 404, "success": False, "message": "Böyle bir yolculuk kaydı bulunmamaktadır."})
            return result

        # Check if driver has an assigned vehicle.
        driver = await self._driver_user_repository.get_one_by_uid(driver_uid)
        if driver.vehicle == None:
            self._logger.info(f"Driver {driver_uid} does not have a vehicle assigned")
            result.update({"code": 404, "success": False, "message": "Bu şoföre atanmış bir araç bulunamadı"})
            return result

        # Retrieve drivers_vehicle and update it's status.
        drivers_vehicle = await self._vehicle_repository.get_one_by_uuid(driver.vehicle.uuid)
        if not drivers_vehicle.is_started:
            self._logger.info(f"Vehicle {drivers_vehicle.uuid} is not on road")
            result.update({"code": 400, "success": False, "message": "Bu araç zaten durdurulmuş"})
            return result


        drivers_vehicle.is_started = False
        driver.vehicle.is_started = False
        journal.is_open = False
        is_vehicle_updated: dict = await self._vehicle_repository.update_one(drivers_vehicle)
        is_driver_updated: dict = await self._driver_user_repository.update_one(driver)
        is_journal_updated: dict = await self._journal_repository.update_one(journal)
        if not is_vehicle_updated.get("success") and not is_driver_updated.get("success") and not is_journal_updated.get("success"):
            self._logger.error(f"SOMETHING FUCKED UP!!, Errors Are: {is_vehicle_updated.get('error')}, {is_driver_updated.get('error')}, {is_journal_updated.get('error')}")
            result.update({"code": 500, "success": False, "message": "Failed to update vehicle", "error": is_vehicle_updated.get("error")})
            return result

        result.update({"code": 200, "success": True, "message": "Journey stopped successfully"})
        return result

    async def update_journal(
            self,
            journal_uuid: str,
            location: BusLocationModel
    ) -> dict:
        result: dict = {
            "code": 0,
            "success": False,
            "message": "",
            "error": "",
            "data": {}
        }
        self._logger.info(f"Updating journal with UUID: {journal_uuid} and location: {location}")
        journal: JournalModel

        # Check if journal exists.
        journal = await self._journal_repository.get_one_by_uuid(journal_uuid)
        if not journal:
            self._logger.info(f"Journal {journal_uuid} not found")
            result.update({"code": 404, "success": False, "message": "Böyle bir yolculuk kaydı bulunmamaktadır."})
            return result

        # Check if journal is open.
        if not journal.is_open:
            self._logger.info(f"Journal {journal_uuid} is not open")
            result.update({"code": 400, "success": False, "message": "Bu yolculuk, artık açık değil."})
            return result

        # Append location to journal.
        journal.locations.append(location.model_dump())
        journal.updated_at = str(dt.datetime.now().isoformat())
        journal_crud_result: dict = await self._journal_repository.update_one(journal)
        if not journal_crud_result.get("success"):
            self._logger.error(f"SOMETHING FUCKED UP!!, Error: {journal_crud_result.get('error')}")
            result.update({"code": 500, "success": False, "message": "Yolculuk kaydı güncellenirken bir hata meydana geldi.", "error": journal_crud_result.get("error")})
            return result

        result.update({"code": 200, "success": True})
        return result


driver_service = DriverUserService()
