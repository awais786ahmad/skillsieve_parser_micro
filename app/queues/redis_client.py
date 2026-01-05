import redis.asyncio as redis
from app.config import settings
from app.core.logger import logger

logger.info("Initializing Redis client")

redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True
)
