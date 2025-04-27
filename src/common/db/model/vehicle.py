# src/common/db/model/vehicle.py
from pydantic import BaseModel

class Vehicle(BaseModel):
    uuid: str
    vehicle_brand: str
    vehicle_model: str
    vehicle_year: int
    plate_number: str
    route_uuids: list[str] = []