from pydantic import BaseModel


class FetchVehicleLocationModel(BaseModel):
    journal_uuid: str