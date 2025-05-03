from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.concurrency import run_in_threadpool
from ..firebase.firebase_handler import firebase_handler
from ..util.logger import get_logger

security = HTTPBearer()  # Create the security instance
logger = get_logger(__name__)

async def jwt_validator(credentials: HTTPAuthorizationCredentials = Depends(security)) -> bool:
    jwt = credentials.credentials
    logger.info(f"Validate JWT: {jwt}")
    try:
        # Verify id token
        is_valid = await run_in_threadpool(
            firebase_handler.validate_token, jwt
        )
        logger.info(f"JWT validation result: {is_valid}")
        return True if is_valid else False
    except Exception as e:
        logger.error(f"Error validating token: {e}")
        return False