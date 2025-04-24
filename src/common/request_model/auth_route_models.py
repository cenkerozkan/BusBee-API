from pydantic import BaseModel, EmailStr

class LogoutRequest(BaseModel):
    user_uid: str

class DeleteAccountRequest(BaseModel):
    user_uid: str

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str

class ValidateRequest(BaseModel):
    refresh_token: str

class AddAdminUserModel(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str

class RemoveAdminUserModel(BaseModel):
    user_uid: str