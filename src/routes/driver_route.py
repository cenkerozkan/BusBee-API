from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..common.response_model.response_model import ResponseModel
from ..common.util.logger import get_logger
from ..service.driver_service import driver_service

logger = get_logger(__name__)

driver_router = APIRouter(prefix="/driver", tags=["Driver"])

@driver_router.get("/get_vehicle/{driver_uid}", tags=["Driver"])
async def get_vehicle(
        driver_uid: str,
        jwt: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> JSONResponse:
    logger.info(f"Get vehicle request for driver UID: {driver_uid}")
    result = await driver_service.get_vehicle(driver_uid)
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )

@driver_router.get("/get_vehicle_route/{driver_uid}", tags=["Driver"])
async def get_vehicle_route(
        driver_uid: str,
        jwt: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> JSONResponse:
    logger.info(f"Get vehicle route request for driver UID: {driver_uid}")
    result = await driver_service.get_vehicle_route(driver_uid)
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )