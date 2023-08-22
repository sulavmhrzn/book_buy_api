from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from schemas.authors import OutputAuthorSchema


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
    created_at: datetime = Field(default_factory=datetime.utcnow)


class BookListOutSchema(BaseBookSchema):
    id: PydanticObjectId = Field(..., alias="_id")


class BookDetailOutSchema(BookListOutSchema):
    created_at: datetime
    author: list[OutputAuthorSchema]
