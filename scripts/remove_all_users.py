import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
import logging
import asyncio
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

CREDENTIALS = credentials.Certificate = credentials.Certificate(
            {
                "type": os.getenv("TYPE"),
                "project_id": os.getenv("PROJECT_ID"),
                "private_key_id": os.getenv("PRIVATE_KEY_ID"),
                "private_key": os.getenv("PRIVATE_KEY").replace(r'\n', '\n'),
                "client_email": os.getenv("CLIENT_EMAIL"),
                "client_id": os.getenv("CLIENT_ID"),
                "auth_uri": os.getenv("AUTH_URI"),
                "token_uri": os.getenv("TOKEN_URI"),
                "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
                "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
                "universe_domain": os.getenv("UNIVERSE_DOMAIN"),
            }
        )


async def delete_users_batch(user_list: List[auth.UserRecord]) -> tuple[int, int]:
    """Delete a batch of users and return success/failure counts"""
    success = 0
    failed = 0

    for user in user_list:
        try:
            auth.delete_user(user.uid)
            success += 1
            logger.debug(f"Deleted user: {user.email or user.phone_number}")
        except Exception as e:
            failed += 1
            logger.error(f"Failed to delete user {user.uid}: {str(e)}")

    return success, failed


async def main():
    logger.info("Starting user cleanup")

    try:
        # Get all users (Firebase returns them in batches automatically)
        page = auth.list_users()
        total_success = 0
        total_failed = 0
        batch_size = 100
        current_batch: List[auth.UserRecord] = []

        # Process users in batches
        for user in page.iterate_all():
            current_batch.append(user)

            if len(current_batch) >= batch_size:
                logger.info(f"Processing batch of {len(current_batch)} users")
                success, failed = await delete_users_batch(current_batch)
                total_success += success
                total_failed += failed
                current_batch = []

        # Process remaining users
        if current_batch:
            logger.info(f"Processing final batch of {len(current_batch)} users")
            success, failed = await delete_users_batch(current_batch)
            total_success += success
            total_failed += failed

        logger.info("=" * 50)
        logger.info("Cleanup Summary:")
        logger.info(f"Successfully deleted: {total_success} users")
        logger.info(f"Failed to delete: {total_failed} users")
        logger.info("=" * 50)

    except Exception as e:
        logger.error(f"Failed to list/delete users: {str(e)}")


if __name__ == "__main__":
    # Initialize Firebase Admin SDK (uses default credentials)
    firebase_admin.initialize_app(CREDENTIALS)
    asyncio.run(main())