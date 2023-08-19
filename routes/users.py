from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from schemas.users import CreateUserSchema, OutputUserSchema

router = APIRouter()


@router.post(
    "/register",
)
async def register(new_user: CreateUserSchema) -> JSONResponse:
    """Get a new user's information and create a new user in the database."""
    return JSONResponse(
        content={"message": "User created"}, status_code=status.HTTP_201_CREATED
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
