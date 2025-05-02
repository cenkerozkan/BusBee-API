# src/common/request_model/admin_vehicle_management_models.py
from pydantic import BaseModel

class NewVehicleModel(BaseModel):
    vehicle_brand: str
    vehicle_model: str
    vehicle_year: int
    plate_number: str
    route_uuid: str | None = None

class UpdateVehicleModel(BaseModel):
    uuid: str
    vehicle_brand: str
    vehicle_model: str
    vehicle_year: int
    plate_number: str
    route_uuid: str | None = None

class DeleteVehicleModel(BaseModel):
    uuid: str

class AssignRouteModel(BaseModel):
    vehicle_uuid: str
    route_uuid: str