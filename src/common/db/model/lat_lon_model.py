from pydantic import BaseModel

class LatLonModel(BaseModel):
    lat: float
    lon: float