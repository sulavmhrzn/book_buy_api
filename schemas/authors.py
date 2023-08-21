from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class BaseAuthorSchema(BaseModel):
    first_name: str
    last_name: str


class CreateAuthorSchema(BaseAuthorSchema):
    pass


class OutputAuthorSchema(BaseAuthorSchema):
    id: PydanticObjectId = Field(..., alias="_id")


class UpdateAuthorSchema(BaseModel):
    first_name: str = None
    last_name: str = None
