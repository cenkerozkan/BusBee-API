from pydantic import BaseModel

from ...common.db.model.lat_lon_model import LatLonModel


class NewRoute(BaseModel):
    route_name: str
    start_time: str
    stops: list[LatLonModel]

class UpdateRouteModel(BaseModel):
    uuid: str
    route_name: str
    start_time: str
    stops: list[LatLonModel]