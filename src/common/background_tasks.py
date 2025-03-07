import firebase_admin
from firebase_admin import credentials, auth
import time
import os

from .logger import get_logger

logger = get_logger(__name__)


def delete_unverified_email(
        email: str
) -> None:
    logger.info("Deleting unverified email")
    time.sleep(300)
    user = auth.get_user_by_email(email)
    if not user.email_verified:
        auth.delete_user(user.uid)