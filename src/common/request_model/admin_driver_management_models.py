from pydantic import BaseModel

class AddDriverUserModel(BaseModel):
    first_name: str
    last_name: str
    phone_number: str

class DeleteDriverUserModel(BaseModel):
    uid: str

class UpdateDriverPhoneNumberModel(BaseModel):
    uid: str
    new_phone_number: str