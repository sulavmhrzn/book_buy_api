from datetime import datetime
from typing import Optional

from beanie import Document, PydanticObjectId


class ActivationToken(Document):
    activation_token: str
    user_id: PydanticObjectId
    expires_at: datetime

    class Settings:
        name = "activation_tokens"

    @classmethod
    async def get_token_for_user(
        cls, *, user_id: PydanticObjectId
    ) -> Optional["ActivationToken"]:
        """Get a token for a user."""
        return await cls.find_one(cls.user_id == user_id)
