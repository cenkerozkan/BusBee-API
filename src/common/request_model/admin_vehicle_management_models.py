# src/common/request_model/admin_vehicle_management_models.py
from pydantic import BaseModel

class NewVehicleModel(BaseModel):
    vehicle_brand: str
    vehicle_model: str
    vehicle_year: int
    plate_number: str
    route_uuids: list[str] = []

class UpdateVehicleModel(BaseModel):
    uuid: str
    vehicle_brand: str
    vehicle_model: str
    vehicle_year: int
    plate_number: str
    route_uuids: list[str] = []

class DeleteVehicleModel(BaseModel):
    uuid: str

class AssignRoutesModel(BaseModel):
    vehicle_uuid: str
    route_uuids: list[str]