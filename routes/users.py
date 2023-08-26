from datetime import datetime, timedelta

from fastapi import APIRouter, BackgroundTasks, Depends, status
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordRequestForm

from config.settings import settings
from models.tokens import ActivationToken
from models.users import User
from schemas.users import (
    ChangePasswordSchema,
    CreateUserSchema,
    GetNewActivationTokenSchema,
    OutputUserSchema,
)
from utils.helpers import error_response, success_response
from utils.mails import send_email
from utils.passwords import create_hash_password, verify_password
from utils.security import create_access_token, get_current_user
from utils.tokens import generate_token

router = APIRouter()


@router.post(
    "/register",
)
async def register(
    new_user: CreateUserSchema,
    background_tasks: BackgroundTasks,
):
    """Get a new user's information and create a new user in the database."""
    if exists := await User.get_user_by_email(email=new_user.email):
        raise error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=f"User with email {exists.email} already exists.",
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

    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="User created successfully.",
    )


@router.post("/activate-token")
async def get_activation_token(
    user: GetNewActivationTokenSchema, background_tasks: BackgroundTasks
):
    """Get a new activation token for a user."""
    user_exists = await User.get_user_by_email(email=user.email)
    if not user_exists:
        raise error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=f"User with email {exists.email} already exists.",
        )
    exists = await ActivationToken.get_token_for_user(user_id=user_exists.id)
    if exists:
        # if the token hasn't expired, return it instead of creating a new one
        if exists.expires_at > datetime.utcnow():
            return success_response(
                message={"token": exists.activation_token},
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
        body=f"Your activation token: {token.activation_token}. Please activate your account within 24 hours.",
    )
    return success_response(
        message={"token": token.activation_token},
        status_code=status.HTTP_201_CREATED,
    )


@router.post("/access-token")
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Get a new access token for a user."""
    email = form_data.username
    password = form_data.password
    user = await User.authenticate(email=email, password=password)
    if not user:
        raise error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Invalid credentials.",
        )
    if not user.is_active:
        raise error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Inactive user. Please activate your account first.",
        )
    token = create_access_token(sub=user.email)
    return {"access_token": token, "token_type": "bearer"}


@router.put("/activated")
async def activate_user(token: str):
    """Activate a user's account."""
    exists = await ActivationToken.find_one(ActivationToken.activation_token == token)
    if not exists:
        raise error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Invalid token.",
        )
    if exists.expires_at < datetime.utcnow():
        await exists.delete()
        raise error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Token has expired.",
        )
    user = await User.find_one(User.id == exists.user_id)
    user.is_active = True
    await user.save()
    await exists.delete()
    return success_response(
        message="User activated.",
        status_code=status.HTTP_200_OK,
    )


@router.get("/me", response_model=OutputUserSchema)
async def get_me(user: User = Depends(get_current_user)):
    """Get the current user's information."""
    return user.model_dump(by_alias=True)


@router.post("/change-password")
async def change_password(
    password: ChangePasswordSchema,
    request: Request,
    user: User = Depends(get_current_user),
):
    """Reset a user's password."""
    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ")[1]

    if not verify_password(password.old_password, user.hashed_password):
        raise error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Please enter your current password correctly.",
        )
    if password.old_password == password.new_password:
        raise error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Your new password cannot be similar to the old password",
        )
    await request.app.state.redis.setex(
        f"bl_{token}", time=timedelta(minutes=settings.JWT_EXPIRY_MINUTES), value=token
    )

    user.hashed_password = create_hash_password(password.new_password)
    await user.save()
    return success_response(
        message="Password changed successfully.",
        status_code=status.HTTP_200_OK,
    )


@router.post("/logout")
async def logout(request: Request, user: User = Depends(get_current_user)):
    auth_header = request.headers.get("Authorization")
    token = auth_header.split(" ")[1]
    await request.app.state.redis.setex(
        f"bl_{token}", time=timedelta(minutes=settings.JWT_EXPIRY_MINUTES), value=token
    )
    return success_response(
        status_code=status.HTTP_200_OK, message="Logged out successfully."
    )
