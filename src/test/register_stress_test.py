import asyncio
import aiohttp
import time
import logging
from collections import Counter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

async def register_user(session, i):
    url = "http://localhost:8000/auth/end_user/register"
    payload = {
        "email": f"test{i}@test.com",
        "password": "Test123!"
    }

    try:
        logger.debug(f"Sending request {i} with email {payload['email']}")
        async with session.post(url, json=payload) as response:
            data = await response.json()
            logger.debug(f"Request {i} completed with status {response.status}")
            return response.status
    except Exception as e:
        logger.error(f"Request {i} failed: {str(e)}")
        return str(e)

async def main():
    logger.info("Starting stress test")
    start_time = time.time()
    requests_to_send = 80
    results = []

    logger.info(f"Configuration: {requests_to_send} total requests running concurrently")

    async with aiohttp.ClientSession() as session:
        tasks = [register_user(session, i) for i in range(requests_to_send)]
        results = await asyncio.gather(*tasks)

    end_time = time.time()
    duration = end_time - start_time

    # Count results
    status_counts = Counter(results)
    successful = sum(1 for status in results if isinstance(status, int) and 200 <= status < 300)
    failed = len(results) - successful

    logger.info("\n" + "="*50)
    logger.info("Test Summary:")
    logger.info(f"Duration: {duration:.2f} seconds")
    logger.info(f"Requests per second: {requests_to_send/duration:.2f}")
    logger.info(f"Total Requests: {len(results)}")
    logger.info(f"Successful: {successful}")
    logger.info(f"Failed: {failed}")
    logger.info("\nStatus Code Distribution:")
    for status, count in status_counts.items():
        logger.info(f"{status}: {count}")
    logger.info("="*50)

if __name__ == "__main__":
    asyncio.run(main())