from pydantic import BaseModel
from .vehicle_model import VehicleModel

class DriverUserModel(BaseModel):
    uid: str            # Firebase UID
    first_name: str
    last_name: str
    phone_number: str
    role: str = "DRIVER_USER"
    vehicle: VehicleModel | None = None