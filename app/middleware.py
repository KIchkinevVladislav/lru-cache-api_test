from datetime import datetime
import logging
import time


from fastapi import Request


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)


async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info(f"Request: {request.method} {request.url} | Start: {datetime.fromtimestamp(start_time)} | Lead time: {process_time:.4f}s")

    return response
