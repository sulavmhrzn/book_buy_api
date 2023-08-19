from datetime import datetime

from beanie import Document, PydanticObjectId


class ActivationToken(Document):
    activation_token: str
    user_id: PydanticObjectId
    expires_at: datetime

    class Settings:
        name = "activation_tokens"
