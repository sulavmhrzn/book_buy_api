from datetime import datetime
from typing import Optional

from beanie import Document, Indexed
from pydantic import Field


class User(Document):
    email: Indexed(str, unique=True)
    hashed_password: str
    is_active: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"

    @classmethod
    async def get_users_by_email(cls, *, email: str) -> Optional["User"]:
        return await cls.find_one(cls.email == email)
