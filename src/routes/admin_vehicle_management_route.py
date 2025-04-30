# src/routes/admin_vehicle_management_route.py
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..common.request_model.admin_vehicle_management_models import *
from ..common.response_model.response_model import ResponseModel
from ..common.util.logger import get_logger
from ..service.admin_vehicle_management_service import admin_vehicle_management_service

logger = get_logger(__name__)

admin_vehicle_management_router = APIRouter(prefix="/admin/management/vehicle", tags=["Admin Vehicle Management"])

@admin_vehicle_management_router.post("/create", tags=["Admin Vehicle Management"])
async def create_vehicle(
        vehicle_data: NewVehicleModel,
        jwt: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> JSONResponse:
    logger.info(f"Create vehicle request for plate number: {vehicle_data.plate_number}")
    result = await admin_vehicle_management_service.create_vehicle(vehicle_data)
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )

@admin_vehicle_management_router.get("/get_all", tags=["Admin Vehicle Management"])
async def get_all_vehicles(
        jwt: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> JSONResponse:
    logger.info("Get all vehicles request")
    result = await admin_vehicle_management_service.get_all_vehicles()
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )

@admin_vehicle_management_router.patch("/update", tags=["Admin Vehicle Management"])
async def update_vehicle(
        vehicle_data: UpdateVehicleModel,
        jwt: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> JSONResponse:
    logger.info(f"Update vehicle request for uuid: {vehicle_data.uuid}")
    result = await admin_vehicle_management_service.update_vehicle(vehicle_data)
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )

@admin_vehicle_management_router.delete("/delete/{vehicle_uuid}", tags=["Admin Vehicle Management"])
async def delete_vehicle(
        vehicle_uuid: str,
        jwt: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> JSONResponse:
    logger.info(f"Delete vehicle request for uuid: {vehicle_uuid}")
    result = await admin_vehicle_management_service.delete_vehicle(vehicle_uuid)
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )

@admin_vehicle_management_router.delete("/delete_by_plate/{plate_number}", tags=["Admin Vehicle Management"])
async def delete_vehicle_by_plate(
        plate_number: str,
        jwt: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> JSONResponse:
    logger.info(f"Delete vehicle request for plate number: {plate_number}")
    result = await admin_vehicle_management_service.delete_vehicle_by_plate(plate_number)
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )

@admin_vehicle_management_router.patch("/assign_routes", tags=["Admin Vehicle Management"])
async def assign_routes(
        assignment: AssignRoutesModel,
        jwt: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> JSONResponse:
    logger.info(f"Assign routes request for vehicle: {assignment.vehicle_uuid}")
    result = await admin_vehicle_management_service.assign_routes(
        assignment.vehicle_uuid,
        assignment.route_uuids
    )
    return JSONResponse(
        status_code=result.get("code", 500),
        content=ResponseModel(
            success=result.get("success", False),
            message=result.get("message", ""),
            data=result.get("data", {}),
            error=result.get("error", "")
        ).model_dump()
    )

@admin_vehicle_management_router.patch("/delete_routes", tags=["Admin Vehicle Management"])
async def delete_routes(
        assignment: AssignRoutesModel,
        jwt: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> JSONResponse:
    logger.info(f"Delete routes request for vehicle: {assignment.vehicle_uuid}")
    result = await admin_vehicle_management_service.delete_routes(
        assignment.vehicle_uuid,
        assignment.route_uuids
    )
    return JSONResponse(
        status_code=result.get("code", 500),
        content=ResponseModel(
            success=result.get("success", False),
            message=result.get("message", ""),
            data=result.get("data", {}),
            error=result.get("error", "")
        ).model_dump()
    )