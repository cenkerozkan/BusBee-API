import re
import asyncio

from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..common.request_model.auth_route_models import *
from ..service.end_user_auth_service import EndUserAuthService
from ..common.response_model.response_model import ResponseModel
from ..common.util.background_tasks import delete_unverified_email
from ..common.util.logger import get_logger
from ..common.util.jwt_validator import jwt_validator  # Import the validator

from ..service.end_user_auth_service import end_user_auth_service

logger = get_logger(__name__)

end_user_auth_router = APIRouter(prefix="/auth/end_user")

@end_user_auth_router.post("/login", tags=["End User Auth"])
def login(
        user_data: LoginRequest
) -> JSONResponse:
    logger.info(f"Login request for {user_data.email}")

    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if not re.match(email_pattern, user_data.email):
        return JSONResponse(
            status_code=400,
            headers={},
            content=ResponseModel(
                success=False,
                message="Invalid email format",
                data={},
                error=""
            ).model_dump()
        )

    login_result:dict = end_user_auth_service.login(user_data.email, user_data.password)
    return JSONResponse(
        status_code=login_result.get("code"),
        headers={"refresh_token": login_result.get("refresh_token"),
                 "id_token": login_result.get("id_token")},
        content=ResponseModel(
            success=login_result.get("success"),
            message=login_result.get("message"),
            data=login_result.get("data"),
            error=login_result.get("error")
        ).model_dump()
    )

@end_user_auth_router.post("/register", tags=["End User Auth"])
def register(
        user_data: LoginRequest,
        background_tasks: BackgroundTasks
) -> JSONResponse:
    logger.info(f"Register request for {user_data.email}")
    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if not re.match(email_pattern, user_data.email):
        return JSONResponse(
            status_code=400,
            content=ResponseModel(
                success=False,
                message="Invalid email format",
                data={},
                error=""
            ).model_dump()
        )

    register_result: dict = end_user_auth_service.register(user_data.email, user_data.password)
    # If success
    if register_result.get("success"):
        background_tasks.add_task(delete_unverified_email, user_data.email)
    return JSONResponse(
        status_code=register_result.get("code"),
        headers={"refresh_token": register_result.get("refresh_token"),
                 "id_token": register_result.get("id_token")},
        content=ResponseModel(
            success=register_result.get("success"),
            message=register_result.get("message"),
            data=register_result.get("data"),
            error=register_result.get("error")
        ).model_dump()
    )

@end_user_auth_router.delete("/delete_account", tags=["End User Auth"])
def delete_account(
        delete_data: DeleteAccountRequest,
        is_jwt_valid: bool = Depends(jwt_validator),  # Apply JWT dependency
) -> JSONResponse:
    if not is_jwt_valid:
        return JSONResponse(
            status_code=401,
            content=ResponseModel(success=False, message="Invalid JWT", data={},error="").model_dump())
    logger.info(f"Delete account request for user UID: {delete_data.user_uid}")
    delete_result: bool = end_user_auth_service.delete_account(delete_data.user_uid)
    return JSONResponse(
        status_code=200 if delete_result else 500,
        content=ResponseModel(
            success=delete_result,
            message="Account deleted" if delete_result else "Failed to delete account",
            data={},
            error=""
        ).model_dump()
    )

@end_user_auth_router.post("/validate_token", tags=["End User Auth"])
def validate_token(
        is_jwt_valid: bool = Depends(jwt_validator),  # Apply JWT dependency
) -> JSONResponse:
    if not is_jwt_valid:
        return JSONResponse(
            status_code=401,
            content=ResponseModel(success=False, message="Invalid JWT", data={},error="").model_dump())
    # The JWT is already validated by the dependency, so we can proceed.
    # The original code was extracting and then re-validating.
    return JSONResponse(
        status_code=200,
        content=ResponseModel(
            success=True,
            message="Token is valid",
            data={},
            error=""
        ).model_dump()
    )

@end_user_auth_router.post("/create_user", tags=["End User Auth"])
async def create_account(
        user_data: CreateAccountRequest,
        is_jwt_valid: bool = Depends(jwt_validator),  # Apply JWT dependency
) -> JSONResponse:
    if not is_jwt_valid:
        return JSONResponse(
            status_code=401,
            content=ResponseModel(success=False, message="Invalid JWT", data={},error="").model_dump())
    logger.info(f"Create account request for {user_data.email}")
    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if not re.match(email_pattern, user_data.email):
        return JSONResponse(
            status_code=400,
            content=ResponseModel(
                success=False,
                message="Invalid email format",
                data={},
                error=""
            ).model_dump()
        )

    create_result: dict = await end_user_auth_service.create_account(user_data.uid, user_data.email,
                                                                     user_data.first_name, user_data.last_name)
    return JSONResponse(
        status_code=create_result.get("code"),
        content=ResponseModel(
            success=create_result.get("success"),
            message=create_result.get("message"),
            data=create_result.get("data"),
            error=create_result.get("error")
        ).model_dump()
    )