import re

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from ..common.request_model.auth_route_models import *
from ..common.response_model.response_model import ResponseModel
from ..common.util.logger import get_logger
from ..common.util.jwt_validator import jwt_validator
from ..common.util.vehicle_state_validator import validate_vehicle_state
from ..common.request_model.admin_driver_management_models import *

from ..service.admin_driver_management_service import admin_management_service

logger = get_logger(__name__)

admin_driver_management_router = APIRouter(prefix="/admin/management", tags=["Admin Driver Management"])

@admin_driver_management_router.get("/get_all_drivers", tags=["Admin Driver Management"])
async def get_all_drivers(
        is_jwt_valid: bool = Depends(jwt_validator),
) -> JSONResponse:
    logger.info("Get all drivers request")
    result: dict = await admin_management_service.get_all_drivers()
    if not is_jwt_valid:
        return JSONResponse(
            status_code=401,
            content=ResponseModel(success=False, message="Invalid JWT", data={},error="").model_dump())
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=""
        ).model_dump()
    )

@admin_driver_management_router.post("/add_driver", tags=["Admin Driver Management"])
def add_driver(
        driver_data: AddDriverUserModel,
        is_jwt_valid: bool = Depends(jwt_validator)
) -> JSONResponse:
    if not is_jwt_valid:
        return JSONResponse(
            status_code=401,
            content=ResponseModel(success=False, message="Invalid JWT", data={},error="").model_dump())
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
async def delete_driver(
        driver_data: DeleteDriverUserModel,
        is_jwt_valid: bool = Depends(jwt_validator)
) -> JSONResponse:
    if not is_jwt_valid:
        return JSONResponse(
            status_code=401,
            content=ResponseModel(success=False, message="Invalid JWT", data={},error="").model_dump())
    is_vehicle_on_route: bool = await validate_vehicle_state(driver_uid=driver_data.uid)
    if is_vehicle_on_route:
        return JSONResponse(
            status_code=409,
            content=ResponseModel(success=False, message="Araç yolculuk yaparken değişiklik yapamazsınız",
                                  data={}, error="").model_dump())
    logger.info(f"Delete driver request for phone number: {driver_data.uid}")
    result: bool = await admin_management_service.delete_driver(driver_data.uid)
    return JSONResponse(
        status_code= 200 if result is True else 500,
        content=ResponseModel(
            success=result,
            message="Driver user deleted" if result is True else "Failed to delete driver user",
            data={},
            error=""
        ).model_dump()
)

@admin_driver_management_router.patch("/update_driver_phone_number", tags=["Admin Driver Management"])
async def update_driver_phone_number(
        driver_data: UpdateDriverPhoneNumberModel,
        is_jwt_valid: bool = Depends(jwt_validator)
) -> JSONResponse:
    if not is_jwt_valid:
        return JSONResponse(
            status_code=401,
            content=ResponseModel(success=False, message="Invalid JWT", data={},error="").model_dump())
    is_vehicle_on_route: bool = await validate_vehicle_state(driver_uid=driver_data.uid)
    if is_vehicle_on_route:
        return JSONResponse(
            status_code=409,
            content=ResponseModel(success=False, message="Araç yolculuk yaparken değişiklik yapamazsınız",
                                  data={}, error="").model_dump())
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

@admin_driver_management_router.patch("/assign_vehicle_to_driver", tags=["Admin Driver Management"])
async def assign_vehicle_to_driver(
        assignment_data: AssignVehicleToDriverModel,
        is_jwt_valid: bool = Depends(jwt_validator)
) -> JSONResponse:
    if not is_jwt_valid:
        return JSONResponse(
            status_code=401,
            content=ResponseModel(success=False, message="Invalid JWT", data={},error="").model_dump())
    is_vehicle_on_route: bool = await validate_vehicle_state(vehicle_uuid=assignment_data.vehicle_uuid)
    if is_vehicle_on_route:
        return JSONResponse(
            status_code=409,
            content=ResponseModel(success=False, message="Araç yolculuk yaparken değişiklik yapamazsınız",
                                  data={}, error="").model_dump())
    logger.info(f"Assign vehicle request for driver UID: {assignment_data.driver_uid} and vehicle UUID: {assignment_data.vehicle_uuid}")
    result: dict = await admin_management_service.assign_vehicle_to_driver(
        assignment_data.driver_uid,
        assignment_data.vehicle_uuid
    )
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )

@admin_driver_management_router.patch("/remove_vehicle_from_driver/{driver_uid}", tags=["Admin Driver Management"])
async def remove_vehicle_from_driver(
        driver_uid: str,
        is_jwt_valid: bool = Depends(jwt_validator)
) -> JSONResponse:
    if not is_jwt_valid:
        return JSONResponse(
            status_code=401,
            content=ResponseModel(success=False, message="Invalid JWT", data={},error="").model_dump())
    is_vehicle_on_route: bool = await validate_vehicle_state(driver_uid=driver_uid)
    if is_vehicle_on_route:
        return JSONResponse(
            status_code=409,
            content=ResponseModel(success=False, message="Araç yolculuk yaparken değişiklik yapamazsınız",
                                  data={}, error="").model_dump())
    logger.info(f"Remove vehicle from driver request for driver UID: {driver_uid}")
    result: dict = await admin_management_service.remove_vehicle_from_driver(driver_uid)
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )