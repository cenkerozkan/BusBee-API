from pydantic import BaseModel

class AddDriverUserModel(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    password: str
    assigned_route: dict

class DeleteDriverUserModel(BaseModel):
    uid: str

class UpdateDriverPasswordModel(BaseModel):
    uid: str
    new_password: str

class UpdateDriverPhoneNumberModel(BaseModel):
    uid: str
    new_phone_number: str