import datetime as dt

from pydantic import BaseModel

from .lat_lon_model import LatLonModel

class RouteModel(BaseModel):
    uuid: str
    route_name: str
    created_at: str
    updated_at: str
    start_time: str
    stops: list[LatLonModel]