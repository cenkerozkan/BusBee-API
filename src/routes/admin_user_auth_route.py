import re

from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.api_key import APIKeyHeader
from starlette.responses import JSONResponse

from ..common.request_model.auth_route_models import *
from ..common.response_model.response_model import ResponseModel
from ..common.request_model.auth_route_models import  AddAdminUserModel
from ..common.util.logger import get_logger
from ..common.util.admin_key_validator import validate_admin_api_key
from ..common.util.jwt_validator import jwt_validator
from ..common.request_model.auth_route_models import RemoveAdminUserModel

from ..service.admin_user_auth_service import admin_user_auth_service

logger = get_logger(__name__)

admin_user_auth_router = APIRouter(prefix="/auth/admin_user")

@admin_user_auth_router.post("/login", tags=["Admin User Auth"])
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

    login_result: dict = admin_user_auth_service.login(user_data.email, user_data.password)
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

@admin_user_auth_router.delete("/delete_account", tags=["Admin User Auth"])
def delete_account(
        delete_data: DeleteAccountRequest,
        is_jwt_valid: bool = Depends(jwt_validator),
) -> JSONResponse:
    if not is_jwt_valid:
        return JSONResponse(
            status_code=401,
            content=ResponseModel(success=False, message="Invalid JWT", data={},error="").model_dump())
    delete_result: bool = admin_user_auth_service.delete_account(delete_data.user_uid)
    return JSONResponse(
        status_code=200 if delete_result else 500,
        content=ResponseModel(
            success=delete_result,
            message="Account deleted" if delete_result else "Failed to delete account",
            data={},
            error=""
        ).model_dump()
    )

@admin_user_auth_router.post("/add_admin_user", tags=["Admin User Auth"])
def add_admin_user(
        user_data: AddAdminUserModel,
        is_key_valid: str = Depends(validate_admin_api_key),
) -> JSONResponse:
    logger.info(f"Add admin user request for {user_data.email}")

    if is_key_valid:
        response: dict = admin_user_auth_service.add_admin_user(
            user_data.email,
            user_data.password,
            user_data.first_name,
            user_data.last_name
        )
        return JSONResponse(
            status_code=response.get("code"),
            content=ResponseModel(
                success=response.get("success"),
                message=response.get("message"),
                data=response.get("data"),
                error=response.get("error")
            ).model_dump()
        )
    return JSONResponse(
        status_code=403,
        content=ResponseModel(
            success=False,
            message="Unauthorized",
            data={},
            error=""
        ).model_dump()
    )

@admin_user_auth_router.delete("/remove_admin_user", tags=["Admin User Auth"])
def remove_admin_user(
        user_data: RemoveAdminUserModel,
        is_key_valid: str = Depends(validate_admin_api_key),
) -> JSONResponse:
    logger.info(f"Remove admin user request for {user_data.user_uid}")

    if is_key_valid:
        response: dict = admin_user_auth_service.remove_admin_user(
            user_data.user_uid
        )
        return JSONResponse(
            status_code=response.get("code"),
            content=ResponseModel(
                success=response.get("success"),
                message=response.get("message"),
                data=response.get("data"),
                error=response.get("error")
            ).model_dump()
        )
    return JSONResponse(
        status_code=403,
        content=ResponseModel(
            success=False,
            message="Unauthorized",
            data={},
            error=""
        ).model_dump()
    )

@admin_user_auth_router.get("/get_all_admins", tags=["Admin User Auth"])
async def get_all_admins(is_key_valid: str = Depends(validate_admin_api_key)) -> JSONResponse:
    logger.info(f"is key valid: {is_key_valid}")
    if is_key_valid:
        response: dict = await admin_user_auth_service.get_all_admins()
        return JSONResponse(
            status_code=response.get("code"),
            content=ResponseModel(
                success=response.get("success"),
                message=response.get("message"),
                data=response.get("data"),
                error=response.get("error")
            ).model_dump()
        )

    return JSONResponse(
        status_code=403,
        content=ResponseModel(success=False,message="Unauthorized",data={},error="").model_dump())

@admin_user_auth_router.patch("/update_admin_user", tags=["Admin User Auth"])
async def update_admin_user(
        update_admin_user: UpdateAdminUserModel,
        is_key_valid: str = Depends(validate_admin_api_key)
) -> JSONResponse:
    logger.info(f"Update admin user request for {update_admin_user.uid}")
    if is_key_valid:
        email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not re.match(email_pattern, update_admin_user.email):
            return JSONResponse(
                status_code=400,
                content=ResponseModel(success=False,message="Hatalı Mail Formatı",data={},error="").model_dump()
            )

        response: dict = await admin_user_auth_service.update_admin_user(**update_admin_user.model_dump())
        return JSONResponse(
            status_code=response.get("code"),
            content=ResponseModel(
                success=response.get("success"),
                message=response.get("message"),
                data=response.get("data"),
                error=response.get("error")
            ).model_dump()
        )

    return JSONResponse(
        status_code=403,
        content=ResponseModel(success=False,message="Unauthorized",data={},error="").model_dump())