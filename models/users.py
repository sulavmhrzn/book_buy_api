from datetime import datetime
from typing import Optional

from beanie import Document, Indexed
from pydantic import Field

from utils.passwords import verify_password


class User(Document):
    email: Indexed(str, unique=True)
    hashed_password: str
    is_active: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"

    @classmethod
    async def get_user_by_email(cls, *, email: str) -> Optional["User"]:
        return await cls.find_one(cls.email == email)

    @classmethod
    async def authenticate(cls, *, email: str, password: str) -> Optional["User"]:
        user = await cls.get_user_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
