import re

from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.api_key import APIKeyHeader

from ..common.request_model.auth_route_models import *
from ..common.response_model.response_model import ResponseModel
from ..common.util.logger import get_logger
from ..common.util.get_admin_api_key import validate_admin_api_key
from ..common.request_model.admin_driver_management_models import *

from ..service.admin_driver_management_service import admin_management_service

logger = get_logger(__name__)

admin_driver_management_router = APIRouter(prefix="/admin/management", tags=["Admin Driver Management"])

@admin_driver_management_router.get("/get_all_drivers", tags=["Admin Driver Management"])
async def get_all_drivers(
        jwt: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> JSONResponse:
    logger.info("Get all drivers request")
    result: dict = await admin_management_service.get_all_drivers()
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message="Drivers retrieved",
            data=result.get("data"),
            error=""
        ).model_dump()
    )

@admin_driver_management_router.post("/add_driver", tags=["Admin Driver Management"])
def add_driver(
        driver_data: AddDriverUserModel,
        jwt: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> JSONResponse:
    logger.info(f"Add driver request for name: {driver_data.first_name} {driver_data.last_name}")
    if not re.match(r'^(?:\+90|0)?[1-9][0-9]{9}$', driver_data.phone_number):
        return JSONResponse(
            status_code=400,
            content=ResponseModel(
                success=False,
                message="Invalid phone number format",
                data={},
                error=""
            ).model_dump()
        )
    result: dict = admin_management_service.add_driver(driver_data)
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )

@admin_driver_management_router.delete("/delete_driver", tags=["Admin Driver Management"])
def delete_driver(
        driver_data: DeleteDriverUserModel,
        jwt: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> JSONResponse:
    logger.info(f"Delete driver request for phone number: {driver_data.uid}")
    result: bool = admin_management_service.delete_driver(driver_data.uid)
    return JSONResponse(
        status_code= 200 if result is True else 500,
        content=ResponseModel(
            success=result,
            message="Driver user deleted" if result is True else "Failed to delete driver user",
            data={},
            error=""
        ).model_dump()
)

@admin_driver_management_router.patch("/update_driver_password", tags=["Admin Driver Management"])
def update_driver_password(
        driver_data: UpdateDriverPasswordModel,
        jwt: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> JSONResponse:
    logger.info(f"Update driver password request for driver uid: {driver_data.uid}")
    result: dict = admin_management_service.update_driver_password(driver_data.uid, driver_data.new_password)
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )

@admin_driver_management_router.patch("/update_driver_phone_number", tags=["Admin Driver Management"])
def update_driver_phone_number(
        driver_data: UpdateDriverPhoneNumberModel,
        jwt: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> JSONResponse:
    logger.info(f"Update driver phone number request for driver uid: {driver_data.uid}")
    result: dict = admin_management_service.update_driver_phone_number(driver_data.uid, driver_data.new_phone_number)
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )