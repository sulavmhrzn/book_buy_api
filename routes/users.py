from datetime import datetime, timedelta

from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from fastapi.responses import JSONResponse

from models.tokens import ActivationToken
from models.users import User
from schemas.users import (
    CreateUserSchema,
    GetNewActivationTokenSchema,
    OutputUserSchema,
)
from utils.mails import send_email
from utils.passwords import create_hash_password
from utils.tokens import generate_token

router = APIRouter()


@router.post(
    "/register",
)
async def register(
    new_user: CreateUserSchema,
    background_tasks: BackgroundTasks,
) -> JSONResponse:
    """Get a new user's information and create a new user in the database."""
    if exists := await User.get_user_by_email(email=new_user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {exists.email} already exists",
        )
    new_user.password = create_hash_password(new_user.password)
    result = await User(
        email=new_user.email, hashed_password=new_user.password
    ).insert()

    token = await ActivationToken(
        activation_token=generate_token(),
        user_id=result.id,
        expires_at=datetime.utcnow() + timedelta(days=1),
    ).insert()

    background_tasks.add_task(
        send_email,
        subject="Activation Token",
        recipients=new_user.email,
        body=f"Thank you for registering! Here's your activation token: {token.activation_token}",
    )

    return JSONResponse(
        content={
            "message": OutputUserSchema(**result.model_dump(by_alias=True)).model_dump()
        },
        status_code=status.HTTP_201_CREATED,
    )


@router.post("/activate-token")
async def get_activation_token(
    user: GetNewActivationTokenSchema, background_tasks: BackgroundTasks
):
    """Get a new activation token for a user."""
    user_exists = await User.get_user_by_email(email=user.email)
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {user.email} not found",
        )
    exists = await ActivationToken.get_token_for_user(user_id=user_exists.id)
    if exists:
        # if the token hasn't expired, return it instead of creating a new one
        if exists.expires_at > datetime.utcnow():
            return JSONResponse(
                content=f"Your activation token: {exists.activation_token}",
                status_code=status.HTTP_200_OK,
            )
        await exists.delete()
    token = await ActivationToken(
        activation_token=generate_token(),
        user_id=user_exists.id,
        expires_at=datetime.utcnow() + timedelta(days=1),
    ).insert()
    background_tasks.add_task(
        send_email,
        subject="Activation Token",
        recipients=user_exists.email,
        body=f"Your activation token: {token.activation_token}. Please use it within 24 hours.",
    )
    return JSONResponse(
        content=f"Your new activation token: {token.activation_token}. Please use it within 24 hours.",
        status_code=status.HTTP_201_CREATED,
    )


@router.post("/access-token")
async def get_access_token():
    """Get a new access token for a user."""
    pass


@router.put("/activated")
async def activate_user(token: str):
    """Activate a user's account."""
    exists = await ActivationToken.find_one(ActivationToken.activation_token == token)
    if not exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token.",
        )
    if exists.expires_at < datetime.utcnow():
        await exists.delete()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token has expired.",
        )
    user = await User.find_one(User.id == exists.user_id)
    user.is_active = True
    await user.save()
    await exists.delete()
    return JSONResponse(
        content="User activated.",
        status_code=status.HTTP_200_OK,
    )


@router.get("/me")
async def get_me():
    """Get the current user's information."""
    pass
