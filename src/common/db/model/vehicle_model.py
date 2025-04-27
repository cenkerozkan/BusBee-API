from pydantic import BaseModel

class VehicleModel(BaseModel):
    uuid: str
    vehicle_brand: str
    vehicle_model: str
    vehicle_year: int
    plate_number: str
    is_started: bool = False # This is a flag variable indicates if a route is started or not.
    route_uuids: list[str] = []