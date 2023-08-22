from datetime import datetime

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field


class Book(Document):
    title: Indexed(str)
    isbn: str
    price: int
    description: str
    lanugage: str
    author_id: PydanticObjectId
    genre: list[str]
    image_url: str
    created_at: datetime

    class Settings:
        name = "books"
