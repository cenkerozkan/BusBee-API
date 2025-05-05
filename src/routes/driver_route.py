import json
import os

from dotenv import load_dotenv

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..common.response_model.response_model import ResponseModel
from ..common.util.logger import get_logger
from ..service.driver_user_service import driver_service
from ..common.request_model.driver_models import LocationDataModel
from ..common.db.model.bus_location_model import BusLocationModel
from ..common.util.jwt_validator import jwt_validator  # Import the validator

logger = get_logger(__name__)
load_dotenv()
API_KEY = os.getenv("DRIVER_API_KEY")

driver_router = APIRouter(prefix="/driver", tags=["Driver"])

@driver_router.get("/get_vehicle/{driver_uid}", tags=["Driver"])
async def get_vehicle(
        driver_uid: str,
        is_jwt_valid: bool = Depends(jwt_validator),  # Apply JWT dependency
) -> JSONResponse:
    if not is_jwt_valid:
        return JSONResponse(
            status_code=401,
            content=ResponseModel(success=False, message="Invalid JWT", data={},error="").model_dump())
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
        is_jwt_valid: bool = Depends(jwt_validator),  # Apply JWT dependency
) -> JSONResponse:
    if not is_jwt_valid:
        return JSONResponse(
            status_code=401,
            content=ResponseModel(success=False, message="Invalid JWT", data={},error="").model_dump())
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

@driver_router.post("/start_journey/{driver_uid}", tags=["Driver"])
async def start_journey(
        driver_uid: str,
        is_jwt_valid: bool = Depends(jwt_validator),  # Apply JWT dependency
) -> JSONResponse:
    if not is_jwt_valid:
        return JSONResponse(
            status_code=401,
            content=ResponseModel(success=False, message="Invalid JWT", data={},error="").model_dump())
    logger.info(f"Start journey request for driver UID: {driver_uid}")
    result = await driver_service.start_journey(driver_uid)
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )

@driver_router.post("/stop_journey/{driver_uid}/{journal_uuid}", tags=["Driver"])
async def start_journey(
        driver_uid: str,
        journal_uuid: str,
        is_jwt_valid: bool = Depends(jwt_validator),  # Apply JWT dependency
) -> JSONResponse:
    if not is_jwt_valid:
        return JSONResponse(
            status_code=401,
            content=ResponseModel(success=False, message="Invalid JWT", data={},error="").model_dump())
    logger.info(f"Start journey request for driver UID: {driver_uid}")
    result = await driver_service.stop_journey(driver_uid, journal_uuid)
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )

@driver_router.get("/get_driver_information/{driver_uid}", tags=["Driver"])
async def get_driver_information(
        driver_uid: str,
        is_jwt_valid: bool = Depends(jwt_validator),  # Apply JWT dependency
) -> JSONResponse:
    if not is_jwt_valid:
        return JSONResponse(
            status_code=401,
            content=ResponseModel(success=False, message="Invalid JWT", data={},error="").model_dump())
    logger.info(f"Get driver information request for driver UID: {driver_uid}")
    result = await driver_service.get_driver_information(driver_uid)
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )


@driver_router.websocket("/ws/update_location")
async def update_location(websocket: WebSocket) -> None:
    # Retrieve API key from headers
    api_key = websocket.headers.get("DRIVER-API-KEY")
    logger.info(f"Driver connection attempt with API key: {api_key}")
    if api_key != API_KEY:
        logger.warning("Unauthorized WebSocket connection attempt")
        await websocket.close(code=1008)  # Policy Violation
        return

    await websocket.accept()
    logger.info("WebSocket connection accepted")

    try:
        while True:
            raw_data: str = await websocket.receive_text()
            jsonified_data: dict = json.loads(raw_data)

            # Parse incoming data to Pydantic model
            location_data = LocationDataModel(**jsonified_data)
            bus_location = BusLocationModel(
                lat=location_data.lat,
                lon=location_data.lon,
                time=location_data.timestamp
            )

            # Call service layer to handle update
            result: dict = await driver_service.update_journal(
                journal_uuid=location_data.journal_uuid,
                location=bus_location
            )

            # Respond to client
            await websocket.send_json(result)

    except WebSocketDisconnect:
        logger.info("Driver disconnected from WebSocket")
    except Exception as e:
        logger.exception(f"Unexpected error in WebSocket connection: {e}")
        await websocket.close(code=1011)  # Internal Error