from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from config.settings import settings
from models import authors, books, carts, tokens, users


async def init_db() -> None:
    client = AsyncIOMotorClient(settings.MONGO_URI)

    await init_beanie(
        database=client[settings.MONGO_DB],
        document_models=[
            users.User,
            tokens.ActivationToken,
            authors.Author,
            books.Book,
            carts.Cart,
        ],
    )
