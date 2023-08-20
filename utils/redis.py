import aioredis

from config.settings import settings


async def init_redis() -> aioredis.Redis:
    return await aioredis.from_url(settings.REDIS_URL)
