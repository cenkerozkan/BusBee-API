import time
import asyncio

from src.common.util.logger import get_logger
from ...repository.end_user_repository import end_user_repository

from firebase_admin import auth

logger = get_logger(__name__)


def delete_unverified_email(
        email: str
) -> None:
    logger.info("Deleting unverified email")
    time.sleep(300)
    user = auth.get_user_by_email(email)
    if not user.email_verified:
        auth.delete_user(user.uid)
        asyncio.run(end_user_repository.delete_one_by_email(email))