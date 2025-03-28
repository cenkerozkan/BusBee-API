import os
from dotenv import load_dotenv

from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from fastapi.encoders import jsonable_encoder

from .logger import get_logger

load_dotenv()
API_KEY: str = os.getenv("ADMIN_API_KEY")
api_key_header = APIKeyHeader(name="ADMIN-API-KEY", auto_error=True)
logger = get_logger(__name__)

async def validate_admin_api_key(api_key: str = Security(api_key_header)) -> bool:
    logger.info(f"header {api_key}")
    logger.info(f"Validating admin API key: {API_KEY}")
    if api_key == API_KEY:
        return True
    return False