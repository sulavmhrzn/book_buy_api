from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from config.settings import settings
from models.users import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/access-token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get the current user."""
    try:
        payload = jwt.decode(token=token, key=settings.JWT_SECRET, algorithms=["HS256"])
        email = payload.get("sub")
        user = await User.get_user_by_email(email=email)
        return user or None
    except JWTError as err:
        raise err


def create_access_token(sub: str):
    """Create an access token."""
    to_encode = {"sub": sub, "exp": datetime.utcnow() + timedelta(minutes=30)}
    return jwt.encode(claims=to_encode, key=settings.JWT_SECRET, algorithm="HS256")
