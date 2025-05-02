from pydantic import BaseModel

class LocationDataModel(BaseModel):
    lat: float
    lon: float
    timestamp: str
    journal_uuid: str