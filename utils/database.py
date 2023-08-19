from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from config.settings import settings
from models import users


async def init_db() -> None:
    client = AsyncIOMotorClient(settings.MONGO_URI)

    await init_beanie(
        database=client[settings.MONGO_DB],
        document_models=[
            users.User,
        ],
    )
