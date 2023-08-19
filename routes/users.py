from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from models.users import User
from schemas.users import CreateUserSchema, OutputUserSchema
from utils.passwords import create_hash_password

router = APIRouter()


@router.post(
    "/register",
)
async def register(new_user: CreateUserSchema) -> JSONResponse:
    """Get a new user's information and create a new user in the database."""
    if exists := await User.get_users_by_email(email=new_user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {exists.email} already exists",
        )
    new_user.password = create_hash_password(new_user.password)
    result = await User(
        email=new_user.email, hashed_password=new_user.password
    ).insert()

    return JSONResponse(
        content={
            "message": OutputUserSchema(**result.model_dump(by_alias=True)).model_dump()
        },
        status_code=status.HTTP_201_CREATED,
    )


@router.post("/access-token")
async def get_access_token():
    """Get a new access token for a user."""
    pass


@router.put("/activated")
async def activate_user():
    """Activate a user's account."""
    pass


@router.get("/me")
async def get_me():
    """Get the current user's information."""
    pass
