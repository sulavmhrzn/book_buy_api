from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from models.authors import Author


class BaseBookSchema(BaseModel):
    title: str
    isbn: str
    price: int
    description: str
    lanugage: str
    author_id: PydanticObjectId
    genre: list[str]
    image_url: str


class BookCreateSchema(BaseBookSchema):
    pass


class BookListOutSchema(BaseBookSchema):
    id: PydanticObjectId = Field(..., alias="_id")
