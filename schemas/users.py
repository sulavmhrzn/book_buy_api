from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class BaseUserSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=32)


class CreateUserSchema(BaseUserSchema):
    confirm_password: str = Field(..., min_length=8, max_length=32)

    @model_validator(mode="after")
    def check_passwords_match(self) -> "CreateUserSchema":
        if (
            self.password is not None
            and self.confirm_password is not None
            and self.password != self.confirm_password
        ):
            raise ValueError("passwords do not match")
        return self


class OutputUserSchema(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    email: EmailStr
    is_active: bool
    model_config = ConfigDict(extra="ignore")


class GetNewActivationTokenSchema(BaseModel):
    email: EmailStr


class ChangePasswordSchema(BaseModel):
    old_password: str = Field(..., min_length=8, max_length=32)
    new_password: str = Field(..., min_length=8, max_length=32)
