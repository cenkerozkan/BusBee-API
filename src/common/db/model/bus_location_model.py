from pydantic import BaseModel

class BusLocationModel(BaseModel):
    lat: float
    lon: float
    time: str