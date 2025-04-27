from .route_model import RouteModel
from pydantic import BaseModel

class EndUserModel(BaseModel):
    uid: str            # Firebase UID
    created_at: str     # This is going to be a timestamp.
    last_active: str    # This is going to be a timestamp.
    role: str = "END_USER"
    email: str
    first_name: str = ""
    last_name: str = ""