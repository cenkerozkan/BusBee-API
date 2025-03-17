from pydantic import BaseModel

class LatLonModel(BaseModel):
    name: str
    lat: float
    lon: float