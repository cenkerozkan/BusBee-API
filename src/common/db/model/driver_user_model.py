from pydantic import BaseModel
from .vehicle import Vehicle

class DriverUserModel(BaseModel):
    uid: str            # Firebase UID
    first_name: str
    last_name: str
    phone_number: str
    role: str = "DRIVER_USER"
    assigned_route: dict = {}
    vehicle: Vehicle | None = None