from pydantic import BaseModel

class AdminUserModel(BaseModel):
    uid: str            # Firebase UID
    created_at: str     # This is going to be a timestamp.
    last_active: str    # This is going to be a timestamp.
    role: str = "ADMIN_USER"
    email: str