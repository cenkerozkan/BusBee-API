import json
import os
from dotenv import load_dotenv

from fastapi import APIRouter, Depends, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..common.request_model.passenger_models import FetchVehicleLocationModel
from ..common.response_model.response_model import ResponseModel
from ..common.util.logger import get_logger
from ..common.util.jwt_validator import jwt_validator
from ..service.end_user_service import end_user_service

load_dotenv()
API_KEY: str = os.getenv("PASSENGER_API_KEY")

logger = get_logger(__name__)

end_user_router = APIRouter(prefix="/passenger")

@end_user_router.get("/get_passenger_information/{uid}", tags=["End User"])
async def get_passenger_info(
        uid: str,
        is_jwt_valid: bool = Depends(jwt_validator),
) -> JSONResponse:
    if not is_jwt_valid:
        return JSONResponse(
            status_code=401,
            content=ResponseModel(success=False, message="Invalid JWT", data={},error="").model_dump())
    result: dict = await end_user_service.get_passenger_information(uid)
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )

@end_user_router.get("/get_all_routes", tags=["End User"])
async def get_all_routes(is_jwt_valid: bool = Depends(jwt_validator)) -> JSONResponse:
    if not is_jwt_valid:
        return JSONResponse(
            status_code=401,
            content=ResponseModel(success=False, message="Invalid JWT", data={}, error="").model_dump())
    result: dict = await end_user_service.get_all_routes()
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )

@end_user_router.get("/get_all_active_journeys", tags=["End User"])
async def get_all_active_journeys(is_jwt_valid: bool = Depends(jwt_validator)) -> JSONResponse:
    if not is_jwt_valid:
        return JSONResponse(
            status_code=401,
            content=ResponseModel(success=False, message="Invalid JWT", data={}, error="").model_dump())
    result: dict = await end_user_service.get_all_active_journeys()
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )

@end_user_router.websocket("/ws/fetch_vehicle_location")
async def fetch_vehicle_location(websocket: WebSocket) -> None:
    # Retrieve API key from headers
    api_key = websocket.headers.get("PASSENGER-API-KEY")
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

            new_passenger_request: FetchVehicleLocationModel = FetchVehicleLocationModel(**jsonified_data)
            result: dict = await end_user_service.fetch_vehicle_location(new_passenger_request.journal_uuid)

            await websocket.send_json(result)

    except WebSocketDisconnect:
        logger.info("Driver disconnected from WebSocket")
    except Exception as e:
        logger.exception(f"Unexpected error in WebSocket connection: {e}")
        await websocket.close(code=1011)  # Internal Error