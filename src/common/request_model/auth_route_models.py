from pydantic import BaseModel

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

class UpdateAdminUserModel(BaseModel):
    uid: str
    first_name: str
    last_name: str
    email: str

class RemoveAdminUserModel(BaseModel):
    user_uid: str

# For end users.
class CreateAccountRequest(BaseModel):
    uid: str
    email: str
    first_name: str
    last_name: str