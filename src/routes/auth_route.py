import re

from fastapi import APIRouter, Depends, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import *

from ..common.request_model.auth_route_model import *
from ..service.auth_service import AuthService
from ..common.response_model.response_model import ResponseModel

auth_router = APIRouter(prefix="/firebase")

@auth_router.post("/login", tags=["Auth"])
def login(
        user_data: LoginRequest
) -> JSONResponse:
    _auth_service = AuthService()

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

    login_result:dict = _auth_service.login(user_data.email, user_data.password)
    return JSONResponse(
        status_code=login_result.get("code"),
        headers={"refresh_token": login_result.get("refresh_token"),
                 "id_token": login_result.get("id_token")},
        content=ResponseModel(
            success=login_result.get("success"),
            message=login_result.get("message"),
            data={},
            error=login_result.get("error")
        ).model_dump()
    )

@auth_router.post("/register", tags=["Auth"])
def register(
        user_data: LoginRequest
) -> JSONResponse:
    _auth_service = AuthService()
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

    register_result:dict = _auth_service.register(user_data.email, user_data.password)
    return JSONResponse(
        status_code=register_result.get("code"),
        headers={"refresh_token": register_result.get("refresh_token"),
                 "id_token": register_result.get("id_token")},
        content=ResponseModel(
            success=register_result.get("success"),
            message=register_result.get("message"),
            data={},
            error=register_result.get("error")
        ).model_dump()
    )


@auth_router.post("/logout", tags=["Auth"])
def logout():
    pass


@auth_router.post("/validate_token", tags=["Auth"])
def validate_token(user_data: ValidateRequest):
    _auth_service = AuthService()
    return _auth_service.validate_token(user_data.refresh_token)