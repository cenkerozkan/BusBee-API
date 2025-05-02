from pydantic import BaseModel
from .bus_location_model import BusLocationModel
from .vehicle_model import VehicleModel

class JournalModel(BaseModel):
    journal_date: str
    driver_name: str
    driver_last_name: str
    created_at: str
    updated_at: str
    journal_uuid: str
    journal_route: dict
    journal_vehicle: VehicleModel
    is_open: bool
    driver_uid: str
    locations: list[BusLocationModel]