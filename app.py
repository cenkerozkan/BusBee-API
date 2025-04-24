import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.common.response_model.response_model import ResponseModel
from src.repository.end_user_repository import end_user_repository
from src.repository.admin_user_repository import admin_user_repository
from src.repository.driver_user_repository import driver_user_repository

from src.routes.end_user_auth_route import end_user_auth_router
from src.routes.admin_user_auth_route import admin_user_auth_router
from src.routes.admin_driver_management_route import admin_driver_management_router
from src.routes.admin_route_management_route import admin_route_management_router

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await asyncio.gather(
            admin_user_repository.ensure_db_setup(),
            end_user_repository.ensure_db_setup(),
            driver_user_repository.ensure_db_setup()
        )
    except Exception as e:
        raise e

    yield

app = FastAPI(root_path="/api", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
        request: Request,
        exc: StarletteHTTPException
) -> JSONResponse:
    error_response = ResponseModel(
        success=False,
        message=str(exc.detail),
        data={},
        error=""
    ).model_dump()

    status_code_messages = {
        404: "Not found",
        401: "Unauthorized",
        403: "Not authenticated",
        500: "Internal server error"
    }

    if exc.status_code in status_code_messages:
        error_response["message"] = status_code_messages[exc.status_code]

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response
    )


app.include_router(end_user_auth_router)
app.include_router(admin_user_auth_router)
app.include_router(admin_driver_management_router)
app.include_router(admin_route_management_router)