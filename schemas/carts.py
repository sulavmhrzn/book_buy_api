from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class BaseCartItemsSchema(BaseModel):
    book_id: PydanticObjectId
    quantity: int = Field(1, gt=0)


class CreateCartItemSchema(BaseCartItemsSchema):
    pass


class CartItemSchema(BaseModel):
    book_id: PydanticObjectId
    quantity: int = 1


class BaseCartSchema(BaseModel):
    cart_items: list[CreateCartItemSchema] = []


class CreateCartSchema(BaseCartSchema):
    pass


class CreateCartSchemaInDB(BaseCartSchema):
    user_id: PydanticObjectId


class OutputCartSchema(BaseCartSchema):
    id: PydanticObjectId = Field(..., alias="_id")
    total_price: int
