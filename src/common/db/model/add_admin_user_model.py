from pydantic import BaseModel

class AddAdminUserModel(BaseModel):
    email: str
    password: str