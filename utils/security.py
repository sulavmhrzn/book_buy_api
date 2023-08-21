from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from config.settings import settings
from models.users import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/access-token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get the current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token=token, key=settings.JWT_SECRET, algorithms=["HS256"])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await User.get_user_by_email(email=email)
    if user is None:
        raise credentials_exception
    return user


async def get_admin_user(current_user: User = Depends(get_current_user)):
    """Get the admin user."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have enough permissions",
        )
    return current_user


def create_access_token(sub: str):
    """Create an access token."""
    to_encode = {"sub": sub, "exp": datetime.utcnow() + timedelta(minutes=30)}
    return jwt.encode(claims=to_encode, key=settings.JWT_SECRET, algorithm="HS256")
