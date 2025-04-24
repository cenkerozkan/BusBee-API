from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..common.request_model.admin_route_management_models import NewRoute, UpdateRouteModel
from ..common.response_model.response_model import ResponseModel
from ..common.util.logger import get_logger
from ..service.admin_route_management_service import admin_route_management_service

logger = get_logger(__name__)

admin_route_management_router = APIRouter(prefix="/admin/management/route", tags=["Admin Route Management"])

@admin_route_management_router.post("/create", tags=["Admin Route Management"])
async def create_route(
        route_data: NewRoute,
        jwt: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> JSONResponse:
    logger.info(f"Create route request for route: {route_data.route_name}")
    result: dict = await admin_route_management_service.create_route(route_data)
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )

@admin_route_management_router.delete("/delete/{route_id}", tags=["Admin Route Management"])
async def delete_route(
        route_id: str,
        jwt: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> JSONResponse:
    logger.info(f"Delete route request for route id: {route_id}")
    result: dict = await admin_route_management_service.delete_route_by_id(route_id)
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )

@admin_route_management_router.delete("/delete_by_name/{route_name}", tags=["Admin Route Management"])
async def delete_route_by_name(
        route_name: str,
        jwt: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> JSONResponse:
    logger.info(f"Delete route request for route name: {route_name}")
    result: dict = await admin_route_management_service.delete_route_by_name(route_name)
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )

@admin_route_management_router.patch("/update", tags=["Admin Route Management"])
async def update_route(
        route_data: UpdateRouteModel,
        jwt: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> JSONResponse:
    logger.info(f"Update route request for route: {route_data.route_name}")
    result: dict = await admin_route_management_service.update_route(route_data)
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )

@admin_route_management_router.get("/get_all", tags=["Admin Route Management"])
async def get_all_routes(
        jwt: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> JSONResponse:
    logger.info("Get all routes request")
    result: dict = await admin_route_management_service.get_all_routes()
    return JSONResponse(
        status_code=result.get("code"),
        content=ResponseModel(
            success=result.get("success"),
            message=result.get("message"),
            data=result.get("data"),
            error=result.get("error")
        ).model_dump()
    )