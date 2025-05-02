from pydantic import BaseModel

class VehicleModel(BaseModel):
    uuid: str
    vehicle_brand: str
    vehicle_model: str
    vehicle_year: int
    plate_number: str
    is_started: bool = False
    route_uuid: str | None = None